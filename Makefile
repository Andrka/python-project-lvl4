install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run pytest --cov=task_manager --cov-report xml tests/

check: lint test

report:
	poetry run coverage report