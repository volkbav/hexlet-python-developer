from flask import render_template, Flask

app = Flask(__name__)

USERS = = [
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
        "users/show.html",
        id=id,
        nickname=nickname
    )

@app.route("/users")
def user_search():
    
    return render_template("users/search.html")