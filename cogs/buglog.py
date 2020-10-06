import discord
from discord.ext import commands
from time import sleep
import datetime as dt
import sqlite3 as sql


class Buglog(commands.Cog):

  def __init__(self, bot):
        self.bot = bot
  
  @commands.command(aliases=["bugLs"])
  async def bugList(self, ctx):
    c = self.bot.get_cog('Db')

    ctx.message.delete()

    bugs = ""

    c.execute("SELECT rowid, * FROM bugTab")
    for x in c.fetchall():
      bugs += f"[{x[0]}] {x[1]} \n"

    Dire = discord.Embed(title="🦠 LISTA BUG 🦠", 
      description=bugs, 
      color=discord.Color.from_rgb(30, 115, 5),
      timestamp=dt.datetime.utcnow())
    
    Dire.set_footer(text="Among Us Ita 0.1 **beta**")
    Dire.set_author(name = "EmergencyBot")
    await ctx.channel.send(embed = Dire)
    
    c.commit()
  
  @commands.command()
  async def bugAdd(self, ctx, *bug):
    c = self.bot.get_cog('Db')

    ctx.message.delete()

    c.execute("INSERT INTO bugTab VALUES (?)", (" ".join(bug),))
    print(f"[?] Aggiunto |{(' '.join(bug))}| alla lista dei bug")

    Dire = discord.Embed(title="BUG AGGIUNTO", 
      description= " ".join(bug), 
      color=discord.Color.from_rgb(255, 255, 255),
      timestamp=dt.datetime.utcnow())
    
    Dire.set_footer(text="Among Us Ita 0.1 **beta**")
    Dire.set_author(name = "EmergencyBot")
    await ctx.channel.send(embed = Dire, delete_after=5)

    c.commit()

  
  @commands.command()
  async def bugRem(self, ctx, number):
    c = self.bot.get_cog('Db')

    ctx.message.delete()

    c.execute("DELETE FROM bugTab WHERE rowid = (?)", (number,))
    print(f"[?] Rimosso il bug numero {number} dalla lista dei bug")

    Dire = discord.Embed(title="BUG RIMOSSO", 
      color=discord.Color.from_rgb(0, 0, 0),
      timestamp=dt.datetime.utcnow())
    
    Dire.set_footer(text="Among Us Ita 0.1 **beta**")
    Dire.set_author(name = "EmergencyBot")
    await ctx.channel.send(embed = Dire, delete_after=5)
    
    c.commit()
  

def setup(bot):
  bot.add_cog(Buglog(bot))        
  print("[!] modulo buglog caricato")