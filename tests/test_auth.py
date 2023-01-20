import jwt
import pytest
from api import auth_manager
from api.models.users_model import UserModel
from config import Config
from tests.init_test import client, user_admin, application, auth_headers


def test_get_jwt_token_auth(client, user_admin):
    user = user_admin
    user_data_req = {
        "email": "admin@mail.com",
        'password': 'admin'
    }
    response = client.post(f'/{Config.VERSION}/auth',
                           json=user_data_req,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 200
    decode_jwt = jwt.decode(data["auth_token"], Config.JWT_SECRET, algorithms="HS256")
    assert decode_jwt["sub"] == user.email
    assert decode_jwt["scope"] == user.id_user


def test_get_jwt_token_auth_negative(client, user_admin):
    user = user_admin
    user_data_req = {
        "email": "admin@mail.com",
        'password': 'admin'
    }
    response = client.post(f'/{Config.VERSION}/auth',
                           json=user_data_req,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 200
    decode_jwt = jwt.decode(data["auth_token"], Config.JWT_SECRET, algorithms="HS256")
    assert decode_jwt["sub"] != "admin@mail"
    assert decode_jwt["scope"] != 2