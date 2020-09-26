from discord.ext import commands
from sqlite3 import connect, Error
import os


class db(commands.Cog):
    def __init__(self, bot):
        

        try:
            self.Database = connect('file:C:/Users/Gabriele/Desktop/Workstation/newbot/cogs/database.db?mode=rw', uri=True)
            self.Cursor = self.Database.cursor()

            print("[!] Connessione al database stabilita.")

        except Error:

            print(Error)


        class database:
            def field(self, command, *valore):
                Cursor.execute(command, tuple(valore))
                fetch = Cursor.fetchone()
                if fetch is not None:
                    return fetch[0]
                return


            def one_record(self, command, *valore):
                Cursor.execute(command, tuple(valore))
                return Cursor.fetchone()

            def records(self, command, *valore):
                Cursor.execute(command, tuple(valore))
                return Cursor.fetchall()

            def column(self, command, *valore):
                Cursor.execute(command, tuple(valore))
                return [item[0] for item in Cursor.fetchall()]
                
            def execute(self, command, *valore):
                Cursor.execute(command, tuple(valore))
                return

            def update(self):
                for Member in Guild.members:
                    database.execute("INSERT OR IGNORE INTO users (ID) VALUES (?)", Member.id)
                for userid in database.column("SELECT ID from users"):
                    if Guild.get_member(userid) is None:
                        database.execute("DELETE FROM users WHERE ID = ?", userid)
                self.Database.commit()
                return


            async def commit(self):
                self.Database.commit()
                return

            def disconnect(self):
                self.Database.close()
                return




def setup(bot):
    bot.add_cog(db(bot))
    print("[!] modulo db caricato")
