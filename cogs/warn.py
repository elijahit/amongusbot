import discord, time, datetime, sqlite3

from discord.ext import commands
from discord import utils

class Warns(commands.Cog):

    def __init__(self, client):
        self.bot = client

    #conn = sqlite3.connect('database.db')
    #c = conn.cursor()
    #c.execute("CREATE TABLE IF NOT EXISTS warns (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id, user_id, gravity, reason)")
    #conn.commit()
    #conn.close()

    @commands.command()
    async def warn(self, ctx, user: discord.Member, gravity: int, *, reason=None):

        # /warn imnotname 1 Flame => No effetti
        # /warn imnotname 2 Spam => ban dopo 5
        # /warn imnotname 3 Flood => ban dopo 3

        cfg = self.bot.get_cog('Config')
        
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all

        guild = ctx.message.guild
        author = ctx.message.author
        channel = ctx.channel
        gravity = int(gravity)
        
        await ctx.message.delete()
        if len(user_roles.intersection(admin_roles)) != 0:
            if ctx.message.author.id == user.id:
                embed = discord.Embed(title = "Errore", description = f"{author.mention} non puoi ammonire te stesso")
                await ctx.send(embed=embed)
                # YOU CAN'T WARN YOUSELF
                return 0
            await Warns.warn_user(self, guild, channel, author, user, gravity, reason)
    
    @commands.command()
    async def warnings(self, ctx, user: discord.Member):
        conn = self.bot.get_cog('Db')
        
        cfg = self.bot.get_cog('Config')
        
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_all
        
        await ctx.message.delete()
        if len(user_roles.intersection(admin_roles)) != 0:
        
            guild_id = ctx.message.guild.id
            user_id = user.id
            user_warnings = conn.fetchall("SELECT * FROM warns WHERE guild_id = ? AND user_id = ?", (guild_id, user_id,))

            warns = [f'[{idx + 1}] ID:*{i[0]}* Motivo: *{i[4]}*  | Gravità **{i[3]}**' for idx, i in enumerate(user_warnings)]
            
            embed=discord.Embed(title = f"Warns di {user}", description = "\n".join(warns) if len(warns)>0 else "Questo utente non ha nessun warns", color = discord.Colour.orange())
            
            await ctx.send(embed=embed)
        
    @warnings.error
    async def warnings_on_error(self, ctx, error):
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!warnings (@tag/id)")
            
    @warn.error
    async def warn_on_error(self, ctx, error):
        
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!warn (@tag/id) gravità motivazione")
            
    async def warn_user(self, guild, channel: discord.TextChannel, author: discord.Member, user: discord.Member, gravity: int, reason: str):
        
        conn = self.bot.get_cog('Db')
        cfg = self.bot.get_cog('Config')

        guild_id = guild.id
        author_id = author.id
        user_id = user.id
        gravity = gravity
        reason = reason if reason is not None else 'Non specificato'

        if gravity == 1:
            conn.execute("INSERT INTO warns(guild_id, user_id, gravity, reason) VALUES (?, ?, ?, ?)", (guild_id, user_id, gravity, reason,))
        elif gravity == 2 or gravity == 3 or gravity == 4:
            check = conn.fetchall("SELECT * FROM warns WHERE user_id = ? AND gravity = ?", (user.id, gravity,))

            if gravity == 2 and len(check) == 3:
                conn.execute("DELETE FROM warns WHERE user_id = ?", (user.id,))
                await Warns.ban_user(self, guild, channel, author, user, "Limite warn di gravità 2")
                return 0
            elif gravity == 3 and len(check) == 2:
                conn.execute("DELETE FROM warns WHERE user_id = ?", (user.id,))
                await Warns.ban_user(self, guild, channel, author, user, "Limite warn di gravità 3")
                return 0
            elif gravity == 4 and len(check) == 1:
                conn.execute("DELETE FROM warns WHERE user_id = ?", (user.id,))
                await Warns.ban_user(self, guild, channel, author, user, "Limite warn di gravità 4")
                return 0
            else:
                conn.execute("INSERT INTO warns(guild_id, user_id, gravity, reason) VALUES (?, ?, ?, ?)", (guild_id, user_id, gravity, reason,))
        
        try:
            for g in conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (author.id,)):
                if g[8] == None:
                    conn.execute("UPDATE analytics SET warn = 1 WHERE admin_id = ?", (author.id,))
                else:
                    conn.execute("UPDATE analytics SET warn = warn+1 WHERE admin_id = ?", (author.id,))
        except:
            pass

        try:
            d = conn.fetchall('SELECT * FROM analytics WHERE admin_id = ?', (author.id,))
            if len(d) == 0:
                conn.execute("INSERT INTO analytics (admin_id, warn) VALUES (?, ?)", (author.id, 1,))
        except:
            pass

        await conn.commit()

        warns = len(conn.fetchall("SELECT * FROM warns WHERE user_id = ? AND gravity = ?", (user_id, gravity,)))

        Warn = discord.Embed(title = "⚠️ • Warn", description= f"{author.mention} ha warnato {user.mention}", colour= discord.Colour.red())

        Warn.add_field(name = "Staffer", value = author, inline = True)
        Warn.add_field(name = "Utente warnato", value = user, inline = True)
        Warn.add_field(name = "Gravità del warn", value = gravity, inline = True)

        Warn.add_field(name = "Motivazione", value = reason, inline = True)
        Warn.add_field(name = "Warn attuali", value = warns, inline = True)
        Warn.add_field(name = "⠀", value = "⠀", inline = True)

        #await channel.send(content = user.mention, embed = Warn)
        logchannel = self.bot.get_channel(cfg.sanzioni) #canale log
        await logchannel.send(content = user.mention, embed = Warn)

    async def ban_user(self, guild, channel: discord.TextChannel, author: discord.Member, user: discord.Member, reason=None):

        cfg = self.bot.get_cog('Config')
        
        await guild.ban(user, reason=reason)
        
        embed = discord.Embed(title = "⛔️ • Ban", description = f"{author.mention} ha bannato {user.mention}")
        embed.add_field(name = "Staffer", value = author, inline = True)
        embed.add_field(name = "Utente bannato", value = user, inline = True)

        embed.add_field(name = "Motivazione", value = reason, inline = True)
        
        #await channel.send(embed=embed)
        logchannel = self.bot.get_channel(cfg.sanzioni) #canale log
        await logchannel.send(embed = embed)

def setup(client):
    client.add_cog(Warns(client))
    print("[!] modulo warns caricato")
