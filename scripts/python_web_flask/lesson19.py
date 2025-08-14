from flask import render_template, Flask, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "users.json"
)

app.logger.setLevel('DEBUG')


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if app.config['SECRET_KEY'] is None:
    raise RuntimeError("SECRET_KEY is not set in environment variables!")


# /
@app.route("/")
def index_show():
    return render_template(
        "users/l19_index.html"
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
        "users/l19_show.html",
        id=id,
        nickname=nickname
    )

# /users/
@app.route("/users/")
def user_search(): 
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
        "users/l19_search.html",
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
            "users/l19_new.html",
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
        "users/l19_new.html",
        user=user,
        errors=errors
        )

# functions
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

    if any(user["email"] in e["email"] for e in repo):
         errors["email"] = "this email exists"
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