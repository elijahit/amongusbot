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

            name = "[1] Owner | [2] Amministratore | [3] Mod | [4] Helper | [5] Gestore | [6] Support"
            field = ("Administrative Command", cfg.aiutoadmin)
            field2 = ("Moderative Command", cfg.aiutoadmin2)

            acmds_embed = embed.get_standard_embed(name,
                                               cfg.blue,
                                               ctx.guild.icon_url,
                                               [field, field2],
                                               cfg.footer)

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
        admin_roles = cfg.rolea_all

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

    @commands.command()#comando richiesta
    async def richiesta(self, ctx, stato, *, text):
        cfg = self.bot.get_cog('Config')
        embed = self.bot.get_cog('Embeds')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            ##log
            member = ctx.message.author
            logchannel = self.bot.get_channel(758390987168677941)

            name = "{0}#{1}".format(member.name, member.discriminator)
            field = ("RICHIESTA: {}".format(stato), "{}".format(text))

            request_embed = embed.get_standard_embed(name,
                                               cfg.green,
                                               member.avatar_url,
                                               [field],
                                               "N° {}".format((random.randint(100000, 9000000))))
                                               
            await logchannel.send(embed=request_embed)
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @commands.command()#comando lista ban
    async def banlist(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            member = ctx.message.author
            bans = await ctx.guild.bans()
            pretty_list = ["• {0.id} ({0.name}#{0.discriminator})".format(entry.user) for entry in bans]
            embed=discord.Embed(color=cfg.lightgreen)
            embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
            embed.add_field(name="Lista ban", value="{}".format("\n".join(pretty_list)), inline=True)
            embed.set_footer(text=cfg.footer)
            await ctx.send(embed=embed)
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @commands.command()#comando add reaction
    async def addreact(self, ctx, messageid, emoij):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2))

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
    
    @commands.command()#comando editmsg
    async def editmsg (self, ctx, id, *, messaggio):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3))

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

    @commands.command()#comando ban
    async def ban (self, ctx, member:discord.User=None, *, reason=None):
        
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            if member == None or member == ctx.message.author:
                await ctx.message.author.send("Non puoi bannarti da solo.")
                return
            if reason == None:
                reason = "Non definito"
            try:
                await ctx.guild.ban(member, reason=reason)
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha bannato da {ctx.guild.name} motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="ban-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await member.send(embed=embed)
            except:
                pass
            
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

    @commands.command()#comando kick
    async def kick (self, ctx, member:discord.User=None, *, reason=None):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

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

    @commands.command()#comando tsay
    async def t (self, ctx, *tutto): #!t "titolo molto utile" descrizione utile
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top5

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            text = ""
            tutto = str(tutto)
            tutto = tutto.split()

            for x in tutto:
                if x.startswith("\""):
                    for y in tutto:
                     text += y
                     tutto.pop(-1)
                     if y.endswith("\""):
                         break

            title = text[0]
            text = " ".join(tutto)
            " ".join(tutto)

            embeds=discord.Embed(color=cfg.blue)
            embeds.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            embeds.add_field(name=title, value=text, inline=True)
            embeds.set_footer(text=cfg.footer)
            await ctx.channel.send(embed=embeds)
            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @commands.command()#comando tsay no embed
    async def tsay (self, ctx, *, text):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top5

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

    @commands.command()#comando tsayuser
    async def tuser (self, ctx, member:discord.User=None, *, text):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2))

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

                        invito = await member.voice.channel.create_invite()
                        reply = discord.Embed(description = f"L'utente {member.mention} si trova in **{member.voice.channel.name}**", colour = discord.Colour.from_rgb(3, 252, 94))
                        reply.add_field(name="Tasto per connettersi", value=f"[[Connettiti]({invito.url} 'Clicca qui per entrare nella stanza dell'utente')]", inline=True)

                        await ctx.send(content=ctx.message.author.mention, embed=reply)

                    else:
                        reply = discord.Embed(description = f"L'utente {member.mention} __non__ è collegato ad un canale vocale!", colour = discord.Colour.dark_red())

                        await ctx.send(content=ctx.message.author.mention, embed=reply)

    @commands.command()
    @commands.bot_has_guild_permissions(deafen_members = True, mute_members = True)
    async def muteroom(self, ctx, *, channel=None):

        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

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

    @commands.command()
    @commands.bot_has_guild_permissions(deafen_members = True, mute_members = True)
    async def unmuteroom(self, ctx, *, channel=None):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

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

def setup(bot):
    bot.add_cog(cmd(bot))
    print("[!] modulo cmd caricato")
