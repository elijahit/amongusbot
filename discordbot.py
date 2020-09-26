from discordutils.bot import Bot

if __name__ == "__main__":
    bot = Bot()
    bot.bot.load_extension('cogs.db')
    bot.bot.load_extension('cogs.default')
    bot.bot.load_extension('cogs.embeds')
    bot.bot.load_extension('cogs.cmd')
    bot.bot.load_extension('cogs.voicechannels')
    bot.bot.load_extension('cogs.callback')
    bot.bot.load_extension('cogs.config')
    bot.start()


