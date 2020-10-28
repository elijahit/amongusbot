import discord
from discord import utils
from discord.ext import commands


class Cmd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # CMD utente

    @commands.command()
    async def ping(self, ctx):

        await ctx.message.delete()
        await ctx.send(f"Ping! In {round(self.bot.latency * 1000)}ms")

    @commands.command()  # about
    async def about(self, ctx):

        await ctx.message.delete()
        cfg = self.bot.get_cog('Config')
        embed = self.bot.get_cog('Embeds')

        name = "About - Among Us Ita BOT"
        field = ("About 3rd Party Developers",
                 "**Among Us Ita BOT**\n"
                 "Questo BOT è stato creato e programmato in python da un team di 6+ developer per amongusita.it, sono stati richiesti \
                 mesi di programmazione per rendere lo stesso adeguato all'utenza attualmente dentro Among Us Ita.\
                 Il bot viene utilizato per gestire l'intera community di Among Us Ita, ciò che in altre community viene fatto con 7 bot diversi.\n"
                 "*Developers*: **Elijah**, **Nico**, **EazY**, **ImNotName**, **iTzSgrullee_**, **MyNameIsDark01**, **Kappa**\n\
                 Librerie utilizzate: *DiscordPy*\n\
                 \n© amongusita.it")

        about_embed = embed.get_standard_embed(name,
                                               cfg.green,
                                               ctx.guild.icon_url,
                                               [field],
                                               cfg.footer)
        await ctx.channel.send(embed=about_embed)

        return

    # ADMIN COMMAND

    @commands.command()  # CMD AIUTO ADMIN
    async def acmds(self, ctx):
        cfg = self.bot.get_cog('Config')
        embed = self.bot.get_cog('Embeds')

        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            name = "COMANDI ADMIN - [!]"
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

    @commands.command()  # comando purge
    async def purge(self, ctx, ammount=int(1)):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.roledev}

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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !purge (valore max 200)")

    @commands.command()  # addrole
    async def addrole(self, ctx, role: discord.Role, member: discord.Member = None, *, motivo=None):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        embed = self.bot.get_cog('Embeds')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea6, cfg.rolea7, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            roleadd = None
            try:
                query = "SELECT * FROM addrole WHERE role_id=?"
                values = (role.id,)
                roleadd = db.fetchall(query, values)[0][1]
            except:
                await ctx.message.delete()

                name = "Amministratore ruoli"
                field = (
                    "Errore", f"Il ruolo {role.mention} non è presente nella lista di gestione.")

                role_embed = embed.get_standard_embed(name,
                                                      cfg.red,
                                                      ctx.guild.icon_url,
                                                      [field],
                                                      cfg.footer)

                await ctx.channel.send(embed=role_embed)

            if role.id == roleadd:

                rolecheck = discord.utils.find(
                    lambda r: r.id == role.id, ctx.guild.roles)
                if rolecheck in member.roles:

                    await ctx.message.delete()

                    name = "Amministratore ruoli"
                    field = (
                        "Errore", f"L'utente {member.mention} possiede già il ruolo {role.mention}.")

                    role_embed = embed.get_standard_embed(name,
                                                          cfg.red,
                                                          ctx.guild.icon_url,
                                                          [field],
                                                          cfg.footer)

                    await ctx.channel.send(embed=role_embed)

                else:
                    await ctx.message.delete()
                    staff = self.bot.get_channel(
                        cfg.staffroom)  # canale sanzioni

                    name = "Amministratore ruoli"
                    field = (
                        "Aggiunto",
                        f"Hai inserito il ruolo {role.mention} al utente {member.mention} motivo: `{motivo}`.")

                    role_embed = embed.get_standard_embed(name,
                                                          cfg.blue,
                                                          ctx.guild.icon_url,
                                                          [field],
                                                          cfg.footer)

                    await ctx.channel.send(embed=role_embed)

                    name = "user-logs"
                    field = (
                        "Aggiunto",
                        f"{ctx.author.mention} ha inserito il ruolo {role.mention} al utente {member.mention} motivo: `{motivo}`.")

                    logs_embed = embed.get_standard_embed(name,
                                                          cfg.green,
                                                          ctx.guild.icon_url,
                                                          [field],
                                                          cfg.footer)

                    await staff.send(embed=logs_embed)
                    await member.add_roles(role)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !addrole (@ruolo) (@utente) (motivo)")

    @commands.command()  # updatedb
    async def updatedb(self, ctx, table, colunm, where1, where2, *value):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.roledev}

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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.send("[!] USA: !updatedb (tabella) (colonna) (field) (contenuto) valore")
            await ctx.send("ES: !updatedb config testo titolo welcomedm testo valore")

    @commands.command()  # comando add reaction
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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !addreact (idmsg) (emoij)")

    @commands.command()  # comando editmsg
    async def editmsg(self, ctx, id, *, messaggio):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.roledev}

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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !editmsg (idmsg) (testo)")

    @commands.command()  # comando ban
    async def ban(self, ctx, member: discord.User, *, reason=None):

        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            if member is None or member == ctx.message.author:
                await ctx.message.author.send("Non puoi bannarti da solo.")
                return
            if reason is None:
                reason = "Non definito"
            try:
                embed = discord.Embed(
                    title="⛔️ • Ban", description=f"{ctx.message.author.mention} ti ha bannato")
                embed.add_field(
                    name="Staffer", value=ctx.message.author, inline=True)
                embed.add_field(name="Utente bannato",
                                value=member, inline=True)

                embed.add_field(name="Motivazione", value=reason, inline=True)
                await member.send(embed=embed)
            except:
                pass

            await ctx.guild.ban(member, reason=reason)
            sanzioni = self.bot.get_channel(cfg.sanzioni)  # canale sanzioni
            embeds = discord.Embed(
                title="⛔️ • Ban", description=f"{ctx.message.author.mention} ha bannato {member.mention}")
            embeds.add_field(name="Lo Staffer",
                             value=ctx.message.author, inline=True)
            embeds.add_field(name="Ha bannato", value=member, inline=True)

            embeds.add_field(name="Motivazione", value=reason, inline=True)
            await sanzioni.send(embed=embeds)

            conn = self.bot.get_cog("Db")
            try:
                for g in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (ctx.message.author.id,)):
                    if g[4] is None:
                        conn.execute(
                            "UPDATE analytics SET ban = 1 WHERE admin_id = ?", (ctx.message.author.id,))
                    else:
                        conn.execute(
                            "UPDATE analytics SET ban = ban+1 WHERE admin_id = ?", (ctx.message.author.id,))
            except:
                print("errore")

            try:
                d = conn.fetchall(
                    'SELECT * FROM analytics WHERE admin_id = ?', (ctx.message.author.id,))
                if len(d) == 0:
                    conn.execute(
                        "INSERT INTO analytics (admin_id, ban) VALUES (?, ?)", (ctx.message.author.id, 1,))
            except:
                print("error2")

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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !ban (@tag/Name#0000) (motivo)")

    @commands.command()  # comando ban
    async def unban(self, ctx, member, *, reason=None):

        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            if member is None or member == ctx.message.author:
                await ctx.message.author.send("Non puoi sbannarti da solo.")
                return
            if reason is None:
                reason = "Non definito"
            try:
                embed = discord.Embed(
                    title="✅ • Unban", description=f"{ctx.message.author.mention} ti ha sbannato")
                embed.add_field(name="Lo Staffer",
                                value=ctx.message.author, inline=True)
                embed.add_field(name="Utente sbannato",
                                value=member, inline=True)

                await member.send(embed=embed)
            except:
                pass

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):

                    await ctx.guild.unban(user, reason=reason)
                    sanzioni = self.bot.get_channel(
                        cfg.sanzioni)  # canale sanzioni
                    embeds = discord.Embed(
                        title="✅ • Unban", description=f"{ctx.message.author.mention} ha sbannato")
                    embeds.add_field(name="Lo Staffer",
                                     value=ctx.message.author, inline=True)
                    embeds.add_field(name="Utente sbannato",
                                     value=member, inline=True)

                    embeds.add_field(name="Motivazione",
                                     value=reason, inline=True)
                    await sanzioni.send(embed=embeds)

                    conn = self.bot.get_cog("Db")
                    try:
                        for g in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (ctx.message.author.id,)):
                            if g[6] is None:
                                conn.execute(
                                    "UPDATE analytics SET unban = 1 WHERE admin_id = ?", (ctx.message.author.id,))
                            else:
                                conn.execute(
                                    "UPDATE analytics SET unban = unban+1 WHERE admin_id = ?", (ctx.message.author.id,))
                    except:
                        print("errore")

                    try:
                        d = conn.fetchall(
                            'SELECT * FROM analytics WHERE admin_id = ?', (ctx.message.author.id,))
                        if len(d) == 0:
                            conn.execute(
                                "INSERT INTO analytics (admin_id, unban) VALUES (?, ?)", (ctx.message.author.id, 1,))
                    except:
                        print("error2")

                    return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !unban (Nome#0000) (motivo)")

    @commands.command()  # comando kick
    async def kick(self, ctx, member: discord.User, *, reason=None):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            if member is None or member == ctx.message.author:
                try:
                    await ctx.message.author.send("Non puoi kickarti da solo.")
                except:
                    pass
                return
            if reason is None:
                reason = "Non definito"
            try:
                embed = discord.Embed(
                    title="⛔️ • Kick", description=f"{ctx.message.author.mention}  ti ha kickato dal server")
                embed.add_field(name="Lo Staffer",
                                value=ctx.message.author, inline=True)
                embed.add_field(name="Ha Kickato", value=member, inline=True)

                embed.add_field(name="Motivazione", value=reason, inline=True)
                await member.send(embed=embed)
            except:
                pass
            conn = self.bot.get_cog("Db")
            try:
                for g in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (ctx.message.author.id,)):
                    if g[8] is None:
                        conn.execute(
                            "UPDATE analytics SET kick = 1 WHERE admin_id = ?", (ctx.message.author.id,))
                    else:
                        conn.execute(
                            "UPDATE analytics SET kick = kick+1 WHERE admin_id = ?", (ctx.message.author.id,))
            except:
                pass

            try:
                d = conn.fetchall(
                    'SELECT * FROM analytics WHERE admin_id = ?', (ctx.message.author.id,))
                if len(d) == 0:
                    conn.execute(
                        "INSERT INTO analytics (admin_id, kick) VALUES (?, ?)", (ctx.message.author.id, 1,))
            except:
                pass

            await ctx.guild.kick(member)
            sanzioni = self.bot.get_channel(cfg.sanzioni)  # canale sanzioni
            embeds = discord.Embed(
                title="⛔️ • Kick", description=f"{ctx.message.author.mention} ha kickato {member.mention}")
            embeds.add_field(name="Lo Staffer",
                             value=ctx.message.author, inline=True)
            embeds.add_field(name="Ha Kickato", value=member, inline=True)

            embeds.add_field(name="Motivazione", value=reason, inline=True)
            await sanzioni.send(embed=embeds)

        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !kick (@tag/id) (motivo)")

    @commands.command()  # comando tsay no embed
    async def tsay(self, ctx, *, text):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.roledev}

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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !tsay (testo)")

    @commands.command()  # comando tsayuser
    async def tuser(self, ctx, member: discord.User = None, *, text):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            try:
                await ctx.message.delete()
                embeds = discord.Embed(color=cfg.blue)
                embeds.set_author(name="{0}".format(
                    ctx.guild.name), icon_url=ctx.guild.icon_url)
                embeds.add_field(name="Admin Message", value=text, inline=True)
                embeds.set_footer(text=cfg.footer)
                await member.send(embed=embeds)
                # MESSAGGIO DI VERIFICA AL AUTORE
                embedss = discord.Embed(color=cfg.blue)
                embedss.set_author(name="{0}".format(
                    ctx.guild.name), icon_url=ctx.guild.icon_url)
                embedss.add_field(name="Hai inviato questo messaggio a {0}#{1}".format(
                    member.name, member.discriminator), value=text, inline=True)
                embedss.set_footer(text=cfg.footer)
                await ctx.message.author.send(embed=embedss)
                # LOG
                logchannel = self.bot.get_channel(cfg.log)  # canale log
                embedsss = discord.Embed(color=cfg.blue)
                embedsss.set_author(name="{0}".format(
                    ctx.guild.name), icon_url=ctx.guild.icon_url)
                embedsss.add_field(name="{0} ha inviato questo messaggio a {1}#{2}".format(
                    ctx.message.author.name, member.name, member.discriminator), value=text, inline=True)
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
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !tuser (@tag/id) (testo)")

    @commands.command()
    async def find(self, ctx):

        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:

            await ctx.message.delete()
            if len(ctx.message.raw_mentions) > 0:

                for user_id in ctx.message.raw_mentions:
                    member = utils.find(
                        lambda m: m.id == user_id, ctx.guild.members)
                    if member.voice is not None:

                        invito = await member.voice.channel.create_invite(temporary=True)
                        reply = discord.Embed(
                            description=f"L'utente {member.mention} si trova in **{member.voice.channel.name}**",
                            colour=discord.Colour.from_rgb(3, 252, 94))
                        reply.add_field(
                            name="Tasto per connettersi",
                            value=f"[[Connettiti]({invito.url} 'Clicca qui per entrare nella stanza dell'utente')]",
                            inline=True)

                        await ctx.send(content=ctx.message.author.mention, embed=reply)

                    else:
                        reply = discord.Embed(
                            description=f"L'utente {member.mention} __non__ è collegato ad un canale vocale!",
                            colour=discord.Colour.dark_red())

                        await ctx.send(content=ctx.message.author.mention, embed=reply)

    @find.error
    async def find_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !find (@tag/id)")

    @commands.command()
    @commands.bot_has_guild_permissions(deafen_members=True, mute_members=True)
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
                            await member.edit(mute=True)
                    text = discord.Embed(
                        title=f"🔇 • Channel Mute",
                        description=f"Ho silenziato tutti gli utenti presenti in **{ctx.message.author.voice.channel.name}**",
                        colour=discord.Colour.red())
                    await ctx.send(content=ctx.message.author.mention, embed=text)
                else:
                    text = discord.Embed(title=f"🔇 • Channel Mute - Errore",
                                         description=f"Non sei connesso a nessun canale vocale!\nPer utilizzare questo comando collegati al canale del quale vuoi mutare gli utenti o specifica il nome del canale di cui vuoi silenziare i membri.",
                                         colour=discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content=ctx.message.author.mention, embed=text)

            elif channel is not None:
                found = False
                for guild_channel in ctx.guild.voice_channels:
                    if channel.lower() in guild_channel.name.lower():
                        found = True
                        if len(guild_channel.members) > 0:
                            for member in guild_channel.members:
                                if member.id != ctx.message.author.id:
                                    await member.edit(mute=True)
                            text = discord.Embed(
                                title=f"🔇 Channel Mute",
                                description=f"Ho silenziato tutti gli utenti presenti in **{guild_channel.name}**",
                                colour=discord.Colour.red())
                            await ctx.send(content=ctx.message.author.mention, embed=text)
                        else:
                            text = discord.Embed(
                                title=f"🔇 Channel Mute - Errore",
                                description=f"La stanza **{guild_channel.name}** non ha utenti connessi!",
                                colour=discord.Colour.from_rgb(252, 32, 3))
                            await ctx.send(content=ctx.message.author.mention, embed=text)
                        break
                if found is False:
                    text = discord.Embed(title=f"🔇 Channel Mute - Errore",
                                         description=f"Non sono riuscito a trovare la stanza che hai specificato!\n{ctx.message.author.mention} prova a spiegarti meglio ;)",
                                         colour=discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content=ctx.message.author.mention, embed=text)

    @muteroom.error
    async def muteroom_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !muteroom (nome stanza)")

    @commands.command()
    @commands.bot_has_guild_permissions(deafen_members=True, mute_members=True)
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
                            await member.edit(mute=False)
                    text = discord.Embed(
                        title=f"🔈 • Channel Unmute",
                        description=f"Ho smutato tutti gli utenti presenti in **{ctx.message.author.voice.channel.name}**",
                        colour=discord.Colour.green())
                    await ctx.send(content=ctx.message.author.mention, embed=text)
                else:
                    text = discord.Embed(title=f"🔈 • Channel Unmute - Errore",
                                         description=f"Non sei connesso a nessun canale vocale!\nPer utilizzare questo comando collegati al canale del quale vuoi smutare gli utenti o specifica il nome del canale di cui vuoi smutare i membri.",
                                         colour=discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content=ctx.message.author.mention, embed=text)

            elif channel is not None:
                found = False
                for guild_channel in ctx.guild.voice_channels:
                    if channel.lower() in guild_channel.name.lower():
                        found = True
                        if len(guild_channel.members) > 0:
                            for member in guild_channel.members:
                                if member.id != ctx.message.author.id:
                                    await member.edit(mute=False)
                            text = discord.Embed(
                                title=f"🔈 Channel Unmute",
                                description=f"Ho smutato tutti gli utenti presenti in **{guild_channel.name}**",
                                colour=discord.Colour.green())
                            await ctx.send(content=ctx.message.author.mention, embed=text)
                        else:
                            text = discord.Embed(
                                title=f"🔈 Channel Unmute - Errore",
                                description=f"La stanza **{guild_channel.name}** non ha utenti connessi!",
                                colour=discord.Colour.from_rgb(252, 32, 3))
                            await ctx.send(content=ctx.message.author.mention, embed=text)
                        break
                if found is False:
                    text = discord.Embed(title=f"🔈 Channel Unmute - Errore",
                                         description=f"Non sono riuscito a trovare la stanza che hai specificato!\n{ctx.message.author.mention} prova a spiegarti meglio ;)",
                                         colour=discord.Colour.from_rgb(252, 32, 3))
                    await ctx.send(content=ctx.message.author.mention, embed=text)

    @unmuteroom.error
    async def unmuteroom_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !unmuteroom (nome stanza)")

    @commands.command()  # comando tsay no embed
    async def analytics(self, ctx, user: discord.Member):
        cfg = self.bot.get_cog('Config')
        embed = self.bot.get_cog('Embeds')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.rolea7, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            conn = self.bot.get_cog('Db')

            try:
                for x in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user.id,)):
                    field = (f"Statistiche", f"*Ticket*: {x[2]}\n\
*Hack*: {x[3]}\n\
*Ban*: {x[4]}\n\
*Note*: {x[5]}\n\
*Sban*: {x[6]}\n\
*Warn*: {x[8]}\n\
*Kick*: {x[7]}")
                    field2 = (f"Amministratore", f"**{user.mention}**({x[1]})")

                analytics_message = embed.get_standard_embed("Analisi staffer",
                                                             cfg.blue,
                                                             user.guild.icon_url,
                                                             [field, field2],
                                                             "Administrative system")
                await ctx.send(embed=analytics_message)
            except:
                field = ("Errore", "Utente non presente nel database.")
                analytics_message = embed.get_standard_embed("Analisi staffer",
                                                             cfg.red,
                                                             user.guild.icon_url,
                                                             [field],
                                                             "Administrative system")
                await ctx.send(embed=analytics_message)

            return
        else:
            try:
                await ctx.message.delete()
                await ctx.message.author.send("Non possiedi il ruolo per eseguire questo comando.")
            except:
                pass
            return

    @analytics.error
    async def analytics_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !analytics (@user)")

    @commands.command()
    async def uservoice(self, ctx):
        await ctx.message.delete()
        users = 0
        for channel in ctx.guild.channels:
            if channel.type == discord.ChannelType.voice:
                users += len(channel.members)

        send = discord.Embed(title="🙆‍♂️ • Utenti",
                             description=f"Attualmente sono connessi **{users}** utenti nei canali vocali",
                             colour=discord.Colour.blue())
        await ctx.channel.send(content=ctx.author.mention, embed=send, delete_after=120)

    @commands.command(aliases=["bugLs"])
    async def buglist(self, ctx):
        c = self.bot.get_cog('Db')
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.rolea7, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:

            await ctx.message.delete()

            bugs = ""

            for x in c.fetchallnovalues('SELECT * FROM bugTab'):
                bugs += f"[{x[0]}] {x[1]} \n"

            dire = discord.Embed(title="🦠 LISTA BUG 🦠",
                                 description=bugs,
                                 color=discord.Color.from_rgb(30, 115, 5))

            dire.set_footer(text=cfg.footer)
            await ctx.channel.send(embed=dire)

            await c.commit()

    @commands.command()
    async def bugadd(self, ctx, *bug):
        c = self.bot.get_cog('Db')
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5, cfg.rolea6, cfg.rolea7, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            c.execute("INSERT INTO bugTab (bug) VALUES (?)", (" ".join(bug),))
            print(f"[?] Aggiunto |{(' '.join(bug))}| alla lista dei bug")

            dire = discord.Embed(title="BUG AGGIUNTO",
                                 description=" ".join(bug),
                                 color=discord.Color.from_rgb(255, 255, 255))

            dire.set_footer(text=cfg.footer)
            await ctx.channel.send(embed=dire, delete_after=5)

            await c.commit()

    @commands.command()
    async def bugremove(self, ctx, number):
        c = self.bot.get_cog('Db')
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.roledev}

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            c.execute("DELETE FROM bugTab WHERE id = (?)", (number,))
            print(f"[?] Rimosso il bug numero {number} dalla lista dei bug")

            dire = discord.Embed(title="BUG RIMOSSO",
                                 color=discord.Color.from_rgb(0, 0, 0))

            dire.set_footer(text=cfg.footer)
            await ctx.channel.send(embed=dire, delete_after=5)

            await c.commit()


def setup(bot):
    bot.add_cog(Cmd(bot))
    print("[!] modulo cmd caricato")
