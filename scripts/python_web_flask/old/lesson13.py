from flask import render_template, Flask, request, url_for, redirect

app = Flask(__name__)

USERS = [
    {"id": 1, "name": "mike"},
    {"id": 2, "name": "mishel"},
    {"id": 3, "name": "adel"},
    {"id": 4, "name": "keks"},
    {"id": 5, "name": "kamila"},
]

@app.route("/users/<int:id>")
def users_show(id):
    user = filter(lambda name: name["id"] == id, USERS)
    nickname = next(user, {'name': 'Unknown'})['name']
    return render_template(
        "users/old/show.html",
        id=id,
        nickname=nickname
    )

@app.route("/users/")
def user_search(): 
    search = request.args.get("query", "") # "" - значение по умолчанию (пустая строка)
    user_id = request.args.get("id", "")
    if user_id:
        return redirect(url_for('users_show', id=int(user_id)))
    if search:
        users = [u for u in USERS if search.lower() in u['name']]
    else:
        users = USERS
    return render_template(
        "users/old/search.html",
        search=search,
        users=users
    )

@app.route("/")
def hello_world():
    return "Hello world"