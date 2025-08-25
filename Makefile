include .env
export $(shell sed 's/=.*//' .env)

server:
	uv run python3 scripts/python_web_flask/server.py

l1:
	uv run scripts/python_sql/lesson1.py
	
l3:
	uv run scripts/python_sql/lesson3_my.py

l4:
	uv run scripts/python_sql/lesson4.py

l5:
	uv run scripts/python_sql/lesson5.py

l6:
	uv run scripts/python_sql/lesson6.py

install:
	uv sync

fix_lint:
	uv run ruff check --fix .

test:
	uv run pytest -s

l3_flask:
	uv run gunicorn -w 4 scripts.python_web_flask.old.lesson3:app

l5_flask:
	uv run flask --app scripts.python_web_flask.old.lesson5 run --port 8000

l5_flask_debug:
	flask --app scripts.python_web_flask.old.lesson5 --debug run --reload --port 8000

l6_flask:
	flask --app scripts.python_web_flask.old.lesson6 --debug run --reload --port 8000

l7_flask:
	flask --app scripts.python_web_flask.old.lesson7 --debug run --reload --port 8000

l8_flask:
	flask --app scripts.python_web_flask.old.lesson8 --debug run --reload --port 8000

l9_flask:
	flask --app scripts.python_web_flask.old.lesson9 --debug run --reload --port 8000

l10_flask:
	flask --app scripts.python_web_flask.old.lesson10 --debug run --reload --port 8000

l11_flask:
	flask --app scripts.python_web_flask.old.lesson11 --debug run --reload --port 8000

l13_flask:
	flask --app scripts.python_web_flask.old.lesson13 --debug run --reload --port 8000

l16_flask:
	flask --app scripts.python_web_flask.old.lesson16 --debug run --reload --port 8000

l17_flask:
	flask --app scripts.python_web_flask.old.lesson17 --debug run --reload --port 8000

l18_flask:
	flask --app scripts.python_web_flask.old.lesson18 --debug run --reload --port 8000

l19_flask:
	flask --app scripts.python_web_flask.old.lesson19 --debug run --reload --port 8000

flask:
	@flask run --host=0.0.0.0 --port=8000

build_flask:
	scripts/python_web_flask/build.sh

gunicorn:
	@gunicorn -b 0.0.0.0:8000 scripts.python_web_flask.result:app --workers 4 --reload

.PHONY: l1 install l3 fix_lint test flask gunicorn