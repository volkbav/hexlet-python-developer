import psycopg2

with psycopg2.connect(
     dbname="python_sql",
        user="alex",
        password="ghbdtn",
        host="88.210.52.150",
        port="5432"
) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users;")
        print(cur.fetchall())
    