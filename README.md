Alembic migrations
Change table schema in postgredb.py
Add data in database.py
First:
	pipenv run python -m alembic revision --autogenerate -m "changes message is a filename for migration"
Second:
	pipenv run python -m alembic upgrade head 

