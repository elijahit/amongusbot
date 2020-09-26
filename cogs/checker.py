from discord.ext import commands


class Checker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def check_zero_param():
        def predicate(ctx):
            return len(ctx.message.content.split()) == 1

        return commands.check(predicate)

    @staticmethod
    def check_bind():
        def predicate(ctx):
            args = ctx.message.content.split()
            if len(args) != 3:
                return -1
            if args[2] not in ['psn', 'xbl', 'origin']:
                return -2
            return 1

        return commands.check(predicate)

    @staticmethod
    def check_dependencies(bot, deps):
        for dep in deps:
            print(bot.cogs)
            print(bot.get_cog(dep))
            if bot.get_cog(dep) is None:
                return False
        return True


def setup(bot):
    bot.add_cog(Checker(bot))
