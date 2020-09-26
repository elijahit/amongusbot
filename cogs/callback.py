from discord.ext import commands
from discord.ext.commands import CommandNotFound
from datetime import datetime, timezone
import discord



class Callback(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_member_join(self, member):

		cfg = self.bot.get_cog('Config')
		db = self.bot.get_cog('db')

		db.Database.execute("INSERT INTO users (ID, Name, Creato, Joined) VALUES (?, ?, ?, ?)", (member.id, member.name, member.created_at.strftime("%d/%m/%y @ %H:%M:%S"), member.joined_at.strftime("%d/%m/%y @ %H:%M:%S")))
		db.Database.commit()
		###################### EMBED LOG INGRESSO #####################
		entrychannel = self.bot.get_channel(cfg.ingresso)
		embed=discord.Embed(color=cfg.green)
		embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
		embed.add_field(name="userlogs", value="**{0}#{1}** è entrato nel server.\n\
			**Id**: {2}\n\
			**Creato il**: {3}".format(member.name, member.discriminator, member.id, member.created_at.strftime("%d/%m/%y @ %H:%M:%S")), inline=True)
		embed.set_footer(text=cfg.footer)
		await entrychannel.send(embed=embed)
		print("[LOG] {0}#{1} è entrato nel server discord".format(member.name, member.discriminator))
		print("{0}".format(member.id))

		#####welcome dm
		messageesports_embed=discord.Embed(color=cfg.lightgreen)
		messageesports_embed.set_author(name="AMONG US ITA")
		messageesports_embed.add_field(name="-> Benvenuto!", value="Benvenuto {0} nel server ufficiale di **Among Us Ita**".format(member.mention, member.guild.member_count))
		messageesports_embed.set_thumbnail(url=member.guild.icon_url)
		messageesports_embed.set_footer(text=cfg.footer)
		await member.send(embed=messageesports_embed);
		#########log##########
		logchannel = self.bot.get_channel(cfg.log) #canale log
		embed=discord.Embed(color=cfg.lightgreen)
		embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
		embed.add_field(name="userlogs", value="**{0} gli è stato settato il ruolo `Ospite`**".format(member.mention), inline=True)
		embed.set_footer(text=cfg.footer)
		await logchannel.send(embed=embed)
		###############################################################

	@commands.Cog.listener()
	async def on_member_remove(self, member):

		cfg = self.bot.get_cog('Config')
		db = self.bot.get_cog('db')

		db.Database.execute("DELETE FROM users WHERE ID=?", (member.id,))
		db.Database.commit()
		###################### EMBED LOG USCITA #####################
		entrychannel = self.bot.get_channel(cfg.ingresso)
		embed=discord.Embed(color=cfg.red)
		embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
		embed.add_field(name="userlogs", value="{0}#{1} è uscito dal server di **Among Us Ita**".format(member.name, member.discriminator), inline=True)
		embed.set_footer(text=cfg.footer)
		await entrychannel.send(embed=embed)
		print("[LOG] {0}#{1} è uscito dal server discord".format(member.name, member.discriminator))
		print("{0}".format(member.id))
		###############################################################

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
	    if isinstance(error, CommandNotFound):
	        return
	    raise error


def setup(bot):
    bot.add_cog(Callback(bot))
    print("[!] modulo callback caricato")