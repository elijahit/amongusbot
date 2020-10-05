from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

        self.aiutoadmin = "•[3 +] **editmsg** (idmsg) (testo) \n*[Edita un messaggio inviato con tsay]*\n\
•[2 +] **purgeinvite** \n*[Cancella tutti gli inviti al server]*\n\
•[5 +] **tuser** (@user) (testo) \n*[Invia EMBED a un utente]*\n\
•[5 +] **purge** (valore=max200) \n*[Elimina messaggi]*\n\
•[5 +] **tsay** (testo) \n*[Scrivi in chat]*\n"

        self.aiutoadmin2 = "•[6 +] **ban** (@user) (motivo) \n*[Banna un utente]*\n\
•[6 +] **kick** (@user) (motivo) \n*[Kicka un utente dal server]*\n"

        self.aiutoadmin3 = "•[8 +] **mvto** (nome stanza) (@user @user) \n*[Sposta gli utenti in una stanza specifica]*\n\
•[8 +] **mvhere** (@user @user) \n*[Sposta gli utenti nella stanza dove ti trovi]*\n\
•[8 +] **hackhelp** \n*[Lista comandi controllo hack]*\n\
•[8 +] **addreact** (idmsg) (emoij) \n*[Aggiungi reazione]*\n\
•[8 +] **muteroom** (nome stanza) o muteroom \n*[Silenzia una stanza VoiP]*\n\
•[8 +] **unmuteroom** (nome stanza) o unmuteroom \n*[Attiva il VoiP in una stanza]*\n\
•[9 +] **find** (@user) \n*[Ricerca user in stanza VoiP]*\n\
•[9 +] **tickethelp** \n*[Lista comandi ticket]*\n"

        self.aiuto = "aiuto **[Mostra la lista dei comandi]**\n\
            insulta (utente) (M/F) **[Insulto random, definire se maschile o femminile]**"

        self.log = 751068836626956350 #Canale logs
        self.sanzioni = 757000456261206057 #canale sanzioni
        self.ingresso = 744613754829799444 #canale ingresso
        self.voicelogs = 751077692446736444 #canale voicelogs
        self.categories = ["TESTVOIP", "APEX"]

        ##ADMIN PEX 

        
        self.roledev = 758086640047620136 #3rd Party
        self.rolea1 = 744631580504359043 #Owner
        self.rolea2 = 744631542608822422 # Admin
        self.rolea3 = 762459421665525802 # Senior Mod
        self.rolea4 = 744631301872680980 # Mod
        self.rolea5 = 762459426128789525 # Senior Helper
        self.rolea6 = 754829854066737182 # Helper
        self.rolea7 = 762459428402233355 # Trial Helper
        self.rolea8 = 762459430528483359 # Gestore
        self.rolea9 = 762460098286190593 # Prova

        self.rolea_all = set((self.rolea1, self.rolea2, self.rolea3, self.rolea4, self.rolea5, self.rolea6, self.rolea7, self.rolea8, self.rolea9, self.roledev))
        self.rolea_top8 = set((self.rolea1, self.rolea2, self.rolea3, self.rolea4, self.rolea5, self.rolea6, self.rolea7, self.rolea8, self.roledev))
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

        self.IDruoliDev = (758086249436151908, 758086640047620136) # id dei ruoli dei dev nel server test (gestore dev, dev) per il server principale cambiarli in (758086249436151908, 758086640047620136)









def setup(bot):
    bot.add_cog(Config(bot))
    print("[!] modulo config caricato")
