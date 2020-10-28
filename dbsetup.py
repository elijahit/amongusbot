import sqlite3

create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                    channel_id integer,
                                    user_id integer
                                ); """

create_tickets_table = """CREATE TABLE IF NOT EXISTS tickets (
                                id integer PRIMARY KEY,
                                name text,
                                creato text,
                                joined text
                                
                            );"""

create_addrole_table = """CREATE TABLE IF NOT EXISTS addrole (
                                id integer PRIMARY KEY,
                                role_id integer
                                
                            );"""

if __name__ == '__main__':
    database = 'cogs/database.db'
    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute(create_users_table)
    cursor.execute(create_tickets_table)
    cursor.execute(create_addrole_table)
    connection.commit()
    connection.close()
