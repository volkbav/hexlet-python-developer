import psycopg2
from psycopg2.extras import execute_batch, execute_values, RealDictCursor, NamedTupleCursor, LoggingCursor

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


def all_users():
    with psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    ) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            cur.execute("SELECT * FROM users;")
            all_users = cur.fetchall()
    print(all_users)

# all_users()


def max_id():
    with psycopg2.connect(
       dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT 
    ) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
            query = """SELECT MAX(id) from users;"""
            cur.execute(query)
            max_id = cur.fetchall()
    print(max_id)

max_id()