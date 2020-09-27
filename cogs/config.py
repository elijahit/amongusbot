from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

        self.aiutoadmin = "**[1]** server query **|** **[2]** Amministratore **|** **[3]** Coach **|** **[4]** TBA **|** **[5]** TBA **|** **[6]** Senior\n\
•[2 +] !ban (@user) (motivo) **[Banna un utente]**\n\
•[2 +] !addreact (idmsg) (emoij) **[Aggiungi reazione]**\n\
•[3 +] !kick (@user) (motivo) **[Kicka un utente dal server]**\n\
•[3 +] !editmsg (idmsg) (testo) **[Edita un messaggio inviato con !tsay]**\n\
•[5 +] !t (titolo) (testo) **[Invia EMBED nel canale]**\n\
•[5 +] !tuser (@user) (testo) **[Invia EMBED a un utente]**\n\
•[5 +] !tsay (testo) **[Scrivi in chat]**\n\
•[6 +] !warn (@user) (motivo) **[Warna un utente]**\n\
•[6 +] !banlist **[Lista ban]**\n\
•[6 +] !purge (valore=max200) **[Elimina messaggi]**\n\
•[6 +] !mvto (nome stanza) (menzione utenti) **[Sposta gli utenti in una stanza specifica]**\n\
•[6 +] !mvhere (menzione utenti) **[Sposta gli utenti nella stanza dove ti trovi]**\n\
•[6 +] !tickethelp **[Lista comandi ticket]**\n\
•[6 +] !hackhelp **[Lista comandi ticket]**"

        self.log = 757654227668697206 #Canale logs
        self.sanzioni = 757654227668697206 #canale sanzioni
        self.rolech = 705563701297676319 #canale ruoli
        self.lfg = 709814722668527617 #canale lfg
        self.nickname = 702555500041994330 #canale nickname
        self.generale = 701594074464911410 #canale generale
        self.ingresso = 757654227668697203 #canale ingresso
        self.categories = ["TESTVOIP", "APEX"]

        ##ADMIN PEX
        self.rolea1 = "Support Team"
        self.rolea2 = "TBA"
        self.rolea3 = "TBA"
        self.rolea4 = "TBA"
        self.rolea5 = "TBA"
        self.rolea6 = "TBA"
        ##

        #controllo parole scurrilid
        self.badwords = []

        #DEFINE COLORI
        self.lightgreen = 0xc3eb34
        self.red = 0x912519
        self.blue = 0x3268a8
        self.green = 0x008000

        self.autorole = 44444

        self.footer = "Among Us Ita 0.1 **beta**"








def setup(bot):
    bot.add_cog(Config(bot))
    print("[!] modulo config caricato")
