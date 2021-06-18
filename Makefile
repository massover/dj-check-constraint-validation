test:
	poetry run pytest

lint:
	poetry run isort .
	poetry run black .

