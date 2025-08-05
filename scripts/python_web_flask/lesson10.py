from flask import render_template, Flask

app = Flask(__name__)

USERS = [
    {'id': 1, 'name': 'user-1'},
    {'id': 2, 'name': 'user-2'},
    {'id': 3, 'name': 'user-3'},
    {'id': 4, 'name': 'user-4'},
    {'id': 5, 'name': 'user-5'},
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

