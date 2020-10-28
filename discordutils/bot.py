from discord.ext import commands

print("AVVIO BOT INIZIALIZZATO")


class Bot:
    _token = 'NzU3NjQ5NDU0MjM1OTEwMTc0.X2jeCg.7pQN7yL4ylmrFXK8pSnGOdFqxRc'

    def __init__(self):
        self.bot = commands.Bot(command_prefix='!')

    def start(self):
        self.bot.run(self._token)
