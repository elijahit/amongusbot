import discord
from discord.ext import commands


def get_prefix(bot, message):
    prefixes = ["it!"]

    if not message.guild:
        return "?"

    return commands.when_mentioned_or(*prefixes)(bot, message)


startup_extensions = ['cogs.interactions', 'cogs.cmd', 'cogs.config', 'cogs.db', 'cogs.default', 'cogs.embeds', 
'cogs.ticket', 'cogs.staffmover', 'cogs.ctrlhack', 'cogs.generatoreinsulti', 'cogs.logger', 'cogs.polls', 'cogs.invitemanager']

bot = commands.Bot(command_prefix=get_prefix, description='', case_insensitive=True)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = f"{type(e).__name__} : {e}"
            print(f"Failed to load extension {extension}\n{exc}")
            exit(1)

@bot.event
async def on_ready():

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Among Us Ita - it!AIUTO"))

    print(f"Logged in as: {bot.user.name} - {bot.user.id}\n")

    cfg = bot.get_cog('Config')
    print('-[{}]-\nScripted by Elijah.'.format(cfg.footer))
    print(
        f'''\nInvite link: https://discordapp.com/oauth2/
        authorize?client_id={bot.user.id}&scope=bot&permissions=8''')

bot.run('NzU3NjQ5NDU0MjM1OTEwMTc0.X2jeCg.7pQN7yL4ylmrFXK8pSnGOdFqxRc',
        bot=True,
        reconnect=True)
