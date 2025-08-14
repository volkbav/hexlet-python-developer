from psycopg2 import connect
from .psycopg2.extras import execute_batch, execute_values

DB_NAME = "python_sql"
DB_USER = "alex"
DB_HOST = "88.210.52.150"
DB_PORT = "5432"

tuple_users = (
    ("Bob", "111111"),
    ("Alice", "2222222"),
    ("John", "3333333"),
)
list_users = [
    ("Bob", "444444"),
    ("Alice", "5555555"),
    ("John", "666666"),
]


def insert_users(users_data):
    with connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    ) as conn:
        with conn.cursor() as cur:
            if isinstance(users_data, tuple):
                query = """INSERT INTO users (username, phone)
                            VALUES (%s, %s)
                            RETURNING username, phone;"""
                execute_batch(cur, query, users_data)
            elif isinstance(users_data, list):
                query = """INSERT INTO users (username, phone)
                            VALUES %s;"""
                execute_values(cur, query, users_data)
        conn.commit
            
def delete_users(name):
    with connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    ) as conn:
        with conn.cursor() as cur:
            query = """DELETE FROM users
            WHERE username=%s"""
            cur.execute(query, (name,))
        conn.commit

def print_users():
    with connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    ) as conn:
        with conn.cursor() as cur:
            query = "SELECT * FROM users;"
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                print(row)


#insert_users(tuple_users)
#insert_users(list_users)
#print(print_users())

delete_users("John")
delete_users("Alice")
delete_users("Bob")
print(print_users())
