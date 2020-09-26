from discord.ext import commands
from asyncio import Lock

ranks = ['PREDATOR', 'MASTER', 'DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE']


class Binder(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._lock = Lock()

    @staticmethod
    async def add_prefix(user, prefix, nick):
        await user.edit(nick=f"{prefix} | {nick}")

    async def sync(self, user, prefix, nick):
        await self.add_prefix(user, prefix, nick)

    async def bind(self, user, nick, platform, prefix):

        db = self.bot.get_cog('DB')
        # lock access to db
        await self._lock.acquire()
        try:
            # write to db
            db.bind_user(nick, user.id, platform)
        finally:
            self._lock.release()

        await self.add_prefix(user, prefix, nick)

    async def unbind(self, user, db):
        await self._lock.acquire()
        try:
            db.unbind_user(user.id)
            await user.edit(nick=user.name)
        finally:
            self._lock.release()

    async def promote(self, user, new_rank, guild_id):

        db = self.bot.get_cog('DB')

        guild = self.bot.get_guild(guild_id)
        # remove old rank
        new_roles = [role for role in user.roles if role.name not in ranks]
        # add new rank
        new_roles.append(guild.get_role(int(db.get_rank_id(new_rank))))

        # set ranks
        await user.edit(roles=new_roles)


def setup(bot):
    bot.add_cog(Binder(bot))
