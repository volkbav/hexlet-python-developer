import os
import secrets
import json

# import psycopg2
# from psycopg2.extras import DictCursor
# from .db_connection import get_connection


DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "users.json"
)

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
    def __init__(self, file_path=DATA_FILE):
        self.file_path = file_path
    
    def validate(self, data, current_id=None):
        errors = {}
        # nickname
        if not data["name"]:
            errors["name"] = "Can't be blank"
        elif len(data["name"]) < 4:
            errors["name"] = "Nickname must be grater than 4 characters" 
        # email        
        if not data["email"]:
            errors["email"] = "Can't be blank"
        elif len(data["email"]) < 4:
            errors["email"] = "Email must be grater than 4 characters"
        else:
            for user in self._read():
        # если email совпадает и это не текущий пользователь → ошибка
                if user["email"] == data["email"] and user["id"] != int(current_id or -1):
                    errors["email"] = "This email already exists"
                    break
        return errors

    def _read(self):
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
        return data

    def _write(self, data):
        repo = self._read()
        repo.append(data)
        with open(DATA_FILE, "w") as f:
            json.dump(repo, f, ensure_ascii=False, indent=4)

    def find(self, id):
        repo = self._read()
        for u in repo:
            if u["id"] == int(id):
                return u
        return None

    def update(self, id, new_data):
        repo = self._read()
        for i, u in enumerate(repo):
            if u["id"] == int(id):
                new_data["id"] = int(id)   # сохраняем id
                repo[i] = new_data
                break
        with open(DATA_FILE, "w") as f:
            json.dump(repo, f, ensure_ascii=False, indent=4)


    def delete(self, id):
        repo = self._read()
        new_data = []
        for i, u in enumerate(repo):
            if u["id"] != int(id):
                new_data.append(repo[i])
        with open(DATA_FILE, "w") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
    
    def get_all(self):
        return self._read()
