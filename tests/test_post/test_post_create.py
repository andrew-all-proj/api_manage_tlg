import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user
from config import Config


def test_post_creation(client, user, auth_headers):
    """
        Тест на создание поста
    """
    user_data = {
        "text": "мой первый пост"
    }
    response = client.post(f'/{Config.VERSION}/posts',
                           json=user_data,
                           content_type='application/json',
                           headers=auth_headers)
    data = response.json
    assert response.status_code == 201
    assert 'мой первый пост' in data.values()


def test_post_creation_no_auth(client, user, auth_headers):
    """
        Тест на создание поста не авторизованым пользователем
    """
    user_data = {
        "text": "мой первый пост"
    }
    response = client.post(f'/{Config.VERSION}/posts',
                           json=user_data,
                           content_type='application/json')

    assert response.status_code == 401
