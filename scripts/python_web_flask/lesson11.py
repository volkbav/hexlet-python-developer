from flask import render_template, Flask

app = Flask(__name__)

COURSE = [
    {'id': 1, 'name': 'course-1'},
    {'id': 2, 'name': 'course-2'},
    {'id': 3, 'name': 'course-3'},
    {'id': 4, 'name': 'course-4'},
    {'id': 5, 'name': 'course-5'},
]

@app.route("/courses/<int:id>")
def users_show(id):
    return render_template(
        "courses/index11.html",
        courses=COURSE
    )
