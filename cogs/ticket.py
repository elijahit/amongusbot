# Sistema Ticket per Among Us Ita (amongusita.it)
# Sviluppato da MyNameIsDark01#5955
# Per Among Us Ita#2534
from discord.ext import commands
import discord
import os


# from Warn import WarnClass
class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        cfg = self.bot.get_cog('Config') 
        self.ticketChannel = 748908550973292604  # canale ticket
        self.category = 750086378028793908  # categoria canale ticket
        self.role = 748907435174920283  # support role
        self.cache = 762079923942195220  # cache channels
        self.limited_roles = [cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.rolea7, cfg.rolea8, cfg.rolea9] # limited roles
        self.limit = [4, 3, 3, 2, 2, 2] # number of tickets for limited roles
        self.stato = "Non definito"

    # => Help Command
    @commands.command()
    async def tickethelp(self, ctx):
        cfg = self.bot.get_cog('Config') 
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:

            d = "it!tAdd - Aggiungere un utente al ticket"
            embed = discord.Embed(title="Comandi Ticket", description=d, color=discord.Colour.green())
            await ctx.send(embed=embed)
            await ctx.message.delete()

    # => Send Ticket Message
    @commands.command()
    async def tmessage(self, ctx):
        cfg = self.bot.get_cog('Config') 
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            
            embed = discord.Embed(title="Pannello Tickets", description = "Per aprire un ticket e contattare lo staff premi la reazione 🎫 sottostante.\nTi ricordo che qualsiasi ticket aperto e inutilizzato sarà frutto di warn.\n\nIn caso di problemi relativi ai sistemi sviluppati per Among Us Ita contatta un **Developers** o un **Mod**", color = discord.Colour.green())
            z = await ctx.send(embed=embed)
            await z.add_reaction('🎫')
    
    # => Add user to ticket
    @commands.command()
    async def tadd(self, ctx, arg: discord.User):
        cfg = self.bot.get_cog('Config') 
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
        
            channel = ctx.message.channel
            user_2_add = arg

            t = "Aggiunto utente"
            d = f"L'utente {user_2_add.mention} è stato aggiunto alla stanza"
            await ctx.message.delete()
            await channel.set_permissions(user_2_add, read_messages=True, send_messages=True, add_reactions=False, read_message_history=True)
            embed = discord.Embed(title=t, description=d)
            await ctx.send(embed=embed)
    @tadd.error
    async def tadd_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!tadd (@tag/id)")

    # => Listen reaction + Ticket Functions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user_id = payload.user_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        emoji = payload.emoji.name
        guild_id = payload.guild_id
        member = payload.member
        user_roles = [i.id for i in member.roles]
        
        if user_id != self.bot.user.id:
            if channel_id == self.ticketChannel and emoji == '🎫':
                
                user = self.bot.get_user(user_id)
                channel = self.bot.get_channel(self.ticketChannel)
                msg = await channel.fetch_message(message_id)
                
                await msg.remove_reaction('🎫', user)
                await Ticket.create_channel(self, user_id, guild_id)

            channel = self.bot.get_channel(channel_id)
            is_support = True if self.role in user_roles else False
            if 'ticket-' in channel.name and is_support:
                if emoji == '✅':                    
                    # Claim
                    await Ticket.claim_ticket(self, user_id, message_id, channel_id, guild_id, user_roles)
                elif emoji == '🟡':
                    # Non è stato possibile
                    message = ("Mi dispiace", "Non è stato possibile chiudere il ticket in maniera corretta", 15844367)
                    await Ticket.send_direct(self, channel_id, message)
                    self.stato = "Non risolto"
                    await Ticket.cache_messages(self, channel_id)
                    await Ticket.delete_channel(self, channel_id)
                elif emoji == '🟢':
                    # Risolto con successo
                    message = ("Perfetto!", "Il ticket è stato risolto.", 3066993)
                    await Ticket.send_direct(self, channel_id, message)
                    self.stato = "Risolto"
                    await Ticket.cache_messages(self, channel_id)
                    await Ticket.delete_channel(self, channel_id)
                elif emoji == '🔴':
                    # Da finire, manca la sezione warn
                    await Ticket.warn_on_useless_ticket(self, guild_id, channel, member, user_id, 1, f'Ticket Inutilizzato \"{channel.name}\""')                
                    message = ("Segnalazione inutile!",
                               "Mi dispiace ma sembra che il tuo ticket sia inutilizzato per cui sei stato warnato.",
                               15158332)
                    await Ticket.send_direct(self, channel_id, message)
                    self.stato = "Inutilizzato"
                    await Ticket.cache_messages(self, channel_id)
                    await Ticket.delete_channel(self, channel_id)
                    # WarnClass.warn(self, user_id)
                    pass

    async def create_channel(self, user_id, guild):
        conn = self.bot.get_cog('Db')
        z = conn.fetchall('SELECT * FROM tickets WHERE user_id = ?', (user_id,))
        if len(z) == 0:
            conn.execute("INSERT INTO tickets (user_id) VALUES (?)", (user_id,))
            await conn.commit()
            n = conn.fetchall('SELECT * FROM tickets WHERE user_id = ?', (user_id,))[0][0]

            guild = self.bot.get_guild(guild)
            category = self.bot.get_channel(self.category)
            user = self.bot.get_user(user_id)
            ticket_support_role = guild.get_role(self.role)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=False,
                                                  add_reactions=False),
                ticket_support_role: discord.PermissionOverwrite(view_channel=True, read_messages=True,
                                                                 send_messages=False, add_reactions=True)
            }
            y = await guild.create_text_channel(name=f'Ticket-{n}', overwrites=overwrites, category=category)

            embed = discord.Embed(title=f"Ticket #{n}",
                                  description=f"{user.mention} attendi che la tua richiesta venga presa in carico "
                                              f"da un operatore.")
            m = await y.send(embed=embed)
            await m.add_reaction('✅')

            conn.execute("UPDATE tickets SET channel_id = ? WHERE user_id = ?", (y.id, user_id,))

        await conn.commit()

    async def claim_ticket(self, user_id, message_id, channel_id, guild_id, user_roles):

        conn = self.bot.get_cog('Db')
        
        check_n_ticket = conn.fetchall("SELECT * FROM tickets WHERE admin_id = ?", (user_id,))

        admin = self.bot.get_user(user_id)
        channel = self.bot.get_channel(channel_id)
        guild = self.bot.get_guild(guild_id)
        supporter = guild.get_role(self.role)
        moderator = guild.get_role(744631301872680980)
        senmod = guild.get_role(762459421665525802)
        thelper = guild.get_role(762459426128789525)
        
        utente = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))[0][1]
        utente = self.bot.get_user(utente)
        
        m = await channel.fetch_message(message_id)
        
        
        if len(check_n_ticket) > 0:
            for idx, i in enumerate(self.limited_roles):
                if i in user_roles and len(check_n_ticket) == self.limit[idx]:
                    await m.remove_reaction('✅', admin)
                    embed = discord.Embed(title="Errore", description="Mi dispiace ma hai raggiunto il numero massimo di ticket claimabili, per claimare questo ticket chiudo un tuo ticket.")
                    await admin.send(embed=embed)
                    return 0
                        
        conn.execute("UPDATE tickets SET admin_id = ? WHERE channel_id = ?", (user_id, channel_id,))
        try:
            for g in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user_id,)):
                if g[2] == None:
                    conn.execute("UPDATE analytics SET tickets = 1 WHERE admin_id = ?", (user_id,))
                else:
                    conn.execute("UPDATE analytics SET tickets = tickets+1 WHERE admin_id = ?", (user_id,))
        except:
            print("errorticket")
        try:
            d = conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user_id,))
            if len(d) == 0:
                conn.execute("INSERT INTO analytics (admin_id, tickets) VALUES (?, ?)", (user_id, 1,))
        except:
            print("error2ticket")
        
        await conn.commit()        

        await channel.set_permissions(supporter, read_messages=False, send_messages=False, add_reactions=False)
        await channel.set_permissions(utente, read_messages=True, send_messages=True, add_reactions=False, read_message_history=True)
        await channel.set_permissions(admin, read_messages=True, send_messages=True, add_reactions=True, read_message_history=True)
        await channel.set_permissions(moderator, read_messages=True, send_messages=True, add_reactions=True, read_message_history=True)
        await channel.set_permissions(senmod, read_messages=True, send_messages=True, add_reactions=True, read_message_history=True)
        await channel.set_permissions(thelper, read_messages=True, send_messages=True, add_reactions=True, read_message_history=True)

        await m.clear_reactions()
        await m.delete()

        embed = discord.Embed(title=m.embeds[0].title,
                              description=f"{utente.mention} la tua richiesta è stata presa in carico dallo "
                                          f"Staffer {admin.mention} di Among Us Ita.")

        embed.add_field(name="Legenda per lo Staff",
                        value="🔴 - Ticket inutilizzato\n"
                              "🟡 - Impossibile risolvere il ticket\n"
                              "🟢 - Ticket risolto correttamente")

        msg = await channel.send(embed=embed)
        await channel.send(f"Ciao {utente.mention} lo staffer {admin.mention} ha preso in carico la tua richiesta, descrivi chiaramente il tuo problema affinchè si risolva nel minor tempo possibile la tua problematica, ti ricordiamo che l'apertura di ticket inutilizzati prevede il warn.")
        await msg.add_reaction('🔴')
        await msg.add_reaction('🟡')
        await msg.add_reaction('🟢')

    async def delete_channel(self, channel_id):

        conn = self.bot.get_cog('Db')
        n_ticket = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))[0][0]

        conn = self.bot.get_cog('Db')
        conn.execute("DELETE FROM tickets WHERE channel_id = ?", (channel_id,))
        await conn.commit()

        channel = self.bot.get_channel(channel_id)
        await channel.delete(reason="Ticket chiuso.")

        if os.path.isfile(f'{n_ticket}.txt'):
            os.remove(f'{n_ticket}.txt')

    async def cache_messages(self, channel_id):

        conn = self.bot.get_cog('Db')
        ticket = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))

        n_ticket = ticket[0][0]
        channel = self.bot.get_channel(channel_id)
        cache = self.bot.get_channel(self.cache)

        cached_messages = []

        async for message in channel.history(oldest_first=True):
            author = message.author
            msg = message.content

            if author.id != self.bot.user.id:
                text = f"{author.name}: {msg}"
                cached_messages.append(text)

        title = f"Ticket N: {n_ticket}"
        
        user = self.bot.get_user(ticket[0][1])
        admin = self.bot.get_user(ticket[0][3])
        
        if len(cached_messages) == 0:
            description = "Nessun Messaggio"
            embed = discord.Embed(title = title, description = description)
            embed.add_field(name="Creatore", value=f"{user.mention}")
            embed.add_field(name="Admin", value=f"{admin.mention}")
            embed.add_field(name="Stato", value=f"{self.stato}")
            await cache.send(embed=embed)   
        else:
            with open(f'{n_ticket}.txt', 'w+') as f:
                f.write('\n'.join(cached_messages))
                
            embed = discord.Embed(title = title)
            embed.add_field(name="Creatore", value=f"{user}")
            embed.add_field(name="Admin", value=f"{admin}")
            embed.add_field(name="Stato", value=f"{self.stato}")
            await cache.send(embed=embed)
            
            with open(f'{n_ticket}.txt', 'rb') as f:
                await cache.send(file=discord.File(f))

    async def send_direct(self, channel_id, message: tuple):

        conn = self.bot.get_cog('Db')
        user_id = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))[0][1]

        user = self.bot.get_user(user_id)
        channel = self.bot.get_channel(channel_id)


        if user == None:
            pass
        else:
            try:
                embed = discord.Embed(title=message[0], description=message[1], colour=discord.Colour(message[2]))
                await user.send(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(title="Errore", description=f"Non riesco a contattare {user.mention} per \n{message[1]}")
                await channel.send(embed=embed)
            except discord.HTTPException:
                await channel.send(content="Richiesta fallita.")

    async def warn_on_useless_ticket(self, guild_id: int, channel: discord.TextChannel, member: discord.Member, user_id: int, gravity: int, reason: str = None):
        
        warn = self.bot.get_cog("Warns")
        conn = self.bot.get_cog("Db")
        
        guild = self.bot.get_guild(guild_id)
        user_id = conn.fetchall("SELECT user_id FROM tickets WHERE channel_id = ? AND admin_id = ?", (channel.id, member.id,))[0][0]
        
        user = self.bot.get_user(user_id)
        await warn.warn_user(guild, channel, member, user, gravity, reason)
                    
def setup(bot):
    bot.add_cog(Ticket(bot))
    print("[!] modulo ticket caricato")
