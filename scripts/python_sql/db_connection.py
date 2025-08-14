import psycopg2

DB_NAME = "python_sql"
DB_USER = "alex"
DB_HOST = "localhost"
DB_PORT = "5432"


def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            port=DB_PORT
            )
        return conn
    except psycopg2.Error:
        print("Can`t establish connection to database: {e}")
        return None
