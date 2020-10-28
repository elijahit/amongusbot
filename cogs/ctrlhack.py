# Sistema Controllo Hack per Among Us Ita (amongusita.it)
# Sviluppato da iTzSgrullee_#585
# Per Among Us Ita#2534
import datetime as dt
import asyncio
import discord
from discord.ext import commands

mess = None
time_start = None
sus_users = [(" ", " ")]
admin_live_id = ""
inUso = False


class Ctrlhack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hackhelp(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            cmd_ls = discord.Embed(title="LISTA COMANDI", description="**Comandi admin** \n\
            it!hack (numero stanza matchmaking) **[Convoca una stanza matchmaking per il controllo hack]**\n\
                \n\
                **Per risolvere i bug** \n\
                it!FAIL **[elimina TUTTE le chat vocali dalla categoria 'controllo hack']**\n\
                    it!RESETLIST **[resetta la lista degli helper con un controllo hack in corso]**")
            cmd_ls.set_author(name="Among Us Ita")
            cmd_ls.set_footer(text=cfg.footer)

            await ctx.channel.send(embed=cmd_ls, delete_after=120)

    @commands.command()
    async def hack(self, ctx, num):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            global mess, admin_live_id

            user_send = ctx.message.author
            if user_send is None:
                await asyncio.sleep(1)
                user_send = ctx.message.author
                await asyncio.sleep(3)

            if str(user_send.id) not in admin_live_id:

                admin_live_id += f"{str(user_send.id)} "

                warning = discord.Embed(title="🟥 E' STATO CONVOCATO UN CONTROLLO HACK 🟥",
                                        description=f"{user_send.mention} ha convocato il gruppo: matchmaking {num} per un controllo hack, proseguire?",
                                        color=discord.Color.red(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")

                message_sent = await ctx.channel.send(embed=warning)
                await message_sent.add_reaction("🟢")
                await message_sent.add_reaction("🔴")

            else:
                warning = discord.Embed(title="🟪 UN MEMBRO PUO' AVERE UN MASSIMO DI UN CONTROLLO APERTO 🟪",
                                        description=f"{user_send.mention}, \nchiudi prima tutti i tuoi controlli  poi riprova",
                                        color=discord.Color.purple(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")
                mexa = await ctx.channel.send(embed=warning)

                await asyncio.sleep(5)

                await mexa.delete()

    @hack.error
    async def hack_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !hack (numero matchmaking)")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        cfg = self.bot.get_cog("Config")
        if user.bot is False and str(reaction.message.embeds[
                                         0].author) == "EmbedProxy(name='Among Us Ita')" and reaction.message.channel.category_id == 762080734537056266:
            global inUso, admin_live_id

            if reaction.emoji == "🟢" and str(user.id) == (
                    ((reaction.message.embeds[0].description.split())[0].replace("<@!", "")).replace(">",
                                                                                                     "").replace(
                        "<@",
                        "").replace(
                        ":", "")) and inUso is False:

                await reaction.message.clear_reaction("🔴")

                global sus_users
                sus_users = [(" ", " ")]
                sus_users.pop()

                # TODO
                # Da rifare l'intero sistema perchè con i globals non si può guardare

                global guild_now, category, category_channels, i, hackchannels
                guild_now = reaction.message.channel.guild
                channel_got = discord.utils.get(guild_now.voice_channels,
                                                name=f"matchmaking {(reaction.message.embeds[0].description.split())[6]}")
                category = discord.utils.get(guild_now.categories, name="controllo hack")
                category_channels = category.voice_channels

                try:
                    user_send = self.bot.get_user(int(
                        ((reaction.message.embeds[0].description.split())[0].replace("<@!", "")).replace(">",
                                                                                                         "").replace(
                            "<@", "").replace(":", "")))

                    inUso = True

                    warning = discord.Embed(title="🟡 IL TUO CONTROLLO STA PER INIZIARE 🟡",
                                            description=f"{user_send.mention}: torna qui una volta finito per chiudere il controllo \n \n*Aspetta che vengano create le tue stanze!* \n \n \n**Hai 10 secondi...** \n \n*Durante questa operazione non sarà possibile reagire ad altri controlli hack*",
                                            color=discord.Color.orange(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="HackBot")
                    await discord.Message.edit(reaction.message, embed=warning)

                    member2_0 = []
                    for member in channel_got.members:
                        memberprovv = f"{str(member.name)}#{str(member.discriminator)} ({member.nick})" if member.nick is not None else f"{str(member.name)}#{str(member.discriminator)} ({member.name})"
                        if member.is_on_mobile() is True:
                            member2_0 += f"{memberprovv} su 📱\n"
                        else:
                            member2_0 += f"{memberprovv} su 💻\n"

                    sus_users.append(tuple(["".join(member2_0), (
                        ((reaction.message.embeds[0].description.split())[0].replace("<@!", "")).replace(">",
                                                                                                         "").replace(
                            "<@", "").replace(":", ""))]))

                    i = 1

                    for channel in category_channels:
                        if str(channel).startswith(f"Vocale {i} generale"):
                            i += 1

                    await category.create_voice_channel(f"Vocale {i} generale 🥵")
                    await category.create_voice_channel(f"┠ Vocale {i}-1 🥶")
                    await category.create_voice_channel(f"┠ Vocale {i}-2 🥶")
                    await category.create_voice_channel(f"┗ Vocale {i}-3 🥶")

                    hackchannels = [discord.utils.get(guild_now.voice_channels, name=f"Vocale {i} generale 🥵"),
                                    discord.utils.get(guild_now.voice_channels, name=f"┠ Vocale {i}-1 🥶"),
                                    discord.utils.get(guild_now.voice_channels, name=f"┠ Vocale {i}-2 🥶"),
                                    discord.utils.get(guild_now.voice_channels, name=f"┗ Vocale {i}-3 🥶")]

                    warning = discord.Embed(title="🟨 IL TUO CONTROLLO STA PER INIZIARE 🟨",
                                            description=f"{user_send.mention}: torna qui una volta finito per chiudere il controllo \n \n*Entra nella chat vocale (Vocale generale {i} 🥵)!* \n \n**Hai 10 secondi...** \n \n*Durante questa operazione non sarà possibile reagire ad altri controlli hack*",
                                            color=discord.Color.orange(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="HackBot")
                    await discord.Message.edit(reaction.message, embed=warning)

                    conn = self.bot.get_cog("Db")
                    try:
                        for g in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user.id,)):
                            if g[4] is None:
                                conn.execute("UPDATE analytics SET hack = 1 WHERE admin_id = ?", (user.id,))
                            else:
                                conn.execute("UPDATE analytics SET hack = hack+1 WHERE admin_id = ?", (user.id,))
                    except:
                        print("errore")

                    try:
                        d = conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (user.id,))
                        if len(d) == 0:
                            conn.execute("INSERT INTO analytics (admin_id, hack) VALUES (?, ?)", (user.id, 1,))
                    except:
                        print("error2")

                    await conn.commit()

                    for member in channel_got.members:
                        await member.move_to(hackchannels[0])

                    await reaction.message.clear_reaction("🟢")

                    await asyncio.sleep(10)

                    warning = discord.Embed(title="🟩 CONTROLLO IN CORSO 🟩",
                                            description=f"Lo staff {user_send.mention} sta controllando degli utenti nella {i}° chat vocale \n \nUna volta chiuso al posto di questo messaggio troverete un rapporto dettagliato del controllo \n \n**PREMI LA REAZIONE PER CHIUDERE IL CONTROLLO**",
                                            color=discord.Color.green(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="Among Us Ita")

                    inUso = False

                    # user_send = (
                    #     ((reaction.message.embeds[0].description.split())[2].replace("<@!", "")).replace(">",
                    #                                                                                      "").replace(
                    #         "<@", "").replace(":", ""))

                    await discord.Message.edit(reaction.message, embed=warning)
                    await discord.Message.add_reaction(reaction.message, "🔕")

                except Exception as error:
                    user_send = self.bot.get_user(int(
                        ((reaction.message.embeds[0].description.split())[0].replace("<@!", "")).replace(">",
                                                                                                         "").replace(
                            "<@", "").replace(":", "")))
                    admin_live_id = admin_live_id.replace(str(user_send.id), " ")
                    inUso = False

                    warning = discord.Embed(title="🧻🚽 OH NO, QUALCOSA E' ANDATO STORTO 🚽🧻",
                                            description=f"{user_send.mention} la tua richiesta non è andata a buon termine, riprova e controlla che la stanza esista \nSe il problema persiste non esitare a contattare uno degli sviluppatori. \n{(reaction.message.channel.guild.get_role(cfg.IDruoliDev[0])).mention} | {(reaction.message.channel.guild.get_role(cfg.IDruoliDev[1])).mention} \n**ERRORE:**{error} \n \nQuesto messaggio si autodistruggerà tra 30 secondi...",
                                            color=discord.Color.dark_orange(), timestamp=dt.datetime.utcnow())
                    warning.set_footer(text=cfg.footer)
                    warning.set_author(name="Among Us Ita")
                    await discord.Message.edit(reaction.message, embed=warning, delete_after=30)
                    await reaction.message.clear_reactions()

            elif reaction.emoji == "🔴" and str(user.id) == (
                    ((reaction.message.embeds[0].description.split())[0].replace("<@!", "")).replace(">",
                                                                                                     "").replace(
                        "<@",
                        "").replace(
                        ":", "")) and inUso is False:
                await reaction.message.clear_reactions()

                user_send = self.bot.get_user(int(
                    ((reaction.message.embeds[0].description.split())[0].replace("<@!", "")).replace(">",
                                                                                                     "").replace(
                        "<@", "").replace(":", "")))
                warning = discord.Embed(title="⬛️ IL CONTROLLO HACK E' STATO REVOCATO ⬛️",
                                        description=f"{user_send.mention}: questo messaggio si autodistruggerà tra 3 secondi...",
                                        color=discord.Colour.default(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")
                await discord.Message.edit(reaction.message, embed=warning, delete_after=3)

                admin_live_id = admin_live_id.replace(str(user_send.id), " ")

            elif reaction.emoji == "🔕" and (reaction.message.embeds[0].title.split())[0] == "🟩" and str(
                    user.id) == (
                    ((reaction.message.embeds[0].description.split())[2].replace("<@!", "")).replace(">",
                                                                                                     "").replace(
                        "<@",
                        "").replace(
                        ":", "")) and inUso is False:
                user_send = self.bot.get_user(int(
                    ((reaction.message.embeds[0].description.split())[2].replace("<@!", "")).replace(">",
                                                                                                     "").replace(
                        "<@", "").replace(":", "")))
                numero = (reaction.message.embeds[0].description.split())[8].replace("°", "")

                times = int((dt.datetime.utcnow() - reaction.message.embeds[0].timestamp).total_seconds())
                timem = int(round(times / 60)) if times >= 60 else 0
                times -= timem * 60 if timem != 0 else 0
                timeh = int(round(timem / 60)) if timem >= 60 else 0
                timem -= timeh * 60 if timeh != 0 else 0

                sus_users_true = None

                for c in sus_users:
                    if c[1] == (
                            ((reaction.message.embeds[0].description.split())[2].replace("<@!", "")).replace(">",
                                                                                                             "").replace(
                                "<@", "").replace(":", "")):
                        sus_users_true = f"`{c[0]}`"

                if sus_users_true == "``":
                    sus_users_true = "`Nessuno`"

                warning = discord.Embed(title="⬜️ CONTROLLO HACK FINITO ⬜️",
                                        description=f"**STAFF:** {user_send.mention} \n \n**DURATA:** {abs(timeh)}:{abs(timem)}:{abs(times)}  _(h:mm:ss)_ \n**UTENTI COINVOLTI:** \n{sus_users_true}",
                                        color=discord.Color.lighter_gray(), timestamp=dt.datetime.utcnow())
                warning.set_footer(text=cfg.footer)
                warning.set_author(name="Among Us Ita")
                await discord.Message.edit(reaction.message, embed=warning)

                category_channels = category.voice_channels

                for channel in category_channels:
                    if str(channel).startswith(f"Vocale {numero}") or str(channel).startswith(
                            f"┠ Vocale {numero}") or str(channel).startswith(f"┗ Vocale {numero}"):
                        await channel.delete()

                await reaction.message.clear_reaction("🔕")
                admin_live_id = admin_live_id.replace(str(user_send.id), " ")

            else:
                await reaction.message.remove_reaction(reaction, user)

        else:
            pass

    @commands.command()
    async def fail(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            for ctx.channel in (discord.utils.get(ctx.guild.categories, name="controllo hack")).voice_channels:
                await ctx.channel.delete()

    @commands.command()
    async def resetlist(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()
            global admin_live_id
            admin_live_id = ""
            await ctx.channel.send("svuotato", delete_after=2)


def setup(bot):
    bot.add_cog(Ctrlhack(bot))
    print("[!] modulo controllohack caricato")
