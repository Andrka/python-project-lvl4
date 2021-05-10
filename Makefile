install:
	poetry install

lint:
	poetry run flake8 labels statuses task_manager tasks users

test:
	poetry run coverage run --omit '.venv/*' --source='.' manage.py test

selfcheck:
	poetry check

check: selfcheck lint test

coverage-report:
	poetry run coverage xml

migrate:
	poetry run python3 manage.py migrate

runserver:
	poetry run python3 manage.py runserver

requirements:
	poetry export -f requirements.txt --output requirements.txt

isort:
	poetry run isort .