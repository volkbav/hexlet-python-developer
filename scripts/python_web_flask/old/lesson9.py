from flask import Flask

app = Flask(__name__)


@app.teardown_request
def run_always(exception):
    print("This will always run")


@app.route("/")
def home():
    raise Exception("Something went wrong")