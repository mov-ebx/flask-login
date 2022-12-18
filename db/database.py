import sqlite3

database = sqlite3.connect('user.db', check_same_thread=False)

def create():
    database.execute("""
    CREATE TABLE IF NOT EXISTS DATA (
        USERID INT NOT NULL,
        USERNAME TEXT NOT NULL,
        NAME TEXT,
        EMAIL TEXT,
        PASSWORD TEXT NOT NULL,
        AUTH TEXT NOT NULL,
        ROLE TEXT NOT NULL
    );
    """)

def reset():
    database.execute('DROP TABLE DATA')
    create()

create()