import sqlite3
from models.db_utils import get_connection

def get_matches():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    SELECT
        g.id AS game_id,
        t1.player_id_1 AS t1_p1, t1.player_id_2 AS t1_p2,
        t2.player_id_1 AS t2_p1, t2.player_id_2 AS t2_p2,
        g.status, g.court
    FROM games g
    JOIN teams t1 ON g.team_id_1 = t1.id
    JOIN teams t2 ON g.team_id_2 = t2.id
    """

    cursor.execute(query)
    matches = cursor.fetchall()

    conn.close()
    return matches

def give_court():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    INSERT INTO games(id, courts) VALUES (?, ?)
    """

    cursor.execute(query, game_id, courts)