from db_connection import get_connection


def get_error():    
    conn = get_connection()
    query_select = """SELECT * FROM users;"""
    query_insert = """INSERT INTO users (username, phone) VALUES ('tommy2', '12223456789');"""

    cursor = conn.cursor()
    cursor.execute(query_select)
    rows = cursor.fetchall()
    print(rows)
    cursor.execute(query_insert)
    
    raise Exception("Ошибка во время транзакции")
    
    conn.commit()
    conn.close()

get_error()

