start:
	pipenv run python -m flask run;

db-setup:
	psql -c "CREATE DATABASE ${DB_NAME};"
	psql -c "CREATE ROLE ${DB_USER} SUPERUSER LOGIN WITH PASSWORD '${DB_PASSWORD}';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"
