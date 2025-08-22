from flask import render_template, Flask, request, redirect, url_for, flash
from .repository import get_secret_key, UserRepository

app = Flask(__name__)
app.config["SECRET_KEY"] = get_secret_key()
app.logger.setLevel('DEBUG')
repo = UserRepository()

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
    users = repo.get_all()
    user = filter(lambda name: name["id"] == id, users)
    nickname = next(user, {'name': 'Unknown'})['name']
    return render_template(
        "users/show.html",
        id=id,
        nickname=nickname
    )

# /users/
@app.route("/users/")
def users_index(): 
    search = request.args.get("query", "") # "" - значение по умолчанию (пустая строка)
    user_id = request.args.get("id", "")
    users = repo.get_all()
    
    if user_id:
        return redirect(url_for('users_show', id=int(user_id)))
    if search:
        users = [u for u in users if search.lower() in u['name']]
    
    return render_template(
        "users/search.html",
        search=search,
        users=users,
    )


@app.post("/users/")
def users_post():
    users = repo.get_all()
    max_id = max((u["id"] for u in users if "id" in u), default=0) + 1
    # извлекаем данные из формы
    user = request.form.to_dict()
    user['id'] = max_id
    # валидируем данные
    errors = repo.validate(user)
    if errors:
        return render_template(
            "users/new.html",
            user=user,
            errors=errors,
        ), 422
    # сохраняем нового пользователя
    repo._write(user)
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
    user = repo.find(id)
    errors = {}

    return render_template(
        "users/edit.html",
        user=user,
        errors=errors
    )

@app.route("/users/<id>/patch", methods=["POST"])
def users_patch(id):
    user = repo.find(id)
    data = request.form.to_dict()

    errors = repo.validate(data, current_id=id)
    if errors:
        return render_template(
            "users/edit.html",
            user=user,
            errors=errors,
        ), 422

    repo.update(id, data)
    flash("User has been updated", "success")
    return redirect(url_for("users_index"))


# ---lesson 22---
# /user/<id>/delete
@app.post('/users/<id>/delete')
def users_delete(id):
    repo.delete(id)
    flash("User has been deleted", "success")
    return redirect(url_for("users_index"))

