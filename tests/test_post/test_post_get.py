import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user
from tests.test_post.init_post import post, post2
from config import Config

def test_get_post(client, user, auth_headers, post, post2):
    """
        Тест на получение всех своих постов
    """
    post_id = post.id_post
    response = client.get(f'/{Config.VERSION}/posts',
                           headers=auth_headers)
    assert response.status_code == 200
    data = response.json
    assert data[0]["id_post"] == post_id


def test_get_post_no_auth(client, user, auth_headers, post):
    """
        Тест на получение всех своих постов не авторизованным
    """
    post_id = post.id_post
    response = client.get(f'/{Config.VERSION}/posts')
    assert response.status_code == 401


def test_get_post_by_id(client, user, auth_headers, post, post2):
    """
        Тест на получение поста по id
    """
    post_id = post.id_post
    response = client.get(f'/{Config.VERSION}/posts/1',
                           headers=auth_headers)
    assert response.status_code == 200
    data = response.json
    assert data["id_post"] == post_id


def test_get_post_by_id_no_auth(client, user, auth_headers, post, post2):
    """
        Тест на получение поста по id не авторизованным пользователем
    """
    post_id = post.id_post
    response = client.get(f'/{Config.VERSION}/posts/1')
    assert response.status_code == 401


def test_get_post_by_id_no_exsit_post(client, user, auth_headers, post, post2):
    """
        Тест на получение поста по не существующего id
    """
    post_id = post.id_post
    response = client.get(f'/{Config.VERSION}/posts/589',
                           headers=auth_headers)
    assert response.status_code == 200
    assert response.json == {}



