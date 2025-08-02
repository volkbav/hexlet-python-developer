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
	uv run flask --app scripts/python_web_flask/lesson5.py --debug run --port 8000

server:
	uv run python3 scripts/python_web_flask/server.py

.PHONY: l1 install l3 fix_lint test l4 l5 l6 l3_flask server l5_flask server l5_flask_debug