from discord.message import Embed
from discord.ext import commands
from discord import Color
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
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
            await ctx.message.delete()

            name = "> Comandi admin"
            field = ("**[1]** Owner **|** **[2]** Amministratore **|** **[3]** Mod **|** **[4]** Helper **|** **[5]** Gestore **|** **[6]** Support", cfg.aiutoadmin)

            acmds_embed = embed.get_standard_embed(name,
                                               cfg.blue,
                                               ctx.guild.icon_url,
                                               [field],
                                               cfg.footer)

            await ctx.channel.send(embed=acmds_embed)
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
        embed = self.bot.get_cog('Embeds')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
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
                await ctx.channel.send("Messaggio non trovato")
                raise e
            await message.edit(content=messaggio)
            await ctx.message.delete()

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
    async def t (self, ctx, *tutto): #!t "titolo molto utile" descrizione utile
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles]:
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
