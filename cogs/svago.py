import discord
from discord.ext import commands
from random import randint
from datetime import datetime as dt
import asyncio
from random import randint


class svago(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def rps(self, ctx):
		actions = ["📄", "✂️", "⛰"]

		await ctx.message.delete()

		botEmbd = discord.Embed(
				title=f"{ctx.message.author.name} ha sfidato il bot.",
				description="Scegli la tua mossa",
				color=discord.Color.from_rgb(230, 230, 230),
				timestamp=dt.utcnow()
			)
		botEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
		botEmbd.set_footer(text = "Toxic bot...")

		botMsg = await ctx.send(embed=botEmbd)

		for action in actions:
			await botMsg.add_reaction(action)

		def check1(reaction, user):
			if user.bot == False:
				return user == ctx.message.author and (str(reaction.emoji) == "📄" or str(reaction.emoji) == "✂️" or str(reaction.emoji) == "⛰")

		try:
			reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check1)

		except asyncio.TimeoutError:
			print("[W] timeout")

		else:
			botReact = actions[randint(0, 2)]
			await botMsg.clear_reactions()

			winEmbd = discord.Embed(
					title="Hai vinto!",
					description=f"{reaction} vs {botReact}",
					color=discord.Color.from_rgb(0, 170, 50),
					timestamp=dt.utcnow()
				)
			winEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
			winEmbd.set_footer(text = "Toxic bot...")

			drawEmbd = discord.Embed(
					title="Pareggio",
					description=f"{reaction} vs {botReact}",
					color=discord.Color.from_rgb(205, 180, 80),
					timestamp=dt.utcnow()
				)
			drawEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
			drawEmbd.set_footer(text = "Toxic bot...")

			lossEmbd = discord.Embed(
					title="Hai perso :(",
					description=f"{reaction} vs {botReact}",
					color=discord.Color.from_rgb(170, 50, 50),
					timestamp=dt.utcnow()
				)
			lossEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
			lossEmbd.set_footer(text = "Toxic bot...")

			if str(reaction.emoji) == "📄":
				if botReact == "📄":
					await discord.Message.edit(botMsg, embed=drawEmbd, delete_after=60)
				elif botReact == "✂️":
					await discord.Message.edit(botMsg, embed=lossEmbd, delete_after=60)
				elif botReact == "⛰":
					await discord.Message.edit(botMsg, embed=winEmbd, delete_after=60)

			elif str(reaction.emoji) == "✂️":
				if botReact == "📄":
					await discord.Message.edit(botMsg, embed=winEmbd, delete_after=60)
				elif botReact == "✂️":
					await discord.Message.edit(botMsg, embed=drawEmbd, delete_after=60)
				elif botReact == "⛰":
					await discord.Message.edit(botMsg, embed=lossEmbd, delete_after=60)

			elif str(reaction.emoji) == "⛰":
				if botReact == "📄":
					await discord.Message.edit(botMsg, embed=lossEmbd, delete_after=60)
				elif botReact == "✂️":
					await discord.Message.edit(botMsg, embed=winEmbd, delete_after=60)
				elif botReact == "⛰":
					await discord.Message.edit(botMsg, embed=drawEmbd, delete_after=60)

	@commands.command(aliases=["8ball"])
	async def eightball(self, ctx, *question):
		await ctx.message.delete()
		answs = [
			"E' certo",
			"Senza dubbio",
			"Puoi contarci",
			"Sicuramente",
			"E' stato deciso così",
			"Per come la vedo io, si",
			"Molto probabilmente",
			"Si",
			"Sembra positivo",
			"I segnali indicano di si",
			"Sono confuso, riprova",
			"Meglio non dirtelo",
			"Richiedimelo più tardi",
			"Non posso prevederlo al momento",
			"Concentrati e richiedimelo",
			"Non ci contare",
			"I segnali non sono positivi",
			"Le mie risorse dicono di no",
			"Molto improbabile",
			"La mia risposta è no",
		]
		ans = answs[randint(0, len(answs) - 1)]

		ansBot = discord.Embed(
				tile=None,
				description=f"**Domanda:** \n{' '.join(question)} \n\n**Risposta:** \n{ans}",
				color=discord.Color.from_rgb(20, 100, 100),
				timestamp=dt.utcnow()
			)
		ansBot.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
		ansBot.set_footer(text = "Toxic bot...")

		await ctx.channel.send(embed=ansBot, delete_after=60)

	@commands.command()
	async def ship(self, ctx, user1=None, user2=None):
		await ctx.message.delete()
		
		if (user1 != None and (user1.startswith("<@!") or user1.startswith("<@")) and user1.endswith(">")) and (user2 != None and (user2.startswith("<@!") or user2.startswith("<@")) and user2.endswith(">")):
			aff=randint(0, 100)
			affStr=""

			for f in range(1, (aff + 1)):
				if (f % 20) == 0:
					affStr+="⬜"
			
			if int(len(affStr) / 2) < 10:
				for g in range(1, (6 - len(affStr))):
					affStr+="⬛"

			affinityEmbd=discord.Embed(
					title=None,
					description=\
					f"**L'affinità tra {user1} e {user2} è di:** \n\
					\t{aff}% \n\
					[{affStr}]",
					color=discord.Color.from_rgb(230, 115, 240),
					timestamp=dt.utcnow()
				)
			affinityEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
			affinityEmbd.set_footer(text = "Toxic bot...")
			await ctx.channel.send(embed=affinityEmbd, delete_after=20)
		else:
			correctEmbd=discord.Embed(
					title="Hai sbagliato comando :(",
					description="Questo comando va usato così: `>ship @utente1 @utente2`, riprova",
					color=discord.Color.from_rgb(230, 30, 30),
					timestamp=dt.utcnow()
				)
			correctEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
			correctEmbd.set_footer(text = "Toxic bot...")
			await ctx.channel.send(embed=correctEmbd, delete_after=20)

	@commands.command()
	async def punch(self, ctx, user2=None):
		await ctx.message.delete()
		commen = [
			"E' superefficace!",
			"E' superefficace!",
			"Colpisci più forte!",
			"Colpisci più forte!",
			"Ha fatto male",
			"Ha fatto male",
			"Sembri una femminuccia...",
			"Sembri una femminuccia...",
			"**KO!! ⚰️💀**"
		]
		punEmbd = discord.Embed(
				title=None,
				description=f"\
					**{ctx.message.author.mention} ha colpito {user2}:** \n\
					{commen[randint(0, 8)]} 🥊\
				",
				color=discord.Color.from_rgb(200, 50, 50),
				timestamp=dt.utcnow()
			)
		punEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
		punEmbd.set_footer(text = "Toxic bot...")
		await ctx.channel.send(embed=punEmbd, delete_after=60)

	@commands.command()
	async def coin(self, ctx):
		await ctx.message.delete()

		poss = ["testa", "croce"]

		flipEmbd = discord.Embed(
				title=None,
				description=f"\
					**{ctx.message.author.mention} ha lanciato una moneta.** \n\
					\n\
					**Il risultato:** \n\
					{poss[randint(0, 1)]}\
				",
				color=discord.Color.from_rgb(255, 255, 50),
				timestamp=dt.utcnow()
			)
		flipEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
		flipEmbd.set_footer(text = "Toxic bot...")

		await ctx.channel.send(embed=flipEmbd, delete_after=60)

	@commands.command()
	async def rand(self, ctx, maxnum=None):
		await ctx.message.delete()

		randEmbd = discord.Embed(
				title="Il tuo numero è:",
				description=f"{str(randint(0, int(maxnum)))}",
				color=discord.Color.from_rgb(25, 200, 200),
				timestamp=dt.utcnow()
			)
		randEmbd.set_author(name="Toxic bot", icon_url=self.bot.user.avatar_url)
		randEmbd.set_footer(text = "Toxic bot...")
		await ctx.channel.send(embed=randEmbd, delete_after=60)

	@commands.command()
	async def insulta(self, ctx, user=None):
	  Insulti = ["sei un coglione.", "sei uno stronzo.", "sei uno sciacallo.", "sei un cesso.", "sei un deficente.", "sei un testa di cazzo.", "sei un gigolò.", "sei un bastardo.",\
		   "sei un lecacculo.", "sei un porco.", "sei uno stupido.", "sei una iena.", "sei una sega.",\
			"sei un imbecille.", "sei un conta-palle.", "sei una palla.", "sei un senza palle.", "sei una merda.", "sei un minchione.", "sei un rincoglionito.", "sei un fannullone.",\
			"sei un buono a nulla.", "sei un ingrato.", "sei un pezzente.", "sei una feccia umana.",\
			"sei un meschino.", "sei un pirla.", "sei un ruffiano.", "sei un merdoso.", "sei un tamarro.", "sei un bifolco.", "sei un farabutto.", "sei un quaquaraquà.", "sei un cerebroleso.",\
			"sei un lurido.", "sei un e-boy.", "sei un goblin.", "sei un maiale.", "pezzo di merda.", "vaffanculo.", "vai a farti fottere.", "obbrobrio.", "ti prendo per le orecchie e ti alzo come la coppa Uefa.",\
			"è uscito meglio pinocchio con una sega che te con una scopata.", "sei un tipo obbiettivo? e fai una foto a sto cazzo!!!", "sei così stronzo che sudi merda!", "occhio che ti parcheggio le mani in faccia."\
			"nella tua vita hai commesso un solo grande errore: esisti", "'Giamaicà' = già mai cacato 'r cazzo", "hai così tante corna che se piovono taralli non ne cade a terra nemmeno uno",\
			"te giro le corna e ti uso come scooter", "sei talmente stronzo che se schiacci 'na merda fai scopa", "sei talmente orribile che fai concorrenza ai marylin manson.",\
			"sei talmente brutto che se te vede la morte se gratta le palle", "non ti piglio a schiaffi perche la merda schizza", "mi presti la tua faccia che devo fare una figura di merda?.",\
			"ma va a fà bungee jumping cor catenaccio.", "Se la bruttezza facesse bandiera a casa tua sarebbe sempre festa nazionale.", "fatti uno stock di cazzi tuoi...",\
			"ma che bella acconciatura: ti sei pettinato coi raudi?", "c'hai l'ascella commossa!", "quando ti siedi devi stringere il culo o ti entra dentro la sedia!",\
			"ami la natura?... anche dopo lo scherzo che ti ha fatto?", "ti do una sberla che vai tanto lontano che devi portarti dietro il cestino della merenda.",\
			"sei cosi' grasso che dovunque guardo stai gia' la'.", "sei così rotto in culo che gli stronzi ti escono per gravità.", "sei come una mutanda... stai sempre davanti al cazzo...",\
			"sei un accollo", "hai la merda in testa", "non sei cosí brutto: ti manca la catena per essere un cesso.", "c'hai una panza che se te vede mazinga ce parcheggia l'astronave."]

	  await ctx.message.delete()
	    
	  cfg = self.bot.get_cog("Config")

	  insulto=Insulti[randint(0, 69)]

	  messaggio = discord.Embed(title=f"{(Insulti.index(insulto) + 1)} / {len(Insulti)}", 
	      description=f"{user} {insulto}", 
	      color=discord.Color.from_rgb(130, 30,150), 
	      timestamp=dt.utcnow())  
	  messaggio.set_footer(text="Toxic bot...")
	  messaggio.set_author(name = "Toxic bot", icon_url=self.bot.user.avatar_url)
	  await ctx.channel.send(embed=messaggio, delete_after=60)


def setup(bot):
	bot.add_cog(svago(bot))
	print("[!] modulo svago caricato")