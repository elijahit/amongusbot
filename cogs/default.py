from discord.ext import commands
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionNotLoaded, ExtensionNotFound
import discord

cogs_path = 'cogs.'


class Default(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Among Us Ita - !AIUTO"))
        cfg = self.bot.get_cog('Config')
        print('-[{}]-\nScripted by Elijah.'.format(cfg.footer))
        print(
        '''\nInvite link: https://discordapp.com/oauth2/
        authorize?client_id={}&scope=bot&permissions=8'''
        .format(self.bot.user.id))

    async def _cog_handler(self, ctx, action, *args):

        embeds = self.bot.get_cog('Embeds')
        if len(args) != 1:
            await ctx.send(f'[SYNTAX]: !{action} <cog-name>')
            return False

        cog = args[0]

        # try:
        try:
            if action == 'caricato':
                self.bot.load_extension(f'cogs.{cog}')
            elif action == 'rimosso':
                self.bot.unload_extension(f'cogs.{cog}')
            elif action == 'ricaricato':
                self.bot.reload_extension(f'cogs.{cog}')
            elif action == 'check':
                self.bot.cog_check(f'cogs.{cog}')

        except ExtensionNotLoaded:
            await ctx.send(embed=embeds.get_error_message(description=f'[ERROR] Modulo {cog} non caricato'))
            return

        except ExtensionAlreadyLoaded:
            await ctx.send(embed=embeds.get_error_message(description=f'[ERROR] Modulo {cog} già caricato'))
            return

        except ExtensionNotFound:
            await ctx.send(embed=embeds.get_error_message(description=f'[ERROR] Modulo {cog} inesistente'))
            return

        await ctx.send(embed=embeds.get_success_message(description=f'[SUCCESS]: Modulo {args[0]} {action} con successo'))

    @commands.command()
    async def load(self, ctx, *args):
        await self._cog_handler(ctx, 'caricato', *args)

    @commands.command()
    async def unload(self, ctx, *args):
        await self._cog_handler(ctx, 'rimosso', *args)

    @commands.command()
    async def reload(self, ctx, *args):
        await self._cog_handler(ctx, 'ricaricato', *args)

    @commands.command()
    async def list(self, ctx, *args):

        embeds = self.bot.get_cog('Embeds')
        await ctx.send(embed=embeds.get_success_message(description=', '.join([c for c in self.bot.cogs]), title='Moduli disponibili'))


def setup(bot):
    bot.add_cog(Default(bot))