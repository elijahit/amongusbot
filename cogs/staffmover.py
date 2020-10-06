# Sistema staffmover per Among Us Ita (amongusita.it)
# Sviluppato da ImNotName#6666
# Per Among Us Ita#2534
import discord
from discord.ext import commands
from discord import utils

admins = [609158181972606987]

class StaffMover(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mvhere(self, ctx):
        await ctx.message.delete()
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            sender = ctx.message.author
            moved = []
            errors = []
            if sender.voice is not None:
                for user_id in ctx.message.raw_mentions:
                    member = utils.find(lambda m: m.id == user_id, ctx.guild.members)
                    if member.voice is not None:
                        if sender.voice.channel.id != member.voice.channel.id:
                            vc = sender.voice.channel
                            await member.move_to(vc)
                            moved.append(f"• `{member.name}` {'(📱)' if member.is_on_mobile() else '(💻)'} \n")
                        else:
                            errors.append(f"• `{member.name}` {'(📱)' if member.is_on_mobile() else '(💻)'} è __già__ connesso al tuo canale vocale.\n")
                    else:
                        errors.append(f"• `{member.name}` {'(📱)' if member.is_on_mobile() else '(💻)'} __non__ è connesso ad un canale vocale.\n")
            else:
                errors.append(f"• `{sender.name}` {'(📱)' if sender.is_on_mobile() else '(💻)'} __non__ sei collegato ad un canale vocale.\n")
            if len(moved) > 0:
                text = discord.Embed(title = f"**👮 Sposta utenti**", description=f"Come richiesto da **{sender.name}** ho spostato gli utenti in stanza **{vc}**", colour = discord.Colour.green())
                text.add_field(name = "👥 Utenti spostati", value = f"{''.join(moved)}", inline=True)
                if len(errors) > 0:
                    text.add_field(name = "📕 Errori", value = f"{''.join(errors)}", inline=False)
                text.set_footer(text="Among Us Ita 0.1 **beta**")
                await ctx.send(embed = text)
            if len(errors) > 0 and len(moved) == 0:
                Warning = discord.Embed(title = f"**👮 Sposta utenti**", colour = discord.Colour.red())
                Warning.add_field(name = "📕 Errori", value = f"{''.join(errors)}", inline=True)
                Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                await ctx.send(embed = Warning)
    @mvhere.error
    async def mvhere_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!mvhere (@tag/id) [Si possono spostare più di un utente]")

    @commands.command()
    async def mvto(self, ctx, *ch_dest):
        await ctx.message.delete()
        cfg = self.bot.get_cog('Config')
        user_roles = set([role.id for role in ctx.message.author.roles])
        admin_roles = cfg.rolea_top8

        if len(user_roles.intersection(admin_roles)) != 0:
            sender = ctx.message.author
            guild = ctx.guild
            moved = []
            errors = []

            dest_ch_id = 0

            filtri = []

            for f in ch_dest:
                if not '@' in f:
                    filtri.append(f)

            text = ""
            n = 0
            for filtro in filtri:
                n = n + 1
                text = text + filtro
                if len(filtri) > n:
                    text = text + ' '

            for channel in guild.voice_channels:
                if text.lower() in channel.name.lower():
                    dest_ch_id = channel.id
                    break

            if dest_ch_id == 0:
                Warning = discord.Embed(description = f"Canale inserito non trovato!", colour = discord.Colour.red())
                await ctx.send(embed = Warning)

            elif dest_ch_id != 0:
                for user_id in ctx.message.raw_mentions:
                    member = utils.find(lambda m: m.id == user_id, ctx.guild.members)

                    if member.voice is not None:
                        vc = self.bot.get_channel(dest_ch_id)
                        if member.voice.channel.id != vc.id:
                            await member.move_to(vc)
                            moved.append(f"• `{member.name}` {'(📱)' if member.is_on_mobile() else '(💻)'} \n")
                        else:
                            errors.append(f"• `{member.name}` {'(📱)' if member.is_on_mobile() else '(💻)'} __è__ già connesso al canale {vc}.\n")
                    else:
                        errors.append(f"• `{member.name}` {'(📱)' if member.is_on_mobile() else '(💻)'} __non__ è connesso ad un canale vocale.\n")

                if len(moved) > 0:
                    text = discord.Embed(title = f"**👮 Sposta utenti**", description=f"Come richiesto da **{sender.name}** ho spostato gli utenti in stanza **{vc}**", colour = discord.Colour.green())
                    text.add_field(name = "👥 Utenti spostati", value = f"{''.join(moved)}", inline=True)
                    if len(errors) > 0:
                        text.add_field(name = "📕 Errori", value = f"{''.join(errors)}", inline=False)
                    text.set_footer(text="Among Us Ita 0.1 **beta**")
                    await ctx.send(embed = text)
                if len(errors) > 0 and len(moved) == 0:
                    Warning = discord.Embed(title = f"**👮 Sposta utenti**", colour = discord.Colour.red())
                    Warning.add_field(name = "📕 Errori", value = f"{''.join(errors)}", inline=True)
                    Warning.set_footer(text="Among Us Ita 0.1 **beta**")
                    await ctx.send(embed = Warning)
    @mvto.error
    async def mvto_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("[!] USA: it!mvto (@tag/id) (nome stanza) [Si possono spostare più di un utente]")


def setup(bot):
    bot.add_cog(StaffMover(bot))
    print("[!] modulo staffmover caricato")
