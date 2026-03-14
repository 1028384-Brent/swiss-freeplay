import os
import sqlite3

DB_path = os.path.join(os.path.dirname(__file__), 'test.db')

def get_connection(db_file = DB_path):
    conn = sqlite3.connect(db_file)
    return conn