import discord
from discord.ext import commands
from asyncio import sleep
import datetime as dt

mess = None
channel_search = None
time_start = None
sus_users = [(" ", " ")]
solo = None
admin_live_id = ""
solo = True

class Ctrlhack(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def hackhelp(self, ctx):
        cmdsLs = discord.Embed(title="LISTA COMANDI HACKCMD", description="**-> Comandi admin** \n\
            !hack (numero stanza matchmaking) **[Convoca una stanza matchmaking per il controllo hack]**\n\
                !FAIL **[elimina TUTTE le chat vocali dalla categoria 'controllo hack']**\n\
                    !RESETLIST **[resetta la lista degli helper con un controllo hack in corso]**")
        cmdsLs.set_author(name = "Among Us Ita")
        cmdsLs.set_footer(text="Among Us Ita 0.1 **beta**")

        await ctx.channel.send(embed=cmdsLs, delete_after=120)

    @commands.command()
    async def hack(self, ctx, channel_num):
        global mess, channel_search, admin_live_id
        channel_search = "matchmaking " + channel_num

        user_send = ctx.channel.last_message.author
        if user_send == None:
            await sleep(1)
            user_send = ctx.channel.last_message.author
            await sleep(3)

        await ctx.channel.purge(limit=1)

        if str(user_send.id) not in admin_live_id:

            admin_live_id += f"{str(user_send.id)} "

            Warning = discord.Embed(title="🟥 E' STATO CONVOCATO UN CONTROLLO HACK 🟥", description=f"{user_send.mention} ha convocato il gruppo: {channel_search} per un controllo hack, proseguire?", color=discord.Color.red(), timestamp=dt.datetime.utcnow())
            Warning.set_footer(text="Among Us Ita 0.1 **beta**")
            Warning.set_author(name = "Among Us Ita")

            message_sent = await ctx.channel.send(embed=Warning)
            await message_sent.add_reaction("🟢")
            await message_sent.add_reaction("🔴")
        
        else:
            Warning = discord.Embed(title="🟪 UN MEMBRO PUO' AVERE UN MASSIMO DI UN CONTROLLO APERTO 🟪", description=f"{user_send.mention}, \nchiudi prima tutti i tuoi controlli  poi riprova", color=discord.Color.purple(), timestamp=dt.datetime.utcnow())
            Warning.set_footer(text="Among Us Ita 0.1 **beta**")
            Warning.set_author(name = "Among Us Ita")
            mexa = await ctx.channel.send(embed=Warning)

            await sleep(5)

            await mexa.delete()

        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global solo

        if user.bot == False and str((reaction.message.embeds)[0].author) == "EmbedProxy(name='Among Us Ita')":
            

            if reaction.emoji == "🟢" and str(user.id) == (((((reaction.message.embeds)[0].description).split())[0].replace("<@!", "")).replace(">", "").replace("<@", "")) and solo == True:
                global sus_users
                sus_users = [(" ", " ")]
                sus_users.pop()

                global guild_now, category, category_channels, i, hackchannels, admin_live_id
                guild_now = reaction.message.channel.guild
                channel_got = discord.utils.get(guild_now.voice_channels, name=channel_search)
                category = discord.utils.get(guild_now.categories, name="controllo hack")
                category_channels = category.voice_channels

                solo = False

                try:
                    user_send=self.bot.get_user(int(((((reaction.message.embeds)[0].description).split())[0].replace("<@!", "")).replace(">", "").replace("<@", "")))


                    member2_0 = []
                    for member in channel_got.members:
                        memberprovv = f"{str(member.name)}#{str(member.discriminator)} ({member.nick})" if member.nick != None else f"{str(member.name)}#{str(member.discriminator)} ({member.name})"
                        if member.is_on_mobile() == True:
                            member2_0 += f"{memberprovv} su 📱\n"
                        else:
                            member2_0 += f"{memberprovv} su 💻\n"
                
                    
                    sus_users.append(tuple(["".join(member2_0), (((((reaction.message.embeds)[0].description).split())[0].replace("<@!", "")).replace(">", "").replace("<@", ""))]))
                    
                    
                    i = 1

                    for channel in category_channels:
                        if str(channel).startswith(f"Vocale {i} generale"):
                            i += 1
                    
                    await category.create_voice_channel(f"Vocale {i} generale 🥵")
                    await category.create_voice_channel(f"┠ Vocale {i}-1 🥶")
                    await category.create_voice_channel(f"┠ Vocale {i}-2 🥶")
                    await category.create_voice_channel(f"┗ Vocale {i}-3 🥶")

                    hackchannels = [discord.utils.get(guild_now.voice_channels, name=f"Vocale {i} generale 🥵"), discord.utils.get(guild_now.voice_channels, name=f"┠ Vocale {i}-1 🥶"), discord.utils.get(guild_now.voice_channels, name=f"┠ Vocale {i}-2 🥶"), discord.utils.get(guild_now.voice_channels, name=f"┗ Vocale {i}-3 🥶")]

                    await reaction.message.clear_reaction("🔴")

                    for member in channel_got.members:
                        await member.move_to(hackchannels[0])

                    Warning = discord.Embed(title="🟨 IL TUO CONTROLLO STA PER INIZIARE 🟨", description=f"{user_send.mention}: torna qui una volta finito per chiudere il controllo \n \n*Entra nella chat vocale (Vocale generale {i} 🥵)!* \n{await hackchannels[0].create_invite()} \n \n**Hai 10 secondi...**", color=discord.Color.orange(), timestamp=dt.datetime.utcnow())
                    Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                    Warning.set_author(name = "Among Us Ita")
                    await discord.Message.edit(reaction.message, embed=Warning)

                    await reaction.message.clear_reaction("🟢")

                    await sleep(10)

                    Warning = discord.Embed(title="🟩 CONTROLLO IN CORSO 🟩", description=f"Lo staff {user_send.mention} sta controllando degli utenti nella {i}° chat vocale \n{await hackchannels[0].create_invite()} \n \nUna volta chiuso al posto di questo messaggio troverete un rapporto dettagliato del controllo \n \n**PREMI LA REAZIONE PER CHIUDERE IL CONTROLLO**", color=discord.Color.green(), timestamp=dt.datetime.utcnow())
                    Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                    Warning.set_author(name = "Among Us Ita")

                    user_send = (((((reaction.message.embeds)[0].description).split())[2].replace("<@!", "")).replace(">", "").replace("<@", ""))

                    await discord.Message.edit(reaction.message, embed=Warning)
                    await discord.Message.add_reaction(reaction.message, "🔕")

                    solo = True

                except Exception as error:
                    user_send = self.bot.get_user(int(((((reaction.message.embeds)[0].description).split())[0].replace("<@!", "")).replace(">", "").replace("<@", "")))
                    Warning = discord.Embed(title="🧻🚽 OH NO, QUALCOSA E' ANDATO STORTO 🚽🧻", description=f"Purtroppo la richiesta di {user_send.mention} non è andata a buon termine, riprova e controlla che la stanza esista e che si può avere solo un controllo attivo per staff. \nSe il problema persiste non esitare a contattare uno degli sviluppatori. \n \n**ERRORE:**{error} \n \nQuesto messaggio si autodistruggerà tra 30 secondi...", color=discord.Color.dark_orange(), timestamp=dt.datetime.utcnow())
                    Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                    Warning.set_author(name = "Among Us Ita")
                    await discord.Message.edit(reaction.message, embed=Warning, delete_after=30)
                    await reaction.message.clear_reactions()

            elif reaction.emoji == "🔴" and str(user.id) == (((((reaction.message.embeds)[0].description).split())[0].replace("<@!", "")).replace(">", "").replace("<@", "")):
                user_send = self.bot.get_user(int(((((reaction.message.embeds)[0].description).split())[0].replace("<@!", "")).replace(">", "").replace("<@", "")))
                Warning = discord.Embed(title="⬛️ IL CONTROLLO HACK E' STATO REVOCATO ⬛️", description=f"{user_send.mention}: questo messaggio si autodistruggerà tra 3 secondi...", color=discord.Colour.default(), timestamp=dt.datetime.utcnow())
                Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                Warning.set_author(name = "Among Us Ita")
                await discord.Message.edit(reaction.message, embed=Warning, delete_after=3)

            elif reaction.emoji == "🔕" and (((reaction.message.embeds)[0].title).split())[0] == "🟩" and str(user.id) == (((((reaction.message.embeds)[0].description).split())[2].replace("<@!", "")).replace(">", "").replace("<@", "")):
                user_send = self.bot.get_user(int(((((reaction.message.embeds)[0].description).split())[2].replace("<@!", "")).replace(">", "").replace("<@", "")))
                numero = (((reaction.message.embeds)[0].description).split())[8].replace("°", "")

                times = int((dt.datetime.utcnow() - (reaction.message.embeds)[0].timestamp).total_seconds())
                timem = int(round(times / 60)) if times >= 60 else 0
                times -= timem * 60 if timem != 0 else 0
                timeh = int(round(timem / 60)) if timem >= 60 else 0
                timem -= timeh * 60 if timeh != 0 else 0
                
                sus_users_true = None

                for c in sus_users:
                    if c[1] == (((((reaction.message.embeds)[0].description).split())[2].replace("<@!", "")).replace(">", "").replace("<@", "")):
                        sus_users_true = c[0]
                
                Warning = discord.Embed(title="⬜️ CONTROLLO HACK FINITO ⬜️", description=f"**STAFF:** {user_send.mention} \n**DURATA:** {timeh}:{timem}:{times}  _(h:mm:ss)_ \n**UTENTI COINVOLTI:** \n`{sus_users_true}`", color=discord.Color.lighter_gray(), timestamp=dt.datetime.utcnow())
                Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                Warning.set_author(name = "Among Us Ita")
                await discord.Message.edit(reaction.message, embed=Warning)

                category_channels = category.voice_channels

                for channel in category_channels:
                    if str(channel).startswith(f"Vocale {numero}") or str(channel).startswith(f"┠ Vocale {numero}") or str(channel).startswith(f"┗ Vocale {numero}"):
                        await channel.delete()
                        
                await reaction.message.clear_reaction("🔕")
                admin_live_id = admin_live_id.replace(str(user_send.id), " ")

            else:
                await reaction.message.remove_reaction(reaction, user)

    @commands.command()
    async def FAIL(self, ctx):
        for channel in (discord.utils.get(ctx.guild.categories, name="controllo hack")).voice_channels:
            await channel.delete()
        await ctx.message.delete()

    @commands.command()
    async def RESETLIST(self, ctx):
        global admin_live_id
        admin_live_id = ""
        await ctx.channel.send("svuotato", delete_after=2)

def setup(bot):
    bot.add_cog(Ctrlhack(bot))
    print("[!] modulo controllohack caricato")