# Sistema logger per Among Us Ita (amongusita.it)
# Sviluppato da ImNotName#6666
# Per Among Us Ita#2534
import discord, time, datetime
from discord.ext import commands
from discord import utils

class Logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        cfg = self.bot.get_cog('Config')
        guild = member.guild
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            now = datetime.datetime.now()
            account_age = now - member.created_at
            account_age = str(account_age).split(" ")[0]
            joined_time = now.strftime("%d/%m/%Y %H:%M:%S")
            Log = discord.Embed(description = f"**Evento**: {member.mention} si è unito al server", colour = discord.Colour.dark_green())
            Log.set_author(name = member, icon_url = member.avatar_url)
            Log.add_field(name = "Nome", value = member, inline=True)
            Log.add_field(name = "ID", value = f"`{member.id}`", inline=True)
            Log.add_field(name = "Età account", value = f"**{account_age}** giorni", inline=True)
            Log.add_field(name = "Orario", value = joined_time, inline=True)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        try:
            await guild.fetch_ban(member)
        except discord.errors.NotFound:
            cfg = self.bot.get_cog('Config')
            log_channel = guild.get_channel(cfg.log)
            if log_channel is not None:
                now = datetime.datetime.now()
                account_age = now - member.created_at
                account_age = str(account_age).split(" ")[0]
                joined_time = now.strftime("%d/%m/%Y %H:%M:%S")
                Log = discord.Embed(description = f"**Evento**: {member.mention} è uscito al server", colour = discord.Colour.dark_red())
                Log.set_author(name = member, icon_url = member.avatar_url)
                Log.add_field(name = "Nome", value = member, inline=True)
                Log.add_field(name = "ID", value = f"`{member.id}`", inline=True)
                Log.add_field(name = "Età account", value = f"**{account_age}** giorni", inline=True)
                Log.add_field(name = "Orario", value = joined_time, inline=True)
                await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.staffroom)
        if log_channel is not None:
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            user_roles = []
            if user in guild.members:
                if len(user.roles) > 0:
                    for i in user.roles:
                        user_roles.append(i.name)
                else:
                    user_roles.append('_Nessun ruolo._')
            else:
                user_roles.append('_Nessun ruolo._')
            motivo = await guild.fetch_ban(user)
            Log = discord.Embed(description= f"**Azione**: {user.mention} è stato bannato dal server.", colour = discord.Colour.red())
            Log.set_author(name = user, icon_url = user.avatar_url)
            Log.add_field(name = "Nome", value = user, inline=True)
            Log.add_field(name = "ID", value = f"`{user.id}`", inline=True)
            Log.add_field(name = "Ruoli", value = "".join(user_roles), inline=False)
            Log.add_field(name = "Motivo", value = motivo.reason if motivo.reason else '_Non specificato_', inline=True)
            Log.add_field(name = "Orario", value = time, inline=True)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.staffroom)
        if log_channel is not None:
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            Log = discord.Embed(description= f"**Azione**: {user.mention} è stato sbannato dal server.", colour = discord.Colour.green())
            Log.set_author(name = user, icon_url = user.avatar_url)
            Log.add_field(name = "Nome", value = user, inline=True)
            Log.add_field(name = "ID", value = f"`{user.id}`", inline=True)
            Log.add_field(name = "Orario", value = time, inline=False)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            Log = discord.Embed(description = f"**Azione**: Messaggio di {message.author.mention} cancellato in {message.channel.mention}", colour = discord.Colour.dark_purple())
            Log.set_author(name = message.author, icon_url = message.author.avatar_url)
            Log.add_field(name = "Testo", value = message.content, inline=False)
            Log.add_field(name = "Autore messaggio", value = message.author, inline=True)
            Log.add_field(name = "ID messaggio", value = f"`{message.id}`", inline=True)
            Log.add_field(name = "⠀", value = "⠀", inline=True)
            Log.add_field(name = "Canale", value = message.channel.mention, inline=True)
            Log.add_field(name = "ID Canale", value = f"`{message.channel.id}`", inline=True)
            Log.add_field(name = "⠀", value = "⠀", inline=True)
            try:
                await log_channel.send(embed = Log)
            except discord.errors.HTTPException:
                pass


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot == False:
            guild = before.guild
            cfg = self.bot.get_cog('Config')
            log_channel = guild.get_channel(cfg.log)
            if log_channel is not None:
                Log = discord.Embed(description = f"**Azione**: {before.author.mention} ha modificato il suo messaggio", colour = discord.Colour.from_rgb(66, 197, 245))
                Log.set_author(name = before.author, icon_url = before.author.avatar_url)
                Log.add_field(name = "Canale", value = before.channel.mention, inline=True)
                Log.add_field(name = "Message", value = f"[[Link](https://discordapp.com/channels/{before.guild.id}/{before.channel.id}/{before.id} 'Clicca qui per andare al messaggio editato.')]", inline=True)
                Log.add_field(name = "Vecchio testo", value = before.content, inline=False)
                Log.add_field(name = "Nuovo testo", value = after.content, inline=False)
                await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            Log = discord.Embed(description = f"**Azione**: Nuovo canale creato", colour = discord.Colour.from_rgb(235, 174, 52))
            tipo = "Non disponibile"
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            if str(channel.type) == "voice":
                tipo = "Vocale"
            elif str(channel.type) == "text":
                tipo = "Testuale"
            elif str(channel.type) == "category":
                tipo = "Categoria"
            Log.add_field(name = "Nome canale", value = channel.name, inline=True)
            if str(channel.type) == "text":
                Log.add_field(name = "Menzione canale", value = channel.mention, inline=True)
            Log.add_field(name = "Tipo canale", value = tipo, inline=True)
            Log.add_field(name = "ID canale", value = f"`{channel.id}`", inline=False)
            Log.add_field(name = "Orario azione", value = time, inline=False)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            Log = discord.Embed(description = f"**Azione**: Canale cancellato", colour = discord.Colour.from_rgb(125, 235, 52))
            tipo = "Non disponibile"
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            if str(channel.type) == "voice":
                tipo = "Vocale"
            elif str(channel.type) == "text":
                tipo = "Testuale"
            elif str(channel.type) == "category":
                tipo = "Categoria"
            Log.add_field(name = "Nome canale", value = channel.name, inline=True)
            Log.add_field(name = "Tipo canale", value = tipo, inline=True)
            Log.add_field(name = "ID canale", value = f"`{channel.id}`", inline=False)
            Log.add_field(name = "Orario azione", value = time, inline=False)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            guild = before.guild
            cfg = self.bot.get_cog('Config')
            log_channel = guild.get_channel(cfg.log)
            if log_channel is not None:
                now = datetime.datetime.now()
                time = now.strftime("%d/%m/%Y %H:%M:%S")
                Log = discord.Embed(description = f"**Azione**: nickname di {before.mention} modificato", colour = discord.Colour.from_rgb(52, 159, 235))
                Log.set_author(name = before, icon_url = before.avatar_url)
                Log.add_field(name = "Vecchio nick", value = before.nick if before.nick else before.name, inline=True)
                Log.add_field(name = "Nuovo nick", value = after.nick if after.nick else before.name, inline=True)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)

        if before.roles != after.roles:
            cfg = self.bot.get_cog('Config')
            log_channel = self.bot.get_channel(cfg.log)
            if log_channel is not None:
                new_roles = []
                removed_roles = []
                total_roles = []
                for new_role in after.roles:
                    if new_role not in before.roles:
                        new_roles.append(new_role.name)
                for removed_role in before.roles:
                    if removed_role not in after.roles:
                        removed_roles.append(removed_role.name)
                for role in after.roles:
                    if not role.is_default():
                        total_roles.append(f"`{role.name}`")
                if len(new_roles) == 0:
                    new_roles.append("_Nessun ruolo aggiunto._")
                if len(removed_roles) == 0:
                    removed_roles.append("_Nessun ruolo rimosso._")
                now = datetime.datetime.now()
                time = now.strftime("%d/%m/%Y %H:%M:%S")
                Log = discord.Embed(description = f"**Azione**: ruoli di {before.mention} aggiornati", colour = discord.Colour.from_rgb(52, 235, 229))
                Log.set_author(name = before, icon_url = before.avatar_url)
                Log.add_field(name = "Ruoli aggiunti", value = "\n".join(new_roles), inline=True)
                Log.add_field(name = "Ruoli rimossi", value = "\n".join(removed_roles), inline=True)
                Log.add_field(name = "Ruoli attuali", value = "\n".join(total_roles), inline=False)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        guild = before.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")

            if before.name != after.name:
                Log = discord.Embed(description = f"**Azione**: nome server modificato", colour = discord.Colour.from_rgb(52, 159, 235))
                Log.set_author(name = before.name, icon_url = before.icon_url)
                Log.add_field(name = "Vecchio nome", value = before.name, inline=True)
                Log.add_field(name = "Nuovo nome", value = after.name, inline=True)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)
            elif before.afk_channel != after.afk_channel:
                Log = discord.Embed(description = f"**Azione**: afk-room server modificata", colour = discord.Colour.magenta())
                Log.set_author(name = before.name, icon_url = before.icon_url)
                Log.add_field(name = "Vecchia stanza", value = f"{before.afk_channel.name} (`{before.afk_channel.id}`)", inline=True)
                Log.add_field(name = "Nuova stanza", value = f"{after.afk_channel.name} (`{after.afk_channel.id}`)", inline=True)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        guild = invite.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            Log = discord.Embed(description = f"**Azione**: {invite.inviter.mention} ha creato un invito", colour = discord.Colour.from_rgb(235, 52, 128))
            Log.set_author(name = invite.inviter, icon_url = invite.inviter.avatar_url)
            Log.add_field(name = "Codice invito", value = f"`{invite.code}`", inline=True)
            Log.add_field(name = "Durata invito", value = f"{f'{invite.max_age} s' if invite.max_age != 0 else 'Permanente'}", inline=True)
            Log.add_field(name = "Utilizzi", value = f"{invite.uses}/{invite.max_uses if invite.max_uses != 0 else 'Infiniti'}", inline=True)
            Log.add_field(name = "Unione temporanea", value = 'Si' if invite.temporary == True else 'No', inline=True)
            Log.add_field(name = "Canale invito", value = invite.channel.mention)
            Log.add_field(name = "Orario azione", value = time, inline=False)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        guild = invite.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.log)
        if log_channel is not None:
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")
            Log = discord.Embed(description = f"**Azione**: invito cancellato", colour = discord.Colour.from_rgb(235, 52, 128))
            Log.add_field(name = "Codice invito", value = f"`{invite.code}`", inline=True)
            Log.add_field(name = "Canale invito", value = invite.channel.mention, inline=True)
            Log.add_field(name = "Orario azione", value = time, inline=False)
            await log_channel.send(embed = Log)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        cfg = self.bot.get_cog('Config')
        log_channel = guild.get_channel(cfg.voicelogs)
        if log_channel is not None:
            now = datetime.datetime.now()
            time = now.strftime("%d/%m/%Y %H:%M:%S")

            if before.channel is None and after.channel is not None: # Utente si è connesso
                Log = discord.Embed(description = f"**Azione**: {member.mention} si è connesso a {after.channel.name}", colour = discord.Colour.from_rgb(3, 252, 32))
                Log.set_author(name = member, icon_url = member.avatar_url)
                Log.add_field(name = "Nome Canale", value = after.channel.name, inline=True)
                Log.add_field(name = "ID Canale", value = f"`{after.channel.id}`", inline=True)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)

            elif after.channel is None and before.channel is not None: # Utente si è disconnesso
                Log = discord.Embed(description = f"**Azione**: {member.mention} disconnesso da {before.channel.name}", colour = discord.Colour.from_rgb(252, 3, 3))
                Log.set_author(name = member, icon_url = member.avatar_url)
                Log.add_field(name = "Nome Canale", value = before.channel.name, inline=True)
                Log.add_field(name = "ID Canale", value = f"`{before.channel.id}`", inline=True)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)

            elif before.channel != after.channel and before.channel is not None and after.channel is not None: # Utente ha cambiato stanza
                Log = discord.Embed(description = f"**Azione**: {member.mention} spostato da {before.channel.name} a {after.channel.name}", colour = discord.Colour.from_rgb(252, 186, 3))
                Log.set_author(name = member, icon_url = member.avatar_url)
                Log.add_field(name = "Vecchio canale", value = f"{before.channel.name} (`{before.channel.id}`)", inline=True)
                Log.add_field(name = "Nuovo canale", value = f"{after.channel.name} (`{after.channel.id}`)", inline=False)
                Log.add_field(name = "Orario azione", value = time, inline=False)
                await log_channel.send(embed = Log)






def setup(bot):
    bot.add_cog(Logger(bot))
    print("[!] modulo logger caricato")
