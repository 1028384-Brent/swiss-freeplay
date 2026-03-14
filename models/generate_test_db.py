import sqlite3
import os
import hashlib

db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.db')

def create_test_db(db_file):
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    ''')

    username = 'test'
    password = 'test'
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)
    ''', (username, hashed_password))

    cursor.execute('''CREATE TABLE IF NOT EXISTS gender (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT)''')

    cursor.execute('''INSERT INTO gender (gender) VALUES ('male')''')
    cursor.execute('''INSERT INTO gender (gender) VALUES ('female')''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    level INTEGER,
    gender INTEGER,
    FOREIGN KEY(gender) REFERENCES gender (id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id_1 INTEGER,
    player_id_2 INTEGER,
    FOREIGN KEY(player_id_1) REFERENCES players (id),
    FOREIGN KEY(player_id_2) REFERENCES players (id)
    )''')


    cursor.execute('''CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
    )''')
    cursor.execute('''INSERT INTO status (name) VALUES ('playing') ''')
    cursor.execute('''INSERT INTO status (name) VALUES ('planned') ''')
    cursor.execute('''INSERT INTO status (name) VALUES ('finished') ''')

    cursor.execute("""CREATE TABLE IF NOT EXISTS courts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    number INTEGER
    )""")

    cursor.execute('''CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id_1 INTEGER,
    team_id_2 INTEGER,
    score_team_1 INTEGER,
    score_team_2 INTEGER,
    status INTEGER,
    court INTEGER,
    FOREIGN KEY(court) REFERENCES courts (id),
    FOREIGN KEY(status) REFERENCES status (id),
    FOREIGN KEY(team_id_1) REFERENCES teams (id),
    FOREIGN KEY(team_id_2) REFERENCES teams (id)
    )''')



    conn.commit()
    cursor.close()
    conn.close()
    print('Database created.')

create_test_db(db_file)