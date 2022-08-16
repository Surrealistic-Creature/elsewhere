# Alembic migrations

1. Change table schema in postgredb.py
2. Add data in database.py
	1. pipenv run python -m alembic revision --autogenerate -m "changes message is a filename for migration"
	2. pipenv run python -m alembic upgrade head 


1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
4. Fourth item 