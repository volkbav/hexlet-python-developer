from flask import Flask

# Это callable WSGI-приложение
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Test2"


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=8000)
