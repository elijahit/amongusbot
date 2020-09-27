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
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
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

    @commands.command()
    async def mvto(self, ctx, *ch_dest):
        await ctx.message.delete()
        cfg = self.bot.get_cog('Config')
        if cfg.rolea1 in [role.name for role in ctx.message.author.roles] or cfg.rolea2 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea3 in [role.name for role in ctx.message.author.roles] or cfg.rolea4 in [role.name for role in ctx.message.author.roles]\
        or cfg.rolea5 in [role.name for role in ctx.message.author.roles] or cfg.rolea6 in [role.name for role in ctx.message.author.roles]:
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


def setup(bot):
    bot.add_cog(StaffMover(bot))
    print("[!] modulo staffmover caricato")
