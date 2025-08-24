import os
import secrets
import json

import psycopg2
from psycopg2.extras import DictCursor


# file as DB
"""
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "users.json"
)
"""

SECRET_FILE = os.path.join(os.path.dirname(__file__), "secret_key.txt")


def get_secret_key():
    if os.path.exists(SECRET_FILE):
        with open(SECRET_FILE, "r") as f:
            secret_key = f.read().strip()
    else:
        secret_key = secrets.token_hex(16)
        with open(SECRET_FILE, "w") as f:
            f.write(secret_key)
    return secret_key


class UserRepository:
    def __init__(self, conn):
        self.conn = conn
    
    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users")
            return [dict(row) for row in cur]

    def validate(self, data, current_id=None):
        errors = {}

        # nickname
        if not data.get("nickname"):
            errors["nickname"] = "Can't be blank"
        elif len(data["nickname"]) < 4:
            errors["nickname"] = "Nickname must be greater than 4 characters"

        # email        
        if not data.get("email"):
            errors["email"] = "Can't be blank"
        elif len(data["email"]) < 4:
            errors["email"] = "Email must be greater than 4 characters"
        else:
            with self.conn.cursor(cursor_factory=DictCursor) as cur:
                if current_id:
                    # Проверка с исключением текущего пользователя
                    cur.execute(
                        "SELECT id FROM users WHERE email = %s AND id != %s",
                        (data["email"], current_id)
                    )
                else:
                    # Проверка при создании нового
                    cur.execute(
                        "SELECT id FROM users WHERE email = %s",
                        (data["email"],)
                    )
                if cur.fetchone():
                    errors["email"] = "This email already exists"

        return errors



    def save(self, user):
        if "id" in user and user["id"]:
            self._update(user)
        else:
            self._create(user)

        

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None


    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET nickname = %s, email = %s WHERE id = %s",
                (user["nickname"], user["email"], user["id"]),
            )
        self.conn.commit()

    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (nickname, email) VALUES (%s, %s) RETURNING id",
                (user["nickname"], user["email"]),
            )
            id = cur.fetchone()[0]
            user["id"] = id
        self.conn.commit()

    def get_all(self):
        return self.get_content()
    
    def delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (id,))
        self.conn.commit()
