import sqlite3
import os
import hashlib

db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tournament.db')

def create_test_db_schema(cursor):
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
        )''')

    username = 'test'
    password = 'test'
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

    cursor.execute('CREATE TABLE IF NOT EXISTS gender (id INTEGER PRIMARY KEY AUTOINCREMENT, gender TEXT)')
    cursor.execute("INSERT INTO gender (gender) VALUES ('male')")
    cursor.execute("INSERT INTO gender (gender) VALUES ('female')")

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

    cursor.execute('CREATE TABLE IF NOT EXISTS status (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
    cursor.executemany("INSERT INTO status (name) VALUES (?)", [('playing',), ('planned',), ('finished',)])

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS courts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, number INTEGER)")

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


def test_players(cursor):
    print('Populating test players...')
    players = []
    # male players
    for i in range(50):
        players.append((f'male_player{i + 1}', (i % 10) + 1, 1))
    # female players
    for i in range(50):
        players.append((f'female_player{i + 1}', (i % 10) + 1, 2))

    cursor.executemany('INSERT INTO players (name, level, gender) VALUES (?, ?, ?)', players)

def test_courts(cursor):
    print('Populating test courts...')
    animal_courts = [
        ("Lion Court", 1), ("Tiger Court", 2), ("Eagle Court", 3), ("Shark Court", 4),
        ("Panther Court", 5), ("Wolf Court", 6), ("Falcon Court", 7), ("Bear Court", 8)
    ]
    cursor.executemany("INSERT INTO courts (name, number) VALUES (?, ?)", animal_courts)

def run_setup():
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
        except PermissionError:
            print("--- CRITICAL ERROR ---")
            print(f"Failed to remove {db_file}")
            return
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            create_test_db_schema(cursor)
            test_players(cursor)
            test_courts(cursor)

            conn.commit()
            print("All setup tasks completed successfully")
    except sqlite3.Error as e:
        print(e)

if __name__ == '__main__':
    run_setup()