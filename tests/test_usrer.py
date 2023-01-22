import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from config import Config


def test_user_get_by_id(client, headers_user, user):
    """
        Тест на получение пользователя через get запрос по id авторизованного пользователя
    """
    response = client.get(f'/{Config.VERSION}/users/1', headers=headers_user)
    assert response.status_code == 200
    assert response.json["user_name"] == user.user_name


def test_user_not_found(client, headers_user, user):
    """
        Тест пользователь не найден по id
    """
    response = client.get(f'/{Config.VERSION}/users/2', headers=headers_user)
    assert response.status_code == 200
    assert response.json == {}


def test_user_not_auth(client, user):
    """
        Тест пользователь не авторизован
    """
    response = client.get(f'/{Config.VERSION}/users/1')
    assert response.status_code == 401

def test_user_error_auth(client, headers_user, user):
    """
        Тест не верный токен
    """
    id_user = user.id_user
    email = user.email
    auth_token = auth_manager.auth_token(email, id_user)
    headers_user = {
        'Authorization': 'Bearer ' + auth_token.signed + "15888"
    }
    response = client.get(f'/{Config.VERSION}/users/1', headers=headers_user)
    assert response.status_code == 401


def test_user_creation(client):
    """
        Тест на создание пользователя через post запрос
    """
    user_data = {
      "email": "valera@example.com",
      "id_telegram": 1234567,
      "password": "valera",
      "user_name": "valera"
    }
    response = client.post(f'/{Config.VERSION}/users',
                           json=user_data,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 201
    assert 'valera' in data.values()


def test_user_creation_already_exist(client, user):
    """
        Тест на создание пользователя с существующим email
    """
    user_data = {"user_name": "testuser", "password": "1234", "email": "test@mail.com"}
    response = client.post(f'/{Config.VERSION}/users',
                           json=user_data,
                           content_type='application/json')
    data = response.json
    assert 'error' in data.keys()
    assert response.status_code == 400


def test_user_delete(client, user, headers_user):
    """
        Тест на удаление пользователя (перенос в архив)
    """
    response = client.delete(f'/{Config.VERSION}/users/1', headers=headers_user)
    data = response.json
    user_data = UserModel.query.get(1)
    assert {} == data
    assert user_data.is_archive == True
    assert response.status_code == 200


def test_delete_other_user(client, user, user2, headers_user):
    """
        Тест на удаление других пользователей (можно удалять только своих)
    """
    response = client.delete(f'/{Config.VERSION}/users/2', headers=headers_user)
    data = response.json
    user_data = UserModel.query.get(2)
    assert {'error': 'You can delete only own profile'} == data
    assert user_data.is_archive == False
    assert response.status_code == 400


def test_delete_user_not_auth(client, user, headers_user):
    """
        Тест на удаление пользователя не авторизованным пользователем
    """
    response = client.delete(f'/{Config.VERSION}/users/1')
    data = response.json
    user_data = UserModel.query.get(1)
    assert {'message': 'Improperly formatted or missing Authorization header'} == data
    assert user_data.is_archive == False
    assert response.status_code == 401


def test_user_edit(client, user, auth_headers):
    """
        Тест на изменение имени ползователя
    """
    user_edited_data = {
        "user_name": "new_name",
        "email": "email@test.com",
        "password": "password",
        "id_telegram": 18555555
    }
    response = client.put(f'{Config.VERSION}/users/1',
                          json=user_edited_data,
                          headers=auth_headers)
    data = response.json
    assert response.status_code == 200
    assert data["user_name"] == user_edited_data["user_name"]


def test_user_edit_email(client, user, auth_headers):
    """
        Тест на изменение email ползователя
    """
    user_edited_data = {
        "email": "email@test.com"
    }
    response = client.put(f'{Config.VERSION}/users/1',
                          json=user_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = UserModel.query.get(1)
    assert response.status_code == 200
    assert new_data.email == user_edited_data["email"]
    assert data["email"] == user_edited_data["email"]


def test_user_edit_email_novalid(client, user, auth_headers):
    """
        Тест на изменение email на не правильный формат
    """
    old_email = user.email
    user_edited_data = {
        "email": "emailtest.com"
    }
    response = client.put(f'{Config.VERSION}/users/1',
                          json=user_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = UserModel.query.get(1)
    assert response.status_code == 200
    assert new_data.email == old_email
    assert user_edited_data["email"] != data["email"]


def test_user_edit_other_user(client, user, auth_headers):
    """
        Тест изменение имени ползователя другого пользователя
    """
    old_email = user.email
    user_edited_data = {
        "user_name": "new_name"
    }
    response = client.put(f'{Config.VERSION}/users/2',
                          json=user_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = UserModel.query.get(1)
    assert response.status_code == 400
    assert new_data.email == old_email
    assert 'user_name' not in data.keys()


def test_user_edit_not_auth(client, user, auth_headers):
    """
        Тест на изменение имени ползователя не авторизованным пользователем
    """
    user_edited_data = {
        "user_name": "new_name"
    }
    response = client.put(f'{Config.VERSION}/users/1',
                          json=user_edited_data)
    data = response.json
    assert response.status_code == 401
    assert 'user_name' not in data.keys()