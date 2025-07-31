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

.PHONY: l1 install l3 fix_lint test l4 l5 l6 l3_flask