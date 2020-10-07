from discord.ext.commands import CommandNotFound
from discord.ext import commands
import discord


class Interactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def welcome_dm(self, member):
        debug = self.bot.get_channel(758089360410411108)
        embed = self.bot.get_cog('Embeds')
        cfg = self.bot.get_cog('Config')

        ##CANALI##
        regolamento = self.bot.get_channel(750840605545857064)
        annunci = self.bot.get_channel(748504257782743081)
        wtf = self.bot.get_channel(755865318777159790)
        booster = self.bot.get_channel(746337813795962961)
        report = self.bot.get_channel(748908550973292604)
        matchmaking = self.bot.get_channel(748932393154641970)
        generale = self.bot.get_channel(747841447407124510)
        live = self.bot.get_channel(751062558206590976)
        ruoli = self.bot.get_channel(746124795791540224)


        field = (f"Benvenuto", cfg.welcomemessage.format(user=member.mention,
                                        server=member.guild.name,
                                        regole=regolamento.mention,
                                        annunci=annunci.mention,
                                        wtf=wtf.mention,
                                        booster=booster.mention,
                                        report=report.mention,
                                        matchmaking=matchmaking.mention,
                                        generale=generale.mention,
                                        live=live.mention,
                                        ruoli=ruoli.mention))

        field2 = (f"Vuoi supportarci?", cfg.welcomemessage2.format(user=member.mention,
                                        server=member.guild.name,
                                        regole=regolamento.mention,
                                        annunci=annunci.mention,
                                        wtf=wtf.mention,
                                        booster=booster.mention,
                                        report=report.mention,
                                        matchmaking=matchmaking.mention,
                                        generale=generale.mention,
                                        live=live.mention,
                                        ruoli=ruoli.mention))
        welcome_message = embed.get_image_embed("Benvenuto su Among Us Ita",
                                                cfg.lightgreen,
                                                member.avatar_url,
                                                [field, field2],
                                                "https://cdn.discordapp.com/attachments/758087809671102574/763020270084554772/Benvenuto.jpg",
                                                member.guild.icon_url,
                                                "Among Us ita © amongusita.it | Devloped by 3rd Party Developers")

        await debug.send(embed=welcome_message)


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
        await db.commit()

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
        try:       
            #self.welcome_dm(member)
            pass
        except:
            pass

    @commands.command()#addrole
    async def debugdm(self, ctx, member:discord.Member):
        await self.welcome_dm(member)

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
    print("[!] modulo interactions caricato")
