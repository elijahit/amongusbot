from discord.message import Embed
from discord.ext import commands
from discord import Color
import discord
import random


class cmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



#CMD utente

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
                 "*Developers*: **Elijah**, **Nico**, **ImNotName**, **iTzSgrullee_**, **MyNameIsDark01**\n\
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
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            messageesports_embed=discord.Embed(color=cfg.red)
            messageesports_embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            messageesports_embed.add_field(name="-> Comandi admin", value=cfg.aiutoadmin, inline=True)
            messageesports_embed.set_footer(text=cfg.footer)

            await ctx.channel.send(embed=messageesports_embed)
            #########log##########
            logchannel = self.bot.get_channel(cfg.log) #canale log
            embed=discord.Embed(color=cfg.lightgreen)
            embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="userlogs", value="**{0} ha usato il comando `!acmds`**".format(ctx.message.author.mention), inline=True)
            embed.set_footer(text=cfg.footer)
            await logchannel.send(embed=embed)
            print("[LOG] {0}#{1} ha usato il comando !acmds".format(ctx.message.author.name, ctx.message.author.discriminator))
            return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando purge
    async def purge(self, ctx, ammount = int(1)):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            if ammount <= 200:
                await ctx.channel.purge(limit=ammount)
                ##log
                member = ctx.message.author
                logchannel = self.bot.get_channel(cfg.log) #canale log
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
                embed.add_field(name="userlogs", value="**{0} ha cancellato {1} messaggi dal canale {2}**".format(member.mention, ammount, ctx.channel.mention), inline=True)
                embed.set_footer(text=cfg.footer)
                await logchannel.send(embed=embed)
                return
            else:
                await ctx.message.author.send("Limite di messaggi da eliminare `200`.")
                await ctx.message.delete()
                return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando richiesta
    async def richiesta(self, ctx, stato, *, text):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            ##log
            member = ctx.message.author
            logchannel = self.bot.get_channel(758390987168677941)
            embed=discord.Embed(color=cfg.lightgreen)
            embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
            embed.add_field(name="RICHIESTA: {}".format(stato), value="{}".format(text), inline=True)
            embed.set_footer(text="N° {}".format((random.randint(100000, 9000000))))
            await logchannel.send(embed=embed)
            return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando lista ban
    async def banlist(self, ctx):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
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
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando add reaction
    async def addreact(self, ctx, messageid, emoij):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            message = await ctx.channel.fetch_message(messageid)
            await message.add_reaction(emoij)
            return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return
    @commands.command()#comando rteam
    async def editmsg (self, ctx, id, *, messaggio):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles]:
            try:
                message = await ctx.channel.fetch_message(id)
            except discord.NotFound as e:
                await commands.send("Messaggio non trovato")
                raise e
            await message.edit(content=messaggio)
            await ctx.message.delete()

    @commands.command()#comando rteam
    async def rteam (self, ctx, user:discord.Member=None, *, reason=None):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles]:
            #if user == None or user == ctx.message.author:
            #    await ctx.message.author.send("Non puoi kickarti da solo dal team.")
            #    return
            if reason == None:
                reason = "Non definito"
            guild = discord.utils.get(commands.guilds)
            if 701844028521447556 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=701844028521447556))#coach
            if 701593541410947083 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=701593541410947083))#senior
            if 703325756536651806 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=703325756536651806))#esports
            if 706818123759878184 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=706818123759878184))#esports2
            if 705782556896788522 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=705782556896788522))#leadercomp
            if 702191255504814162 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=702191255504814162))#comp
            if 704812555134173283 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=704812555134173283))#accademyleader
            if 704782635209326646 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=704782635209326646))#accademy
            if 705164932433576026 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=705164932433576026))#juniorleader
            if 705164776938012823 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=705164776938012823))#junior
            if 701593626245071019 in [role.id for role in user.roles]:
                await user.remove_roles(discord.utils.get(guild.roles, id=701593626245071019))#defaultrole
                await user.add_roles(discord.utils.get(guild.roles, id=703771340301271053))#defaultrole
                await ctx.message.delete()
                sanzioni = self.bot.get_channel(cfg.sanzioni) #canale sanzioni
                messagech = f"**{user} è stato rimosso dal team da {ctx.message.author.mention} motivo: `{reason}`**"
                embeds=discord.Embed(color=cfg.red)
                embeds.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embeds.add_field(name="Admin", value=messagech, inline=True)
                embeds.set_footer(text=cfg.footer)
                await sanzioni.send(embed=embeds)
                #########log##########
                logchannel = self.bot.get_channel(cfg.log) #canale log
                embed=discord.Embed(color=cfg.red)
                embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="userlogs", value=f"**{user} è stato rimosso dal team da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
                embed.set_footer(text=cfg.footer)
                await logchannel.send(embed=embed)
                print(f"[LOG] {user} è stato rimosso dal team da {ctx.message.author.mention} motivo: `{reason}`")
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha rimosso dal team {ctx.guild.name} motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.red)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="team-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await user.send(embed=embed)
                await user.edit(nick=user.name)
                return
            else:
                await ctx.message.delete()
                await ctx.message.author.send("Questo membro non fa parte del team.")
                return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()
    async def warn(self, ctx, user:discord.Member=None, *, reason=None):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('db')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            if user == None or user == ctx.message.author:
                await ctx.message.author.send("Non puoi warnarti da solo.")
                return
            if reason == None:
                reason = "Non definito"
            if not (discord.utils.get(user.roles, name="Warn 1")) and not (discord.utils.get(user.roles, name="Warn 2")) and not (discord.utils.get(user.roles, name="Warn 3")):
                db.Database.execute("INSERT INTO warns (ID, Name, Livello, Motivo, Data) VALUES (?, ?, ?, ?, ?)", (user.id, user.name, 1, reason, 1))
                db.Database.commit()
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha warnato per la prima volta da {ctx.guild.name} motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="ban-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await user.send(embed=embed)
                #########log##########
                sanzioni = self.bot.get_channel(cfg.sanzioni) #canale log
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="userlogs", value=f"**{user} è stato warnato(1) da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
                embed.set_footer(text=cfg.footer)
                await sanzioni.send(embed=embed)
                print(f"[LOG] {user} è stato warnato(1) da {ctx.message.author.mention} motivo: `{reason}`")
                return
            if (discord.utils.get(user.roles, name="Warn 1")) and not (discord.utils.get(user.roles, name="Warn 2")) and not (discord.utils.get(user.roles, name="Warn 3")):
                await user.add_roles(discord.utils.get(self, ctx.guild.roles, name="Warn 2"))
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha warnato per la seconda volta da {ctx.guild.name} motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="ban-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await user.send(embed=embed)
                #########log##########
                sanzioni = self.bot.get_channel(cfg.sanzioni) #canale log
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="userlogs", value=f"**{user} è stato warnato(2) da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
                embed.set_footer(text=cfg.footer)
                await sanzioni.send(embed=embed)
                print(f"[LOG] {user} è stato warnato(2) da {ctx.message.author.mention} motivo: `{reason}`")
                return
            if (discord.utils.get(user.roles, name="Warn 1")) and (discord.utils.get(user.roles, name="Warn 2")) and not (discord.utils.get(user.roles, name="Warn 3")):
                await user.add_roles(discord.utils.get(self, ctx.guild.roles, name="Warn 3"))
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha warnato per la terza volta da {ctx.guild.name} motivo:** `{reason}`\n\
                **Sei già al terzo WARN, in caso di un successivo warning verrai automaticamente bannato dal server.**"
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="ban-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await user.send(embed=embed)
                #########log##########
                sanzioni = self.bot.get_channel(cfg.sanzioni) #canale log
                embed=discord.Embed(color=cfg.lightgreen)
                embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="userlogs", value=f"**{user} è stato warnato(3) da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
                embed.set_footer(text=cfg.footer)
                await sanzioni.send(embed=embed)
                print(f"[LOG] {user} è stato warnato(3) da {ctx.message.author.mention} motivo: `{reason}`")
                return
            if (discord.utils.get(user.roles, name="Warn 1")) and (discord.utils.get(user.roles, name="Warn 2")) and (discord.utils.get(user.roles, name="Warn 3")):
                message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha warnato per la quarta volta da {ctx.guild.name} di conseguenza sei stato bannato motivo:** `{reason}`"
                embed=discord.Embed(color=cfg.red)
                embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                embed.add_field(name="ban-logs", value=message, inline=True)
                embed.set_footer(text=cfg.footer)
                await user.send(embed=embed)
                #########log##########
                sanzioni = self.bot.get_channel(cfg.sanzioni) #canale log
                embed=discord.Embed(color=cfg.red)
                embed.set_author(name="{0}#{1}".format(ctx.message.author.name, ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="userlogs", value=f"**{user} è stato warnato(4) e bannato da {ctx.message.author.mention} motivo: `{reason}`**", inline=True)
                embed.set_footer(text=cfg.footer)
                await sanzioni.send(embed=embed)
                print(f"[LOG] {user} è stato warnato(4) e bannato da {ctx.message.author.mention} motivo: `{reason}`")
                await ctx.guild.ban(user, reason="Limite warn (Controlla sanzioni)")
                return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando ban
    async def ban (self, ctx, member:discord.User=None, *, reason=None):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            if member == None or member == ctx.message.author:
                await ctx.message.author.send("Non puoi bannarti da solo.")
                return
            if reason == None:
                reason = "Non definito"
            message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha bannato da {ctx.guild.name} motivo:** `{reason}`"
            embed=discord.Embed(color=cfg.lightgreen)
            embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            embed.add_field(name="ban-logs", value=message, inline=True)
            embed.set_footer(text=cfg.footer)
            await member.send(embed=embed)
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
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando kick
    async def kick (self, ctx, member:discord.User=None, *, reason=None):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            if member == None or member == ctx.message.author:
                await ctx.message.author.send("Non puoi kickarti da solo.")
                return
            if reason == None:
                reason = "Non definito"
            message = f"**{ctx.message.author.name}#{ctx.message.author.discriminator} ti ha kickato da {ctx.guild.name} motivo:** `{reason}`"
            embed=discord.Embed(color=cfg.red)
            embed.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            embed.add_field(name="kick-logs", value=message, inline=True)
            embed.set_footer(text=cfg.footer)
            await member.send(embed=embed)
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
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return


    @commands.command()#comando tsay
    async def t (self, ctx, title, *, text):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            embeds=discord.Embed(color=cfg.blue)
            embeds.set_author(name="{0}".format(ctx.guild.name), icon_url=ctx.guild.icon_url)
            embeds.add_field(name=title, value=text, inline=True)
            embeds.set_footer(text=cfg.footer)
            await ctx.channel.send(embed=embeds)
            return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando tsay no embed
    async def tsay (self, ctx, *, text):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()
            await ctx.channel.send(text)
            return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return

    @commands.command()#comando tsayuser
    async def tuser (self, ctx, member:discord.User=None, *, text):
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]:
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
            return
        else:
            await ctx.message.delete()
            await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            return




def setup(bot):
    bot.add_cog(cmd(bot))
    print("[!] modulo cmd caricato")
