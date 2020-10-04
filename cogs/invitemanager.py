# Sistema invitesystem per Among Us Ita (amongusita.it)
# Sviluppato da ImNotName#6666
# Per Among Us Ita#2534
import discord, time, datetime
from discord.ext import commands
import asyncio

class InviteManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def purgeinvite(self, ctx):
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3))
        if len(user_roles.intersection(admin_roles)) != 0:

            Embed = discord.Embed(description = f"Sei sicuro di voler cancellare tutti gli inviti esistenti attualmente?", colour = discord.Colour.orange())
            bot_reply = await ctx.send(content = ctx.message.author.mention, embed = Embed)
            await bot_reply.add_reaction("✅")
            await bot_reply.add_reaction("🚫")
            def check(reaction, user):
                return user.id == ctx.message.author.id
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check)
            except asyncio.TimeoutError:
                pass
            else:
                if reaction.emoji == "✅":
                    await bot_reply.clear_reactions()
                    Embed = discord.Embed(description = f"Sto cancellando tutti gli inviti del server...", colour = discord.Colour.blue())
                    await bot_reply.edit(content = ctx.message.author.mention, embed = Embed)
                    guid_invites = await ctx.guild.invites()
                    for invite in guid_invites:
                        await invite.delete()
                    Embed = discord.Embed(description = f"Ho cancellato tutti gli inviti esistenti", colour = discord.Colour.green())
                    await bot_reply.edit(content = ctx.message.author.mention, embed = Embed)

                elif reaction.emoji == "🚫":
                    await bot_reply.clear_reactions()
                    await bot_reply.delete()
                    await ctx.message.delete()


    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        if invite.max_age == 0:
            Embed = discord.Embed(description = f"Non puoi creare un invito con scadenza illimitata!", colour = discord.Colour.red())
            try:
                await invite.inviter.send(content = invite.inviter.mention, embed = Embed)
            except:
                pass
            await invite.delete()
        else:
            guid_invites = await invite.guild.invites()

            cfg = self.bot.get_cog('Config')
            user_roles = set([role.id for role in invite.inviter.roles])
            admin_roles = set((cfg.rolea1, cfg.rolea2, cfg.rolea3))

            if len(user_roles.intersection(admin_roles)) != 0:
                pass

            else:

                ignored_roles_ids = [744631580504359043, # owner
                                    744631542608822422, # mod
                                    744631301872680980, # helper
                                    754829854066737182, # gestore
                                    747833282993061889 # bots
                                    ]


                ignored_roles_objects = []
                for i in ignored_roles_ids:
                    try:
                        role = invite.guild.get_role(i)
                        ignored_roles_objects.append(role)
                    except Exception as e:
                        print(e)

                if len(guid_invites) > 0:
                    for server_invite in guid_invites:
                        if server_invite.inviter == invite.inviter and server_invite.code != invite.code:

                            for ignored in ignored_roles_objects:
                                if ignored in server_invite.inviter.roles:
                                    pass
                                else:
                                    await server_invite.delete()


def setup(bot):
    bot.add_cog(InviteManager(bot))
    print("[!] modulo invitemanager caricato")
