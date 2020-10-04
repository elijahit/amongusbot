import discord
from discord.ext import commands, tasks
import asyncio
# from sqlite3 import connect


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()


    @commands.command()
    async def poll(self, ctx, domanda, *opzioni):
        db = self.bot.get_cog('Db')
        embeds = self.bot.get_cog('Embeds')
        
        # Inizializza i polls

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


    @commands.command()
    async def stop_update(self, ctx, msg_id):
        db = self.bot.get_cog('Db')

        command = "DELETE FROM polls WHERE msg_id=?"
        db.Cursor.execute(command, (msg_id,))        


    @tasks.loop(seconds=10)
    async def update(self):
        db = self.bot.get_cog('Db')

        # Modifica l'embed aggiornando le percentuali e le barre

        reactions = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:", ":regional_indicator_j:"]

        # Estrae tutti gli id di tutti i polls dal db

        query = "SELECT msg_id FROM polls"
        db.Cursor.execute(query)
        polls = db.Cursor.fetchall()

        for poll in polls[-5:]:
            poll = poll[0]

            query = "SELECT channel_id FROM polls WHERE msg_id=?"
            db.Cursor.execute(query, (poll,))

            channel = self.bot.get_channel(758089360410411108)

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
    print("[!] modulo polls caricato.")