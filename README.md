# Alembic migrations

1. Change table schema in postgredb.py
2. Add data in database.py
	1. First: pipenv run python -m alembic revision --autogenerate -m "changes message is a filename for migration"
	2. Second: pipenv run python -m alembic upgrade head 

