install:
	poetry install

lint:
	poetry run flake8 task_manager

test:
	poetry run pytest --cov=task_manager --cov-report xml tests/

check: lint test

report:
	poetry run coverage report

migrate:
	poetry run python3 manage.py migrate

runserver:
	poetry run python3 manage.py runserver

requirements:
	poetry export -f requirements.txt --output requirements.txt