# Sistema insulti per Among Us Ita (amongusita.it)
# Sviluppato da iTzSgrullee_#5858
# Per Among Us Ita#2534
import random
from datetime import datetime as dt

import discord
from discord.ext import commands

InsultiF = ["sei una cogliona", "sei una stronza", "sei una sciacalla", "sei una cessa", "sei una deficente",
            "sei una testa di cazzo", "sei una baldracca", "sei una bastarda",
            "sei una lecacculo", "sei una porca", "sei una stupida", "sei una iena", "sei una sega",
            "sei una imbecille", "sei una conta-palle", "sei una palla", "sei una senza palle", "sei una merda",
            "sei una minchiona", "sei una rincoglionita", "sei una fannullona",
            "sei una buona a nulla", "sei una ingrata", "sei una pezzente", "sei una feccia umana",
            "sei una meschina", "sei una pirla", "sei una ruffiana", "sei una merdosa", "sei una tamarra",
            "sei una bifolca", "sei una farabutta", "sei una quaquaraquà", "sei una cerebrolesa",
            "sei una lurida", "sei una e-girl", "sei una befana", "sei una scrofa", "pezzo di merda", "vaffanculo",
            "vai a farti fottere", "obbrobrio", "ti prendo per le orecchie e ti alzo come la coppa Uefa",
            "è uscito meglio pinocchio con una sega che te con una scopata",
            "sei una tipa obbiettiva? e fai una foto a sto cazzo!!!", "sei così stronza che sudi merda!",
            "occhio che ti parcheggio le mani in faccia"
            "nella tua vita hai commesso un solo grande errore: esisti", "'Giamaicà' = già mai cacato 'r cazzo",
            "hai così tante corna che se piovono taralli non ne cade a terra nemmeno uno",
            "te giro le corna e ti uso come scooter", "sei talmente stronzo che se schiacci 'na merda fai scopa",
            "sei talmente orribile che fai concorrenza ai marylin manson",
            "Sei talmente brutta che se te vede la morte se gratta le palle",
            "Non ti piglio a schiaffi perche la merda schizza",
            "Mi presti la tua faccia che devo fare una figura di merda?",
            "Ma va a fà bungee jumping cor catenaccio",
            "Se la bruttezza facesse bandiera a casa tua sarebbe sempre festa nazionale",
            "fatti uno stock di cazzi tuoi..",
            "ma che bella acconciatura: ti sei pettinata coi raudi?", "c'hai l'ascella commossa!",
            "quando ti siedi devi stringere il culo o ti entra dentro la sedia!",
            "ami la natura?... anche dopo lo scherzo che ti ha fatto?",
            "ti do una sberla che vai tanto lontano che devi portarti dietro il cestino della merenda",
            "sei cosi' grassa che dovunque guardo stai gia' la'",
            "sei così rotta in culo che gli stronzi ti escono per gravità",
            "sei come una mutanda... stai sempre davanti al cazzo..",
            "sei una cozza", "hai la merda in testa", "non sei cosí brutta: ti manca la catena per essere un cesso",
            "c'hai una panza che se te vede mazinga ce parcheggia l'astronave"]

InsultiM = ["sei un coglione", "sei uno stronzo", "sei uno sciacallo", "sei un cesso", "sei un deficente",
            "sei un testa di cazzo", "sei un gigolò", "sei un bastardo",
            "sei un lecacculo", "sei un porco", "sei uno stupido", "sei una iena", "sei una sega",
            "sei un imbecille", "sei un conta-palle", "sei una palla", "sei un senza palle", "sei una merda",
            "sei un minchione", "sei un rincoglionito", "sei un fannullone",
            "sei un buono a nulla", "sei un ingrato", "sei un pezzente", "sei una feccia umana",
            "sei un meschino", "sei un pirla", "sei un ruffiano", "sei un merdoso", "sei un tamarro", "sei un bifolco",
            "sei un farabutto", "sei un quaquaraquà", "sei un cerebroleso",
            "sei un lurido", "sei un e-boy", "sei un goblin", "sei un maiale", "pezzo di merda", "vaffanculo",
            "vai a farti fottere", "obbrobrio", "ti prendo per le orecchie e ti alzo come la coppa Uefa",
            "è uscito meglio pinocchio con una sega che te con una scopata",
            "sei un tipo obbiettivo? e fai una foto a sto cazzo!!!", "sei così stronzo che sudi merda!",
            "occhio che ti parcheggio le mani in faccia"
            "nella tua vita hai commesso un solo grande errore: esisti", "'Giamaicà' = già mai cacato 'r cazzo",
            "hai così tante corna che se piovono taralli non ne cade a terra nemmeno uno",
            "te giro le corna e ti uso come scooter", "sei talmente stronzo che se schiacci 'na merda fai scopa",
            "sei talmente orribile che fai concorrenza ai marylin manson",
            "Sei talmente brutto che se te vede la morte se gratta le palle",
            "Non ti piglio a schiaffi perche la merda schizza",
            "Mi presti la tua faccia che devo fare una figura di merda?",
            "Ma va a fà bungee jumping cor catenaccio",
            "Se la bruttezza facesse bandiera a casa tua sarebbe sempre festa nazionale",
            "fatti uno stock di cazzi tuoi..",
            "ma che bella acconciatura: ti sei pettinato coi raudi?", "c'hai l'ascella commossa!",
            "quando ti siedi devi stringere il culo o ti entra dentro la sedia!",
            "ami la natura?... anche dopo lo scherzo che ti ha fatto?",
            "ti do una sberla che vai tanto lontano che devi portarti dietro il cestino della merenda",
            "sei cosi' grasso che dovunque guardo stai gia' la'",
            "sei così rotto in culo che gli stronzi ti escono per gravità",
            "sei come una mutanda... stai sempre davanti al cazzo..",
            "sei un accollo", "hai la merda in testa", "non sei cosí brutto: ti manca la catena per essere un cesso",
            "c'hai una panza che se te vede mazinga ce parcheggia l'astronave"]


class Generatoreinsulti(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insulta(self, ctx, user, sesso):
        await ctx.message.delete()

        cfg = self.bot.get_cog("Config")

        insulto = InsultiF[random.randint(0, 69)] if sesso.lower() == "f" else InsultiM[random.randint(0, 69)]
        colore = 16711935 if sesso.lower() == "f" else 4020177
        index = InsultiF.index(insulto) if sesso.lower() == "f" else InsultiM.index(insulto)

        messaggio = discord.Embed(title=f"{index} / {len(InsultiF)}", description=f"{user} {insulto}",
                                  color=discord.Colour(colore), timestamp=dt.utcnow())
        messaggio.set_footer(text=cfg.footer)
        messaggio.set_author(name="Generatore di insulti")

        await ctx.channel.send(embed=messaggio)


def setup(bot):
    bot.add_cog(Generatoreinsulti(bot))
    print("[!] modulo Generatoreinsulti caricato")
