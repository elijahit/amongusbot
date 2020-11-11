from sqlite3 import connect, Error

from discord.ext import commands


class Db(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        databaseuri = 'cogs/databaseserver.db'

        try:
            self.Database = connect(databaseuri)
            self.Cursor = self.Database.cursor()

            print("[!] Connessione al database stabilita.")
            self.Cursor.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, channel_id, admin_id)")
            self.Cursor.execute("CREATE TABLE IF NOT EXISTS warns (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, user_id INTEGER, gravity INTEGER, reason TEXT)")
            self.Cursor.execute("CREATE TABLE IF NOT EXISTS scheduled_tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, channel_id INTEGER, text TEXT, freq TEXT)")
            # TODO
            # self.Cursor.execute("CREATE TABLE IF NOT EXISTS poll ()")
        except Error:

            print(Error)

    def field(self, command, *values):
        self.Cursor.execute(command, tuple(values))
        fetch = self.Cursor.fetchone()

        if fetch is not None:
            return fetch[0]

    def one_record(self, command, *values):
        self.Cursor.execute(command, tuple(values))
        return self.Cursor.fetchone()

    def records(self, command, *values):
        self.Cursor.execute(command, tuple(values))
        return self.Cursor.fetchall()

    def column(self, command, *values):
        self.Cursor.execute(command, tuple(values))
        return [item[0] for item in self.Cursor.fetchall()]

    def execute(self, command, values):
        self.Cursor.execute(command, values)

    def executeone(self, command):
        self.Cursor.execute(command)

    def fetchall(self, command, values):
        self.Cursor.execute(command, values)
        return self.Cursor.fetchall()

    def fetchallnovalues(self, command):
        self.Cursor.execute(command)
        return self.Cursor.fetchall()

    # def update(self):
    #     for Member in Guild.members:
    #         database.execute("INSERT OR IGNORE INTO users (ID) VALUES (?)", Member.id)
    #     for userid in database.column("SELECT ID from users"):
    #         if Guild.get_member(userid) is None:
    #             database.execute("DELETE FROM users WHERE ID = ?", userid)
    #     self.Database.commit()
    #     return

    async def commit(self):
        self.Database.commit()
        return

    def disconnect(self):
        self.Database.close()
        return


def setup(bot):
    bot.add_cog(Db(bot))
    print("[!] modulo db caricato")
