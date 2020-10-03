from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

        self.aiutoadmin = "•[2 +] it!ban (@user) (motivo) **[Banna un utente]**\n\
•[2 +] it!addreact (idmsg) (emoij) **[Aggiungi reazione]**\n\
•[3 +] it!kick (@user) (motivo) **[Kicka un utente dal server]**\n\
•[3 +] it!editmsg (idmsg) (testo) **[Edita un messaggio inviato con it!tsay]**\n\
•[5 +] it!t (titolo) (testo) **[Invia EMBED nel canale]**\n\
•[5 +] it!tuser (@user) (testo) **[Invia EMBED a un utente]**\n\
•[5 +] it!tsay (testo) **[Scrivi in chat]**\n\
•[6 +] it!banlist **[Lista ban]**\n\
•[6 +] it!purge (valore=max200) **[Elimina messaggi]**\n\
•[6 +] it!mvto (nome stanza) (@user @user) **[Sposta gli utenti in una stanza specifica]**\n\
•[6 +] it!mvhere (@user @user) **[Sposta gli utenti nella stanza dove ti trovi]**\n\
•[6 +] it!tickethelp **[Lista comandi ticket]**\n\
•[6 +] it!hackhelp **[Lista comandi controllo hack]**\n\
•[6 +] it!find (@user) **[Ricerca user in stanza VoiP]**\n\
•[6 +] it!muteroom (nome stanza) o it!muteroom **[Silenzia una stanza VoiP]**\n\
•[6 +] it!unmuteroom (nome stanza) o it!unmuteroom **[Attiva il VoiP in una stanza]**"

        self.aiuto = "it!aiuto **[Mostra la lista dei comandi]**\n\
            it!insulta (utente) (M/F) **[Insulto random, definire se maschile o femminile]**"

        self.log = 757654227668697206 #Canale logs
        self.sanzioni = 757654227668697206 #canale sanzioni
        self.rolech = 705563701297676319 #canale ruoli
        self.lfg = 709814722668527617 #canale lfg
        self.nickname = 702555500041994330 #canale nickname
        self.generale = 701594074464911410 #canale generale
        self.ingresso = 760287555626860554 #canale ingresso
        self.voicelogs = 757654227668697205 #canale voicelogs
        self.categories = ["TESTVOIP", "APEX"]

        ##ADMIN PEX
        self.rolea1 = "Tester"
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

        self.IDruoliDev = (757654227215712423, 757654227215712422) # id dei ruoli dei dev nel server test (gestore dev, dev) per il server principale cambiarli in (758086249436151908, 758086640047620136)









def setup(bot):
    bot.add_cog(Config(bot))
    print("[!] modulo config caricato")
