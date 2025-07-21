import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor

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

# theory
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

# max_id()
conn = psycopg2.connect(
       dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT 
    )
# begin
# practice
def get_order_sum(conn, month):
    query = """SELECT
                customer_name,
                EXTRACT(MONTH FROM order_date) as month,
                SUM(total_amount)
            FROM orders AS o
            JOIN customers AS c
            ON o.customer_id = c.customer_id
            GROUP BY customer_name, order_date
            HAVING EXTRACT(MONTH FROM order_date) = %s;"""
    result = []

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(query, (month,))
        rows = cur.fetchall()
        for row in rows:
            text = f'Покупатель {row[0]} совершил покупок на сумму {row[2]}'
            result.append(text)
    result = '\n'.join(result)

    print(result)
    return result

# end
get_order_sum(conn, 2)
conn.close()