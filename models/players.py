from models.db_utils import get_connection

def get_players():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('select * from players')
    players = cursor.fetchall()

    conn.close()
    return players