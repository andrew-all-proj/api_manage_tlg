import shutil
from pathlib import Path

from api import db, auth_manager
from app import app
from config import Config
from base64 import b64encode
from api.models.users_model import UserModel
import pytest

BASE_DIR = Path(__file__).parent

@pytest.fixture()
def application():
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
    })
    db.app = app
    with app.app_context():
        db.create_all()

    yield app

    db.session.close()
    db.drop_all()
    try:
        shutil.rmtree(f"{Config.BASE_DIR}/1")
    except:
        print()


@pytest.fixture()
def client(application):
    return application.test_client()

@pytest.fixture()
def user_admin():
    user_data = {"user_name": "admin", "password": "admin", "email": "admin@mail.com"}
    user = UserModel(**user_data)
    user.save()
    return user

@pytest.fixture()
def auth_headers(user_admin):
    user_data = {"email": "admin@mail.com", "password": "admin", "id_user": 1}
    auth_token = auth_manager.auth_token(user_data['email'], user_data['id_user'])
    headers = {
        'Authorization': 'Bearer ' + auth_token.signed
    }
    return headers

@pytest.fixture()
def user():
    """
        Фикстура по созданию в бд тестового пользователя
    """
    user_data = {"user_name": "testuser", "password": "1234", "email": "test@mail.com"}
    user = UserModel(**user_data)
    user.save()
    return user

@pytest.fixture()
def user2():
    """
        Фикстура по созданию в бд тестого пользователя
    """
    user_data = {"user_name": "jonh", "password": "1234", "email": "jonh@mail.com"}
    user = UserModel(**user_data)
    user.save()
    return user

@pytest.fixture()
def headers_user(user):
    id_user = user.id_user
    email = user.email
    auth_token = auth_manager.auth_token(email, id_user)
    return  {
        'Authorization': 'Bearer ' + auth_token.signed
    }
file_name = "image.jpeg"


@pytest.fixture()
def file_name():
    return str(BASE_DIR) + "/image.jpeg"

