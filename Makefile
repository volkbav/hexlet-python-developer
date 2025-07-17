l1:
	uv run scripts/python_sql/lesson1.py
	uv run scripts/python_sql/lesson1_my.py
l3:
	uv run scripts/python_sql/lesson3_my.py

install:
	uv sync

fix_lint:
	uv run ruff check --fix .

test:
	uv run pytest -s

.PHONY: l1 install l3 fix_lint test