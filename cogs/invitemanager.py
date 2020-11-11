# Sistema invitesystem per Among Us Ita (amongusita.it)
# Sviluppato da ImNotName#6666
# Per Among Us Ita#2534
import asyncio

import discord
from discord.ext import commands


class InviteManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purgeinvite(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3}
        if len(user_roles.intersection(admin_roles)) != 0:

            embed = discord.Embed(description=f"Sei sicuro di voler cancellare tutti gli inviti esistenti attualmente?",
                                  colour=discord.Colour.orange())
            bot_reply = await ctx.send(content=ctx.message.author.mention, embed=embed)
            await bot_reply.add_reaction("✅")
            await bot_reply.add_reaction("🚫")

            def check(_, user):
                return user.id == ctx.message.author.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
            except asyncio.TimeoutError:
                pass
            else:
                if reaction.emoji == "✅":
                    await bot_reply.clear_reactions()
                    embed = discord.Embed(description=f"Sto cancellando tutti gli inviti del server...",
                                          colour=discord.Colour.blue())
                    await bot_reply.edit(content=ctx.message.author.mention, embed=embed)
                    guid_invites = await ctx.guild.invites()

                    for invite in guid_invites:
                        if invite.code != "hwSd6AM":
                            await invite.delete()

                    embed = discord.Embed(description=f"Ho cancellato tutti gli inviti esistenti",
                                          colour=discord.Colour.green())
                    await bot_reply.edit(content=ctx.message.author.mention, embed=embed)

                elif reaction.emoji == "🚫":
                    await bot_reply.clear_reactions()
                    await bot_reply.delete()
                    await ctx.message.delete()

<<<<<<< HEAD
    @commands.Cog.listener()
=======
    # @commands.Cog.listener()
>>>>>>> 5eb16c953dc3716c566b441c11d15029edfe778d
    async def on_invite_create(self, invite):

        if invite.max_age == 0:
            embed = discord.Embed(description=f"Non puoi creare un invito con scadenza illimitata!",
                                  colour=discord.Colour.red())
            try:
                await invite.inviter.send(content=invite.inviter.mention, embed=embed)
            except:
                pass
            await invite.delete()
        else:
            guild = invite.guild
            guid_invites = await guild.invites()

            cfg = self.bot.get_cog('Config')
            member = guild.get_member(invite.inviter.id)

            # When is None invoke the api -> return Member object
            if member is None:
                member = await guild.fetch_member(invite.inviter.id)
            user_roles = set([role.id for role in member.roles])
            admin_roles = {cfg.rolea1, cfg.rolea2, cfg.rolea3}

            if len(user_roles.intersection(admin_roles)) != 0:
                pass
            else:
                if len(guid_invites) > 0:
                    for server_invite in guid_invites:
                        if server_invite.inviter == invite.inviter and server_invite.code != invite.code:
                            await server_invite.delete()


def setup(bot):
    bot.add_cog(InviteManager(bot))
    print("[!] modulo invitemanager caricato")
