from asyncio import Lock

import discord
from discord.ext import commands

categories = ["STAFF VOICE"]


class Voicechannels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._channel_lock = Lock()

    @staticmethod
    def _get_guild(before, after):
        if before.channel:
            return before.channel.guild
        if after.channel:
            return after.channel.guild
        return None

    @staticmethod
    def _is_apex(channel, guild):
        if channel:
            category = guild.get_channel(channel.category_id)
            if category.name.upper() in categories:
                return category
        return False

    async def _add_channel(self, after_category, after_channel):
        await self._channel_lock.acquire()
        try:
            if len(after_channel.members) <= 1:
                new_name = after_category.voice_channels[-1].name.split()[1]
                await after_channel.clone(name=f'{after_channel.name.split()[0]} {int(new_name) + 1}')
                # actually add channel
        finally:
            self._channel_lock.release()

    async def _delete_channel(self, before_category, before_channel):
        await self._channel_lock.acquire()
        try:
            if len(before_channel.members) == 0 and len(before_category.voice_channels) > 1:
                await before_channel.delete()
                for i, channel in enumerate(before_category.voice_channels):
                    await channel.edit(name=f'{before_channel.name.split()[0]} {i + 1}')

            # actually delete channel
        finally:
            self._channel_lock.release()

    async def manage_channels(self, before, after):

        guild = self._get_guild(before, after)
        if guild:
            before_category = self._is_apex(before.channel, guild)
            after_category = self._is_apex(after.channel, guild)
            # if before_category != after_category:
            if before_category is not False:
                await self._delete_channel(before_category, before.channel)
            if after_category:
                await self._add_channel(after_category, after.channel)

    async def log_movements(self, member, before, after):

        cfg = self.bot.get_cog('Config')
        # embeds = self.bot.get_cog('Embeds')
        logchannel = self.bot.get_channel(cfg.voicelogs)

        if before.channel != after.channel:
            message = f'{member.display_name} è '
            if before.channel:
                message += f'uscito da {before.channel.name} '
            if after.channel:
                if before.channel:
                    message += 'ed è '
                message += f'entrato in {after.channel.name}'

            embed = discord.Embed(color=cfg.blue)
            embed.set_author(name="{0}#{1}".format(member.name, member.discriminator), icon_url=member.avatar_url)
            embed.add_field(name="userlogs-vocal", value=f"**{message}**", inline=True)
            embed.set_footer(text=cfg.footer)
            await logchannel.send(embed=embed)

    # LISTENERS
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        await self.log_movements(member, before, after)
        if before.channel != after.channel:
            await self.manage_channels(before, after)


def setup(bot):
    bot.add_cog(Voicechannels(bot))
