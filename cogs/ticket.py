from discord.ext import commands
import discord
import os


# from Warn import WarnClass
class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ticketChannel = 757654228259831872  # canale ticket
        self.category = 757654228259831871  # categoria canale ticket
        self.role = 757654227211518023  # support role
        self.cache = 757654228259831873  # cache channels

    @commands.command()
    async def ticket_help(self, ctx):

        d = "!tAdd - Aggiungere un utente al ticket"
        embed = discord.Embed(title="Comandi Ticket", description=d, color=discord.Colour.green())
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def t_add(self, ctx, arg: discord.User):

        channel = ctx.message.channel
        user_2_add = arg

        t = "Aggiunto utente"
        d = f"L'utente {user_2_add.mention} è stato aggiunto alla stanza"
        await ctx.message.delete()
        await channel.set_permissions(user_2_add, read_messages=True, send_messages=True, add_reactions=False)
        embed = discord.Embed(title=t, description=d)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        user_id = payload.user_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        emoji = payload.emoji.name
        guild_id = payload.guild_id
        member = payload.member

        if user_id != self.bot.user.id:
            if channel_id == self.ticketChannel and emoji == '🎫':
                channel = self.bot.get_channel(self.ticketChannel)
                msg = await channel.fetch_message(message_id)
                user = self.bot.get_user(user_id)
                await msg.remove_reaction('🎫', user)
                await Ticket.create_channel(self, user_id, guild_id)

            channel = self.bot.get_channel(channel_id)
            is_support = True if self.role in [i.id for i in member.roles] else False
            if 'ticket-' in channel.name and is_support:
                if emoji == '✅':
                    # Claim
                    await Ticket.claim_ticket(self, user_id, message_id, channel_id, guild_id)
                elif emoji == '🟡':
                    # Non è stato possibile
                    message = ("Mi dispiace", "Non è stato possibile chiudere il ticket in maniera corretta", 15844367)
                    await Ticket.send_direct(self, channel_id, message)
                    await Ticket.cache_messages(self, channel_id)
                    await Ticket.delete_channel(self, channel_id)
                elif emoji == '🔴':
                    # Risolto con successo
                    message = ("Perfetto!", "Il ticket è stato risolto.", 3066993)
                    await Ticket.send_direct(self, channel_id, message)
                    await Ticket.cache_messages(self, channel_id)
                    await Ticket.delete_channel(self, channel_id)
                elif emoji == '🔵':
                    # Da finire, manca la sezione warn
                    message = ("Segnalazione inutile!",
                               "Mi dispiace ma sembra che il tuo ticket sia inutilizzato per cui sei stato warnato.",
                               15158332)
                    await Ticket.send_direct(self, channel_id, message)
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

    async def claim_ticket(self, user_id, message_id, channel_id, guild_id):

        conn = self.bot.get_cog('Db')
        user_ = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))[0][1]

        await conn.commit()

        channel = self.bot.get_channel(channel_id)

        guild = self.bot.get_guild(guild_id)
        supporter = guild.get_role(self.role)
        user_ = self.bot.get_user(user_)
        user = self.bot.get_user(user_id)

        await channel.set_permissions(supporter, read_messages=False, send_messages=False, add_reactions=False)
        await channel.set_permissions(user_, read_messages=True, send_messages=True, add_reactions=False)
        await channel.set_permissions(user, read_messages=True, send_messages=True, add_reactions=True)

        m = await channel.fetch_message(message_id)
        await m.clear_reactions()
        await m.delete()

        embed = discord.Embed(title=m.embeds[0].title,
                              description=f"Ciao {user_.mention} la tua richiesta è stata presa in carico dallo "
                                          f"Staffer {user.mention} di Among Us Ita, come può esserti utile?\n"
                                          f"Esponi chiaramente la tua richiesta affinchè lo staffer possa "
                                          f"esaustivamente risolvere la tua problematica, ricordati che l'apertura di "
                                          f"ticket inutilizzati incomberà al warn.")

        embed.add_field(name="Legenda per lo Staff",
                        value="🔵 - Ticket inutilizzato\n"
                              "🟡 - Impossibile risolvere il ticket\n"
                              "🔴 - Ticket risolto correttamente")

        m = await channel.send(embed=embed)
        await m.add_reaction('🔵')
        await m.add_reaction('🟡')
        await m.add_reaction('🔴')

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
        n_ticket = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))[0][0]

        channel = self.bot.get_channel(channel_id)
        cache = self.bot.get_channel(self.cache)

        cached_messages = []

        async for message in channel.history(oldest_first=True):
            author = message.author
            msg = message.content

            if author.id != self.bot.user.id:
                text = f"{author.name}: {msg}"
                cached_messages.append(text)

        if len(cached_messages) == 0:
            embed = discord.Embed(title=f"Ticket N: {n_ticket}", description="Nessun Messaggio")
            await cache.send(embed=embed)
        else:
            with open(f'{n_ticket}.txt', 'w+') as f:
                f.write('\n'.join(cached_messages))
            embed = discord.Embed(title=f"Ticket N: {n_ticket}")
            await cache.send(embed=embed)
            with open(f'{n_ticket}.txt', 'rb') as f:
                await cache.send(file=discord.File(f))

    async def send_direct(self, channel_id, message: tuple):

        conn = self.bot.get_cog('Db')
        user_id = conn.fetchall("SELECT * FROM tickets WHERE channel_id = ?", (channel_id,))[0][1]

        user = self.bot.get_user(user_id)
        channel = self.bot.get_channel(channel_id)

        try:
            embed = discord.Embed(title=message[0], description=message[1], colour=discord.Colour(message[2]))
            await user.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description=f"I can't contact {user.mention} btw \n{message[1]}")
            await channel.send(embed=embed)
        except discord.HTTPException:
            await channel.send(content="Request Failed.")


def setup(bot):
    bot.add_cog(Ticket(bot))
    print("[!] modulo ticket caricato")
