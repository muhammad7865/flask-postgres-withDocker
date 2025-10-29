
"""[General Configuration Params]
"""
from os import environ, path
from dotenv import load_dotenv

# Base dir and optional local .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def get_db_uri():
    """Return a SQLAlchemy-compatible database URI.

    Priority:
      1. Use explicit DATABASE_URL env var if present (common in CI and Docker).
      2. Otherwise build from DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME with sensible defaults.

    This function avoids returning literal 'None' for the port (which breaks SQLAlchemy).
    """
    # If a full DATABASE_URL is provided (e.g. in CI), use it directly.
    database_url = environ.get('DATABASE_URL')
    if database_url:
        return database_url

    user = environ.get('DB_USER', 'postgres')
    password = environ.get('DB_PASSWORD', '')
    host = environ.get('DB_HOST', '127.0.0.1')
    port = environ.get('DB_PORT')
    # Ensure port is numeric; fall back to default 5432 when missing/invalid
    try:
        port_int = int(port) if port not in (None, '', 'None') else 5432
    except (TypeError, ValueError):
        port_int = 5432
    database = environ.get('DB_NAME', 'postgres')

    # Build the URI. If password is empty, omit the password part.
    if password:
        return f'postgresql://{user}:{password}@{host}:{port_int}/{database}'
    return f'postgresql://{user}@{host}:{port_int}/{database}'


def get_secret_key():
    return environ.get('SECRET_KEY', 'change-me')
