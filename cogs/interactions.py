from discord.ext.commands import CommandNotFound
from discord.ext import commands


class Interactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        embed = self.bot.get_cog('Embeds')

        # Inserisce l'utente nel DB
        query = "INSERT INTO users (ID, Name, Creato, Joined) VALUES (?, ?, ?, ?)"
        values = (member.id, member.name, member.created_at.strftime("%d/%m/%y @ %H:%M:%S"),
                  member.joined_at.strftime("%d/%m/%y @ %H:%M:%S"))

        db.execute(query, values)
        db.commit()

        # Embed d'ingresso
        entrychannel = self.bot.get_channel(cfg.ingresso)
        name = f"{member}"
        field = ("userlogs",
                 f"**{member}** è entrato nel server.\n"
                 f"**Id**: {member.id}\n"
                 f"**Creato il**: {member.created_at.strftime('%d/%m/%y @ %H:%M:%S')}")

        login_embed = embed.get_standard_embed(name,
                                               cfg.green,
                                               member.avatar_url,
                                               [field],
                                               cfg.footer)

        await entrychannel.send(embed=login_embed)

        print(f"[LOG] {member.name}#{member.discriminator} è entrato nel server discord")
        print(f"{member.id}")

        # welcome dm
        field = (f"-> Benvenuto!", f"Benvenuto {member.mention} nel server ufficiale di **Among Us Ita**")
        welcome_message = embed.get_standard_embed("AMONG US ITA",
                                                   cfg.lightgreen,
                                                   member.guild.icon_url,
                                                   [field],
                                                   cfg.footer)

        await member.send(embed=welcome_message)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cfg = self.bot.get_cog('Config')
        db = self.bot.get_cog('Db')
        embed = self.bot.get_cog('Embeds')

        db.execute("DELETE FROM users WHERE ID=?", (member.id,))
        await db.commit()

        # Log d'uscita
        entrychannel = self.bot.get_channel(cfg.ingresso)
        field = ("userlogs", f"{member} è uscito dal server di **Among Us Ita**")
        embed = embed.get_standard_embed(f"{member}",
                                         cfg.red,
                                         member.avatar_url,
                                         [field],
                                         cfg.footer)

        await entrychannel.send(embed=embed)

        print("[LOG] {0}#{1} è uscito dal server discord".format(member.name, member.discriminator))
        print("{0}".format(member.id))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        raise error


def setup(bot):
    bot.add_cog(Interactions(bot))
    print("[!] modulo callback caricato")
