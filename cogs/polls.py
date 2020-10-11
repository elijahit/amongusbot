import discord
from discord.ext import commands, tasks
import asyncio


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()


    @commands.command()
    async def poll(self, ctx, domanda, *opzioni):

        # Inizializza i polls

        db = self.bot.get_cog('Db')
        embeds = self.bot.get_cog('Embeds')
        cfg = self.bot.get_cog("Config")

        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            # Manda un messaggio di errore in caso le opzioni selezionate siano minori di 1 o maggiori di 10

            if len(opzioni) == 0 or len(opzioni) <= 1:
                msg = await ctx.channel.send(embed=embeds.get_error_message(description="Non puoi iniziare un sondaggio con meno di 2 opzioni! Assicurati di aver utilizzato la giusta formattazione: `?poll \"Domanda\" \"Opzione 1\" \"Opzione 2\"` (le opzioni vanno messe tra le virgolette con un massimo di 10 opzioni)."))
                await asyncio.sleep(10)
                await msg.delete()

            elif len(opzioni) > 10:
                msg = await ctx.channel.send(embed=embeds.get_error_message(description="Non puoi iniziare un sondaggio con più di 10 opzioni! Assicurati di aver utilizzato la giusta formattazione: `?poll \"Domanda\" \"Opzione 1\" \"Opzione 2\"` (le opzioni vanno messe tra le virgolette con un massimo di 10 opzioni)."))
                await asyncio.sleep(10)
                await msg.delete()

            # Crea il sondaggio

            else:
                reactions = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯"]
                testo = ""

                for i, opzione in enumerate(opzioni):
                    testo += f"{reactions[i]} {opzione}\n"

                embed = discord.Embed(title=f"📊 **{domanda}**", description=testo, colour=discord.Colour.gold())
                embed.set_footer(text="Among Us Ita 0.1 **beta**")
                msg = await ctx.message.channel.send(embed=embed)

                for x in range(len(opzioni)):
                    await msg.add_reaction(reactions[x])

                # Aggionge al db l'id del messaggio e del canale del poll

                try:
                    command = "INSERT INTO polls (msg_id, channel_id) VALUES (?, ?)"
                    db.Cursor.execute(command, (msg.id, msg.channel.id))
                    db.Database.commit()

                except Exception:
                    print("[!] Poll non aggiunto al database.")


    @tasks.loop(seconds=10)
    async def update(self):

        # Modifica l'embed aggiornando le percentuali e le barre

        db = self.bot.get_cog('Db')

        reactions = [":regional_indicator_a:",
                     ":regional_indicator_b:",
                     ":regional_indicator_c:",
                     ":regional_indicator_d:",
                     ":regional_indicator_e:",
                     ":regional_indicator_f:",
                     ":regional_indicator_g:",
                     ":regional_indicator_h:",
                     ":regional_indicator_i:",
                     ":regional_indicator_j:"]

        # Estrae tutti gli id di tutti i polls dal db

        query = "SELECT msg_id FROM polls"
        db.Cursor.execute(query)
        polls = db.Cursor.fetchall()

        for poll in polls:
            try:
                poll = poll[0]

                query = "SELECT channel_id FROM polls WHERE msg_id=?"
                db.Cursor.execute(query, (poll,))
                channel_id = db.Cursor.fetchone()
                db.Database.commit()

                channel = self.bot.get_channel(channel_id[0])

                msg = await channel.fetch_message(poll)
                embed = msg.embeds[0]

                # Rimuove le precedenti stats

                for x in range(len(embed.fields)):
                    embed.remove_field(0)

                totale = 0

                for react in msg.reactions:
                    totale += react.count - 1

                # Aggiorna le nuove stats

                if totale != 0:
                    stats = []

                    for i, react in enumerate(msg.reactions):
                        stats.append(int(((react.count - 1) / totale) * 100))

                        intero = int(stats[i] / 10)

                        bar = ""

                        if intero == 0:
                            bar = "<:vuoto1:760485808372449280>" +  "<:vuoto2:760485783542693919>" * 6 + "<:vuoto3:760485761593770034>"

                        elif intero == 10:
                            bar = "<:pieno1:760485732711268382>" + "<:pieno2:760485711681683486>" * 6 + "<:pieno3:760485685395718164>"

                        else:
                            bar = "<:pieno1:760485732711268382>" + "<:pieno2:760485711681683486>" * (intero - 3) + "<:vuoto2:760485783542693919>" * (7 - (intero)) + "<:vuoto3:760485761593770034>"


                        embed.add_field(name=f"{reactions[i]} - {stats[i]}%", value=bar, inline=False)

                    await msg.edit(embed=embed)

            except:
                continue


    @commands.command()
    async def delete_polls(self, ctx):
        db = self.bot.get_cog('Db')
        embeds = self.bot.get_cog('Embeds')
        cfg = self.bot.get_cog("Config")

        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            try:
                query = "DELETE FROM polls"
                db.Cursor.execute(query)
                db.Database.commit()

                await ctx.channel.send(embed=embeds.get_success_message("Polls cancellati con successo!"))

            except Exception:
                await ctx.channel.send(embed=embeds.get_error_message("Non sono riuscito cancellare i polls..."))


    @commands.command()
    async def delete_poll(self, ctx, msg_id):
        db = self.bot.get_cog('Db')
        embeds = self.bot.get_cog('Embeds')
        cfg = self.bot.get_cog("Config")

        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5,
        cfg.rolea6, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            try:
                query = "SELECT msg_id, channel_id FROM polls WHERE msg_id=?"
                db.Cursor.execute(query, (msg_id,))
                data = db.Cursor.fetchall()
                db.Database.commit()

                channel = self.bot.get_channel(data[0][1])
                msg = await channel.fetch_message(data[0][0])

                for reaction in msg.reactions:
                    async for user in reaction.users():
                        await reaction.remove(user)

                query = "DELETE FROM polls WHERE msg_id=?"
                db.Cursor.execute(query, (msg_id,))
                db.Database.commit()

                await ctx.channel.send(embed=embeds.get_success_message("Poll rimosso dal db."))

            except Exception:
                await ctx.channel.send(embed=embeds.get_error_message("Non sono riuscito a rimuovere il poll dal db."))


    @commands.command()
    async def add_poll(self, ctx, msg_id, channel_id):
        db = self.bot.get_cog('Db')
        embeds = self.bot.get_cog('Embeds')
        cfg = self.bot.get_cog("Config")

        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3, cfg.rolea4, cfg.rolea5,
        cfg.rolea6, cfg.roledev))

        if len(user_roles.intersection(admin_roles)) != 0:
            await ctx.message.delete()

            try:
                command = "INSERT INTO polls (msg_id, channel_id) VALUES (?, ?)"
                db.Cursor.execute(command, (msg_id, channel_id))
                db.Database.commit()

                channel = self.bot.get_channel(764492739660218379)
                msg = await channel.fetch_message(msg_id)

                for i, field in enumerate(msg.embeds[0].fields):
                    await msg.add_reaction(reactions[i])

                await ctx.channel.send(embed=embeds.get_success_message("Poll aggiunto al db."))

            except Exception:
                await ctx.channel.send(embed=embeds.get_error_message("Non sono riuscito ad aggiungere il poll al db."))


    @commands.command()
    async def pollshelp(self, ctx):
        embed = self.bot.get_cog("Embeds")
        cfg = self.bot.get_cog("Config")

        name = "Polls System"
        field = ("Comandi Poll","it!poll (\"Domanda\") (\"Opzione 1\") (\"Opzione 2\") **[Inizializza il poll con un massimo di 10 opzioni]**\n\
                                 it!delete_poll (msg_id) **[Rimuove tutti i polls dal db]** \n\
                                 it!delete_polls **[Rimuove il poll selezionato dal db]** \n\
                                 it!add_poll (msg_id) (channel_id)  **[Aggiunge al db il poll indicato]** \n\
                                 it!pollshelp **[Info sul modulo Poll]**")

        about_embed = embed.get_standard_embed(name,
                                               cfg.blue,
                                               ctx.guild.icon_url,
                                               [field],
                                               cfg.footer)

        await ctx.channel.send(embed=about_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        db = self.bot.get_cog('Db')

        # Fa in modo che gli utenti possano aggiungere solo una react al poll

        db.Cursor.execute("SELECT channel_id FROM polls WHERE msg_id=?", (payload.message_id,))
        result = db.Cursor.fetchone()

        if result:

            channel = await self.bot.fetch_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)

            for r in msg.reactions:

                if payload.member in await r.users().flatten() and not payload.member.bot and str(r) != str(payload.emoji):

                    await msg.remove_reaction(r.emoji, payload.member)


def setup(bot):
    bot.add_cog(Poll(bot))
    print("[!] Modulo polls caricato.")
