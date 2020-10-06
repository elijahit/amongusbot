from discord.message import Embed
from discord.ext import commands
from discord import Color
from discord import utils
import discord
import random
import time


class cmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



#CMD utente

    @commands.command()
    async def ping(self, ctx):

        await ctx.message.delete()
        await ctx.send(f"Ping! In {round(self.bot.latency * 1000)}ms")

    @commands.command()#about
    async def about (self, ctx):

        await ctx.message.delete()
        cfg = self.bot.get_cog('Config')
        embed = self.bot.get_cog('Embeds')

        name = "About - Among Us Ita BOT"
        field = ("About 3rd Party Developers",
                 "**Among Us Ita BOT**\n"
                 "Questo BOT è stato creato e programmato in python da un team di 6+ developer per amongusita.it, sono stati richiesti \
                 mesi di programmazione per rendere lo stesso adeguato all'utenza attualmente dentro Among Us Ita.\
                 Il bot viene utilizato per gestire l'intera community di Among Us Ita, ciò che in altre community viene fatto con 7 bot diversi.\n"
                 "*Developers*: **Elijah**, **Nico**, **ImNotName**, **iTzSgrullee_**, **MyNameIsDark01**, **Kappa**\n\
                 Librerie utilizzate: *DiscordPy*\n\
                 \n© amongusita.it")

        about_embed = embed.get_standard_embed(name,
                                               cfg.green,
                                               ctx.guild.icon_url,
                                               [field],
                                               cfg.footer)
        await ctx.channel.send(embed=about_embed)



        return
