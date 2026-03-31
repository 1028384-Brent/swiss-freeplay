from models.db_utils import get_connection

def get_players():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(""""
        SELECT 
            players.id, 
            players.name, 
            players.level, 
            gen.gender 
        FROM players 
        LEFT JOIN gender AS gen ON players.gender = gen.id;
    """)
    players = cursor.fetchall()

    conn.close()
    return players

def post_players(name, level, gender):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            INSERT INTO players (
            name,
            level,
            gender
            ) VALUES (?, ?, ?)          
        """ ,name, level, gender)
    conn.commit()
    conn.close()