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
    matches = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM status")
    status_list = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return matches, status_list

def give_court(game_id, court_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        check_query = "SELECT id FROM games WHERE court = ? AND [status] = 1"
        cursor.execute(check_query, (court_id,))
        existing_matches = cursor.fetchone()

        if existing_matches:
            return {"status": "error", "message": f"Baan {court_id} is al bezet door game {existing_matches['id']}"}

        update_query = "UPDATE games SET court = ? WHERE id = ?"
        cursor.execute(update_query, (court_id, game_id))
        conn.commit()
        return {"status": "success", "message": f"Baan {court_id} is gegeven aan {game_id}"}

    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()