###############    ADMIN COMMAND

    @commands.command() ###CMD AIUTO ADMIN
    async def acmds(self, ctx):
        cfg = self.bot.get_cog('Config')
        embed = self.bot.get_cog('Embeds')

        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            name = "COMANDI ADMIN - [it!]"
            field = ("Administrative Command", cfg.aiutoadmin)
            field2 = ("Moderative Command", cfg.aiutoadmin2)
            field3 = ("Non Administrative", cfg.aiutoadmin3)

            acmds_embed = embed.get_standard_embed(name,
                                               cfg.blue,
                                               ctx.guild.icon_url,
                                               [field, field2, field3],
                                               "[1] Owner | [2] Admin | [3] S. Mod | [4] Mod \n[5] S. Helper | [6] Helper | [7] T. Helper | [8] Gestore | [9] Prova")

            await ctx.channel.send(embed=acmds_embed)
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @commands.command()#comando purge
    async def purge(self, ctx, ammount = int(1)):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            if ammount <= 200:
                await ctx.channel.purge(limit=ammount)
                return
            else:
                try:
                    await ctx.message.author.send("Limite di messaggi da eliminare `200`.")
                    await ctx.message.delete()
                except:
                    pass
                return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!purge (valore max 200)")


    @commands.command()#addrole
    async def addrole(self, ctx, role:discord.Role, member:discord.Member=None, *, motivo=None):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        embed = self.bot.get_cog('Embeds')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea6, cfg.rolea7, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            roleadd = None
            try:
                query = "SELECT * FROM addrole WHERE role_id=?"
                values = (role.id,)
                roleadd = db.fetchall(query, values)[0][1]
            except:
                await ctx.message.delete()

                name = "Amministratore ruoli"
                field = ("Errore", f"Il ruolo {role.mention} non è presente nella lista di gestione.")

                role_embed = embed.get_standard_embed(name,
                                                cfg.red,
                                                ctx.guild.icon_url,
                                                [field],
                                                cfg.footer)

                await ctx.channel.send(embed=role_embed)


            if role.id == roleadd:

                rolecheck = discord.utils.find(lambda r: r.id == role.id, ctx.guild.roles)
                if rolecheck in member.roles:
                    
                    await ctx.message.delete()

                    name = "Amministratore ruoli"
                    field = ("Errore", f"L'utente {member.mention} possiede già il ruolo {role.mention}.")

                    role_embed = embed.get_standard_embed(name,
                                                    cfg.red,
                                                    ctx.guild.icon_url,
                                                    [field],
                                                    cfg.footer)

                    await ctx.channel.send(embed=role_embed)

                else:
                    await ctx.message.delete()
                    staff = self.bot.get_channel(cfg.staffroom) #canale sanzioni

                    name = "Amministratore ruoli"
                    field = ("Aggiunto", f"Hai inserito il ruolo {role.mention} al utente {member.mention} motivo: `{motivo}`.")

                    role_embed = embed.get_standard_embed(name,
                                                    cfg.blue,
                                                    ctx.guild.icon_url,
                                                    [field],
                                                    cfg.footer)

                    await ctx.channel.send(embed=role_embed)

                    name = "user-logs"
                    field = ("Aggiunto", f"{ctx.author.mention} ha inserito il ruolo {role.mention} al utente {member.mention} motivo: `{motivo}`.")

                    logs_embed = embed.get_standard_embed(name,
                                                    cfg.green,
                                                    ctx.guild.icon_url,
                                                    [field],
                                                    cfg.footer)

                    await staff.send(embed=logs_embed)
                    await member.add_roles(role)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!addrole (@ruolo) (@utente) (motivo)")


    @commands.command()#updatedb
    async def updatedb(self, ctx, table, colunm, where1, where2, *value):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0: 
            try:
                query = f"UPDATE {table} SET {colunm} = ? WHERE {where1} = ?"
                values = (' '.join(i for i in value), where2,)
                db.execute(query, values)
                await db.commit()
            except Exception as e:
                print(e)    
                
    @updatedb.error
    async def updatedb_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("[!] USA: it!updatedb (tabella) (colonna) (field) (contenuto) valore")
            await ctx.send("ES: it!updatedb config testo titolo welcomedm testo valore")

    @commands.command()#comando add reaction
    async def addreact(self, ctx, messageid, emoij):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            message = await ctx.channel.fetch_message(messageid)
            await message.add_reaction(emoij)
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return
    @addreact.error
    async def addreact_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!addreact (idmsg) (emoij)")
    
    @commands.command()#comando editmsg
    async def editmsg (self, ctx, id, *, messaggio):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            try:
                message = await ctx.channel.fetch_message(id)
            except discord.NotFound as e:
                await ctx.channel.send("Messaggio non trovato")
                raise e
            await message.edit(content=messaggio)
            await ctx.message.delete()
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return
    @editmsg.error
    async def editmsg_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!editmsg (idmsg) (testo)")

    @commands.command()#comando ban
    async def ban (self, ctx, member:discord.User, *, reason=None):
        
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, 
        cfg.rolea6, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            if member == None or member == ctx.message.author:
                await ctx.message.author.send("Non puoi bannarti da solo.")
                return
            if reason == None:
                reason = "Non definito"
            try:
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha bannato da {ctx.guild.name} motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="ban-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await member.send(embed=embed)
            except:
                pass

            await ctx.guild.ban(member, reason=reason)
            sanzioni = self.bot.get_channel(cfg.sanzioni) #canale sanzioni
            messagech = f"**{member} è stato bannato da {ctx.message.author.mention} motivo: `{reason}`**"
            embeds=discord.Embed(color=cfg.red)
            embeds.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            embeds.add_field(name="Admin", value=messagech, inline=True)
            embeds.set_footer(text=cfg.footer)
            await sanzioni.send(embed=embeds)
            
            
            #########log##########
            logchannel = self.bot.get_channel(cfg.log) #canale log
            embed=discord.Embed(color=cfg.red)
            embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="userlogs", value=f"**{member} è stato bannato da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
            embed.set_footer(text=cfg.footer)
            await logchannel.send(embed=embed)
            print(f"[LOG] {member} è stato bannato da {ctx.message.author.mention} motivo: `{reason}`")
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!ban (@tag/id) (motivo)")

    @commands.command()#comando kick
    async def kick (self, ctx, member:discord.User, *, reason=None):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, 
        cfg.rolea6, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            if member == None or member == ctx.message.author:
                try:
                    await ctx.message.author.send("Non puoi kickarti da solo.")
                except:
                    pass
                return
            if reason == None:
                reason = "Non definito"
            try:
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha kickato da {ctx.guild.name} motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.red)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="kick-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await member.send(embed=embed)
            except:
                pass
            await ctx.guild.kick(member)
            sanzioni = self.bot.get_channel(cfg.sanzioni) #canale sanzioni
            messagech = f"**{member} è stato kickato da {ctx.message.author.mention} motivo: `{reason}`**"
            embeds=discord.Embed(color=cfg.red)
            embeds.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            embeds.add_field(name="Admin", value=messagech, inline=True)
            embeds.set_footer(text=cfg.footer)
            await sanzioni.send(embed=embeds)
            #########log##########
            logchannel = self.bot.get_channel(cfg.log) #canale log
            embed=discord.Embed(color=cfg.red)
            embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="userlogs", value=f"**{member} è stato kickato da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
            embed.set_footer(text=cfg.footer)
            await logchannel.send(embed=embed)
            print(f"[LOG] {member} è stato kickato da {ctx.message.author.mention} motivo: `{reason}`")
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!kick (@tag/id) (motivo)")

    @commands.command()#comando tsay no embed
    async def tsay (self, ctx, *, text):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            await ctx.channel.send(text)
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return
    @tsay.error
    async def tsay_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!tsay (testo)")

    @commands.command()#comando tsayuser
    async def tuser (self, ctx, member:discord.User=None, *, text):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            try:
                await ctx.message.delete()
                embeds=discord.Embed(color=cfg.blue)
                embeds.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embeds.add_field(name="Admin Message", value=text, inline=True)
                embeds.set_footer(text=cfg.footer)
                await member.send(embed=embeds)
                ##MESSAGGIO DI VERIFICA AL AUTORE
                embedss=discord.Embed(color=cfg.blue)
                embedss.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embedss.add_field(name="Hai inviato questo messaggio a {0}#{1}".format(member.name, member.discriminator), value=text, inline=True)
                embedss.set_footer(text=cfg.footer)
                await ctx.message.author.send(embed=embedss)
                #########log##########
                logchannel = self.bot.get_channel(cfg.log) #canale log
                embedsss=discord.Embed(color=cfg.blue)
                embedsss.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embedsss.add_field(name="{0} ha inviato questo messaggio a {1}#{2}".format(ctx.message.author.name, member.name, member.discriminator), value=text, inline=True)
                embedsss.set_footer(text=cfg.footer)
                await logchannel.send(embed=embedsss)
            except:
                await ctx.channel.send("L'utente non riceve messaggi in DM.")
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return
    @tuser.error
    async def tuser_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!tuser (@tag/id) (testo)")

    @commands.command()
    async def find(self, ctx):
        
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            
            await ctx.message.delete()
            if len(ctx.message.raw_mentions) > 0:

                for user_id in ctx.message.raw_mentions:
                    member = utils.find(lambda m: m.id == user_id, ctx.guild.members)
                    if member.voice is not None:

                        invito = await member.voice.channel.create_invite(temporary=True)
                        reply = discord.Embed(description = f"L'utente {member.mention} si trova in **{member.voice.channel.name}**", colour = discord.Colour.from_rgb(3, 252, 94))
                        reply.add_field(name="Tasto per connettersi", value=f"[[Connettiti]({invito.url} 'Clicca qui per entrare nella stanza dell'utente')]", inline=True)

                        await ctx.send(content=ctx.message.author.mention, embed=reply)

                    else:
                        reply = discord.Embed(description = f"L'utente {member.mention} __non__ è collegato ad un canale vocale!", colour = discord.Colour.dark_red())

                        await ctx.send(content=ctx.message.author.mention, embed=reply)
    @find.error
    async def find_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!find (@tag/id)")

    @commands.command()
    @commands.bot_has_guild_permissions(deafen_members = True, mute_members = True)
    async def muteroom(self, ctx, *, channel=None):

        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            
            await ctx.message.delete()
            if channel is None:
                if ctx.message.author.voice is not None:
                    for member in ctx.message.author.voice.channel.members:
                        if member.id != ctx.message.author.id:
                            await member.edit(mute = True)
                    text = discord.Embed(title = f"🔇 • Channel Mute", description=f"Ho silenziato tutti gli utenti presenti in **{ctx.message.author.voice.channel.name}**", colour = discord.Colour.red())
                    await ctx.send(content = ctx.message.author.mention, embed=text)
                else:
                    text = discord.Embed(title = f"🔇 • Channel Mute - Errore", description=f"Non sei connesso a nessun canale vocale!\nPer utilizzare questo comando collegati al canale del quale vuoi mutare gli utenti o specifica il nome del canale di cui vuoi silenziare i membri.", colour = discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content = ctx.message.author.mention, embed=text)

            elif channel is not None:
                found = False
                for guild_channel in ctx.guild.voice_channels:
                    if channel.lower() in guild_channel.name.lower():
                        found = True
                        if len(guild_channel.members) > 0:
                            for member in guild_channel.members:
                                if member.id != ctx.message.author.id:
                                    await member.edit(mute=True)
                            text = discord.Embed(title = f"🔇 Channel Mute", description=f"Ho silenziato tutti gli utenti presenti in **{guild_channel.name}**", colour = discord.Colour.red())
                            await ctx.send(content = ctx.message.author.mention, embed=text)
                        else:
                            text = discord.Embed(title = f"🔇 Channel Mute - Errore", description=f"La stanza **{guild_channel.name}** non ha utenti connessi!", colour = discord.Colour.from_rgb(252, 32, 3))
                            await ctx.send(content = ctx.message.author.mention, embed=text)
                        break
                if found == False:
                    text = discord.Embed(title = f"🔇 Channel Mute - Errore", description=f"Non sono riuscito a trovare la stanza che hai specificato!\n{ctx.message.author.mention} prova a spiegarti meglio ;)", colour = discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content = ctx.message.author.mention, embed=text)
    @muteroom.error
    async def muteroom_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!muteroom (nome stanza)")

    @commands.command()
    @commands.bot_has_guild_permissions(deafen_members = True, mute_members = True)
    async def unmuteroom(self, ctx, *, channel=None):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            
            await ctx.message.delete()
            if channel is None:
                if ctx.message.author.voice is not None:
                    for member in ctx.message.author.voice.channel.members:
                        if member.id != ctx.message.author.id:
                            await member.edit(mute = False)
                    text = discord.Embed(title = f"🔈 • Channel Unmute", description=f"Ho smutato tutti gli utenti presenti in **{ctx.message.author.voice.channel.name}**", colour = discord.Colour.green())
                    await ctx.send(content = ctx.message.author.mention, embed=text)
                else:
                    text = discord.Embed(title = f"🔈 • Channel Unmute - Errore", description=f"Non sei connesso a nessun canale vocale!\nPer utilizzare questo comando collegati al canale del quale vuoi smutare gli utenti o specifica il nome del canale di cui vuoi smutare i membri.", colour = discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content = ctx.message.author.mention, embed=text)

            elif channel is not None:
                found = False
                for guild_channel in ctx.guild.voice_channels:
                    if channel.lower() in guild_channel.name.lower():
                        found = True
                        if len(guild_channel.members) > 0:
                            for member in guild_channel.members:
                                if member.id != ctx.message.author.id:
                                    await member.edit(mute=False)
                            text = discord.Embed(title = f"🔈 Channel Unmute", description=f"Ho smutato tutti gli utenti presenti in **{guild_channel.name}**", colour = discord.Colour.green())
                            await ctx.send(content = ctx.message.author.mention, embed=text)
                        else:
                            text = discord.Embed(title = f"🔈 Channel Unmute - Errore", description=f"La stanza **{guild_channel.name}** non ha utenti connessi!", colour = discord.Colour.from_rgb(252, 32, 3))
                            await ctx.send(content = ctx.message.author.mention, embed=text)
                        break
                if found == False:
                    text = discord.Embed(title = f"🔈 Channel Unmute - Errore", description=f"Non sono riuscito a trovare la stanza che hai specificato!\n{ctx.message.author.mention} prova a spiegarti meglio ;)", colour = discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content = ctx.message.author.mention, embed=text)
    @unmuteroom.error
    async def unmuteroom_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!unmuteroom (nome stanza)")

def setup(bot):
    bot.add_cog(cmd(bot))
    print("[!] modulo cmd caricato")
