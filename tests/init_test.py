from api import db
from app import app
from config import Config
from base64 import b64encode
from api.models.users_model import UserModel
import pytest


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
    user_data = {"email": "admin@mail.com", "password": "admin"}
    headers = {
        'Authorization': 'Basic ' + b64encode(
            f"{user_data['user_name']}:{user_data['password']}".encode('ascii')).decode('utf-8')
    }
    return headers
