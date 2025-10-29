
"""[General Configuration Params]
"""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def get_db_uri():
    return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=environ.get('DB_USER'),
        password=environ.get('DB_PASSWORD'),
        host=environ.get('DB_HOST'),
        port=environ.get('DB_PORT'),
        database=environ.get('DB_NAME')
    )


def get_secret_key():
    return environ.get('SECRET_KEY')
