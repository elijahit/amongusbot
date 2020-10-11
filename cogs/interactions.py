from discord.ext.commands import CommandNotFound
from datetime import datetime, timedelta
from discord.ext import commands, tasks
import discord
import time

class Interactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tasks = None
        if self.messageloop.is_running():
            self.messageloop.cancel()
            self.messageloop.start()
        else:
            self.messageloop.start()

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
        field3 = (f"\n\nIn fine", cfg.welcomemessage3.format(server=member.guild.name))
        welcome_message = embed.get_welcomemessage_embed("Benvenuto su Among Us Ita",
                                                cfg.lightgreen,
                                                member.avatar_url,
                                                [field, field2],
                                                field3, #inlinefield
                                                "https://cdn.discordapp.com/attachments/758087809671102574/763020270084554772/Benvenuto.jpg",
                                                member.guild.icon_url,
                                                "Among Us ita © amongusita.it | Devloped by 3rd Party Developers")

        await debug.send(embed=welcome_message)

    async def checkinvite(self, message):
        pass
        


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
        crewmember = member.guild.get_role(746124009715924996)
        await member.add_roles(crewmember)

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

    @tasks.loop(seconds=10)
    async def messageloop(self):
        if self.tasks is None:
            await self.load_tasks()
            return 0

        if len(self.tasks) > 0:
            for i in self.tasks:
                
                # 0 = id, 1 = channel_id, 2 = text, 3 = freq
                now = round(int(time.time()), -1)

                # TODO: Read list of recurrent msgs from DB
                msg = i[2]
                freq = i[3]
                #

                freq = datetime.strptime(freq, "%H:%M:%S")
                ms = int(timedelta(hours=freq.hour, minutes=freq.minute, seconds=freq.second).total_seconds())

                if now % ms == 0:
                    Send = discord.Embed(title = "🤖 • Messaggio automatico", description= f"{msg}")
                    await self.bot.get_channel(i[1]).send(embed=Send)

    @messageloop.before_loop
    async def before_loop(self):        
        await self.bot.wait_until_ready()
    
    async def load_tasks(self):
        conn = self.bot.get_cog("Db")
        z = conn.fetchallnovalues("SELECT * FROM scheduled_tasks")
        self.tasks = z
        
        if self.messageloop.is_running() is True:
            self.messageloop.restart()
        else:
            self.messageloop.start()        
    
    @commands.command()
    async def addmessage(self, ctx, channel_id: int, freq: str, *, text: str):
        
        conn = self.bot.get_cog("Db")
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.roledev

        if len(user_roles.intersection(admin_roles)) != 0:
            conn.execute("INSERT INTO scheduled_tasks (channel_id, text, freq) VALUES (?, ?, ?)", (channel_id, text, freq,))
            await conn.commit()
            
            msg = f"Messaggio automatico in: {channel_id}\nesto: {text}\nFrequenza: {freq}"
            await ctx.send(content=msg, delete_after=40)
            await self.load_tasks()
    @addmessage.error
    async def addmessage_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !addmessage (canaleID) (freq 00:00:00) (testo)")

    @commands.command()
    async def removemessage(self, ctx, messageid):
        
        conn = self.bot.get_cog("Db")
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.roledev

        if len(user_roles.intersection(admin_roles)) != 0:
            conn.execute("DELETE FROM scheduled_tasks WHERE id=?", (messageid,))
            await conn.commit()
            
            msg = f"Rimosso messaggio ID: {messageid}"
            await ctx.send(content=msg, delete_after=40)
            await self.load_tasks()
    
    @removemessage.error
    async def removemessage_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument) or isinstance(error, commands.errors.BadArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: !removemessage (ID message DB)")


def setup(bot):
    bot.add_cog(Interactions(bot))
    print("[!] modulo interactions caricato")
