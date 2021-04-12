install:
	poetry install

lint:
	poetry run flake8 task_manager tasks

selfcheck:
	poetry check

check: selfcheck lint

migrate:
	poetry run python3 manage.py migrate

runserver:
	poetry run python3 manage.py runserver

requirements:
	poetry export -f requirements.txt --output requirements.txt