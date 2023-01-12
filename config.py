from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    _USER_NAME_DB = "postgres"
    _PASSWORD_DB = 1
    _NAME_DB = "web_site"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{_USER_NAME_DB}:{_PASSWORD_DB}@localhost/{_NAME_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Зачем эта настройка: https://flask-sqlalchemy-russian.readthedocs.io/ru/latest/config.html#id2
    DEBUG = True
    PORT = 5000
    SECRET_KEY = "ghjklkjhgfghj"
    RESTFUL_JSON = {
        'ensure_ascii': False,
    }
    TEST_DATABASE_URI = f"postgresql+psycopg2://{_USER_NAME_DB}:{_PASSWORD_DB}@localhost/db_unit_test"
    LANGUAGES = ['en', 'ru']
    VERSION = "v1"
