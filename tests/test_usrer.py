import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin
from config import Config

@pytest.fixture()
def user():
    """
        Фикстура по созданию в бд тестого пользователя
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
        Тест на удаление пользователя не авторизованным
    """
    response = client.delete(f'/{Config.VERSION}/users/1')
    data = response.json
    user_data = UserModel.query.get(1)
    assert {'message': 'Improperly formatted or missing Authorization header'} == data
    assert user_data.is_archive == False
    assert response.status_code == 401



def test_user_edit(client, user, auth_headers):
    user_edited_data = {
        "username": "new_name"
    }
    response = client.put(f'/users/{user.id}',
                          json=user_edited_data,
                          headers=auth_headers)
    data = response.json
    assert response.status_code == 200
    assert data["username"] == user_edited_data["username"]


@pytest.mark.skip(reason="test not implemented")
def dtest_user_delete(client, user, auth_headers):
    pass
    # TODO: реализуйте тест на удаление пользователя и запустите его, убрав декоратор @pytest.mark.skip
