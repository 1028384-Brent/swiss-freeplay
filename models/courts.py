from models.db_utils import get_connection

def get_courts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('select id, name, number from courts')
    courts = cursor.fetchall()

    court_list = []
    for row in courts:
        court_list.append({
            'id': row[0],
            'name': row[1],
            'number': row[2]
        })

    conn.close()
    return court_list