l1:
	uv run scripts/python_sql/lesson1.py
	uv run scripts/python_sql/lesson1_my.py

install:
	uv sync

.PHONY: l1 install