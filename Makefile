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
	uv run gunicorn -w 4 scripts.python_web_flask.lesson3:app

l5_flask:
	uv run flask --app scripts.python_web_flask.lesson5 run --port 8000

l5_flask_debug:
	flask --app scripts.python_web_flask.lesson5 --debug run --reload --port 8000

l6_flask:
	flask --app scripts.python_web_flask.lesson6 --debug run --reload --port 8000

l7_flask:
	flask --app scripts.python_web_flask.lesson7 --debug run --reload --port 8000

l8_flask:
	flask --app scripts.python_web_flask.lesson8 --debug run --reload --port 8000

l9_flask:
	flask --app scripts.python_web_flask.lesson9 --debug run --reload --port 8000

l10_flask:
	flask --app scripts.python_web_flask.lesson10 --debug run --reload --port 8000

l11_flask:
	flask --app scripts.python_web_flask.lesson11 --debug run --reload --port 8000

l13_flask:
	flask --app scripts.python_web_flask.lesson13 --debug run --reload --port 8000

l16_flask:
	flask --app scripts.python_web_flask.lesson16 --debug run --reload --port 8000

l17_flask:
	flask --app scripts.python_web_flask.lesson17 --debug run --reload --port 8000

l18_flask:
	flask --app scripts.python_web_flask.lesson18 --debug run --reload --port 8000

.PHONY: l1 install l3 fix_lint test 