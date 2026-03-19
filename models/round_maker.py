from db_utils import get_connection

def create_teams():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM teams')
    team_count = cursor.fetchone()[0]

    if team_count == 0:
        print("No teams found. Creating new teams.")

        cursor.execute("SELECT id, level FROM players WHERE gender = 1 ORDER BY level")
        male_players = cursor.fetchall()

        cursor.execute("SELECT id, level FROM players WHERE gender = 2 ORDER BY level")
        female_players = cursor.fetchall()

        teams = []
        def pair_players(player_list):
            temp_teams = []

            if len(player_list) % 2 != 0:
                player_list.pop()

            for i in range(0, len(player_list), 2):
                p1 = player_list[i][0]
                p2 = player_list[i+1][0]
                temp_teams.append((p1, p2))

            return temp_teams

        teams.extend(pair_players(male_players))
        teams.extend(pair_players(female_players))

        cursor.executemany("INSERT INTO teams (player_id_1, player_id_2) VALUES (?, ?)",
                           teams)

        print(f"{len(teams)} teams created.")

    else:
        print("Team already exists.")

    conn.commit()
    conn.close()

create_teams()

def create_matches():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM teams')
    teams = [row[0] for row in cursor.fetchall()]

    if len(teams) %2 != 0:
        teams = teams[:-1]

    games = []

    for i in range (0, len(teams), 2):
        t1 = teams[i]
        t2 = teams[i+1]
        games.append((t1, t2))

    cursor.executemany("""
    INSERT INTO games (team_id_1, team_id_2, [status]) 
    VALUES (?, ?, 2)
    """, games)

    conn.commit()
    conn.close()

    print(f"{len(games)} games created.")

create_matches()