from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_DIR = f'{BASE_DIR}/content_media'
VERSION = "api/v1"

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
    VERSION = VERSION

    JWT_ISSUER = "Flask_PyJWT"
    JWT_AUTHTYPE = "HS256"
    JWT_SECRET = "SuperSecretKey"
    JWT_AUTHMAXAGE = 36000

    SECURITY_PASSWORD_SALT = 'my_precious_two'

    BASE_DIR = BASE_DIR

class EmailConfig:
    BASE_LINK = 'managetlg.com/' + VERSION + '/email/confirm/'
    HOST = 'smtp.gmail.com'
    PORT = 587
    USER = "info.manager.tlg@gmail.com"
    PWD = "lyckbbkfasucxaak"
    FROM = 'info.manager.tlg@gmail.co'