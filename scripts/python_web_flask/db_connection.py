import psycopg2
import os



def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT"))
            )
        return conn
    except psycopg2.Error:
        print("Can`t establish connection to database: {e}")
        return None
