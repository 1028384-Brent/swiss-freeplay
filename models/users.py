import hashlib
from .db_utils import get_connection

def check_login(username, password):
    hashed_input = hashlib.sha256(password.encode('utf-8')).hexdigest()

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT username FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, hashed_input))
    user = cursor.fetchone()

    conn.close()
    return user