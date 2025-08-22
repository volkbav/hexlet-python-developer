from flask import render_template, Flask, request, redirect, url_for, flash
import json
import os
import secrets


app = Flask(__name__)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "users.json"
)

SECRET_FILE = os.path.join(os.path.dirname(__file__), "secret_key.txt")

if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as f:
        secret_key = f.read().strip()
else:
    secret_key = secrets.token_hex(16)
    with open(SECRET_FILE, "w") as f:
        f.write(secret_key)

app.config["SECRET_KEY"] = secret_key
app.logger.setLevel('DEBUG')


# /
@app.route("/")
def index_show():
    return render_template(
        "users/index.html"
    )


# /users/id
@app.route("/users/<int:id>")
def users_show(id):
    app.logger.debug("logger debug")
    app.logger.info("logger info")
    app.logger.warning("logger warning")
    app.logger.error('logger error')
    app.logger.critical('logger critical')
    repo = read_repo()
    user = filter(lambda name: name["id"] == id, repo)
    nickname = next(user, {'name': 'Unknown'})['name']
    return render_template(
        "users/show.html",
        id=id,
        nickname=nickname
    )

# /users/
@app.route("/users/")
def users_index(): 
    repo = read_repo()
    search = request.args.get("query", "") # "" - значение по умолчанию (пустая строка)
    user_id = request.args.get("id", "")
    if user_id:
        return redirect(url_for('users_show', id=int(user_id)))
    if search:
        users = [u for u in repo if search.lower() in u['name']]
    else:
        users = repo
    return render_template(
        "users/search.html",
        search=search,
        users=users,
    )


@app.post("/users/")
def users_post():
    repo = read_repo()
    max_id = max((u["id"] for u in repo if "id" in u), default=0) + 1
    # извлекаем данные из формы
    user = request.form.to_dict()
    user['id'] = max_id
    # валидируем данные
    errors = validate(user)
    if errors:
        return render_template(
            "users/new.html",
            user=user,
            errors=errors,
        ), 422
    # сохраняем нового пользователя
    write_repo(user)
    # делаем редирект на список пользователей
    flash("user is added and saved in file", "success")
    return redirect("/users", code=302)


# /users/new
@app.route("/users/new")
def users_new():
    user = {
        "name": "",
        "email": "",
    }
    errors = {}
    return render_template(
        "users/new.html",
        user=user,
        errors=errors
        )

# ---lesson 21---
# /users/<id>/edit
@app.route("/users/<id>/edit")
def users_edit(id):
    user = user_find(id)
    errors = {}

    return render_template(
        "users/edit.html",
        user=user,
        errors=errors
    )

@app.route("/users/<id>/patch", methods=["POST"])
def users_patch(id):
    user = user_find(id)
    data = request.form.to_dict()

    errors = validate(data)
    if errors:
        return render_template(
            "users/edit.html",
            user=user,
            errors=errors,
        ), 422

    update_repo(id, data)
    flash("User has been updated", "success")
    return redirect(url_for("users_index"))


# ---lesson 22---
# /user/<id>/delete
@app.post('/users/<id>/delete')
def users_delete(id):
    user_destroy(id)
    flash("User has been deleted", "success")
    return redirect(url_for("users_index"))


# ---functions---
def validate(user):
    errors = {}
    # nickname
    if not user["name"]:
        errors["name"] = "Can't be blank"
    elif len(user["name"]) < 4:
        errors["name"] = "Nickname must be grater than 4 characters"
    
    # email
    repo = read_repo()
    # errors["email"] = ["this email exists" for e in repo if user["email"] in e["email"]]
    if not user["email"]:
        errors["email"] = "Can't be blank"
    elif len(user["email"]) < 4:
        errors["email"] = "Email must be grater than 4 characters"

#    if any(user["email"] in e["email"] for e in repo):
#         errors["email"] = "this email exists"
    return errors


def read_repo():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    return data


def write_repo(user):
    repo = read_repo()
    repo.append(user)
    with open(DATA_FILE, "w") as f:
        json.dump(repo, f, ensure_ascii=False, indent=4)

def user_find(id):
    repo = read_repo()
    for u in repo:
        if u["id"] == int(id):
            return u
    return None

def update_repo(id, new_data):
    repo = read_repo()
    for i, u in enumerate(repo):
        if u["id"] == int(id):
            new_data["id"] = int(id)   # сохраняем id
            repo[i] = new_data
            break
    with open(DATA_FILE, "w") as f:
        json.dump(repo, f, ensure_ascii=False, indent=4)


def user_destroy(id):
    repo = read_repo()
    new_data = []
    for i, u in enumerate(repo):
        if u["id"] != int(id):
            new_data.append(repo[i])
    with open(DATA_FILE, "w") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
