import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user
from tests.test_post.init_post import post, post2
from config import Config

def test_update_post(client, user, auth_headers, post, post2):
    """
        Тест на обновление поста
    """
    data_new = {
      "text": "new text!!!"
    }
    post_id = post.id_post
    response = client.put(f'/{Config.VERSION}/posts/{post_id}',
                          json=data_new,
                           headers=auth_headers)
    assert response.status_code == 200
    data = response.json
    assert data["text"] == data_new["text"]


def test_update_post_no_auth(client, user, auth_headers, post, post2):
    """
        Тест на обновление поста не авторизованого пользователя
    """
    data_new = {
      "text": "new text!!!"
    }
    post_id = post.id_post
    response = client.put(f'/{Config.VERSION}/posts/{post_id}',
                          json=data_new)
    assert response.status_code == 401


def test_update_post_no_exist_id(client, user, auth_headers, post, post2):
    """
        Тест на обновление не существующего поста
    """
    data_new = {
      "text": "new text!!!"
    }
    response = client.put(f'/{Config.VERSION}/posts/25895',
                          json=data_new,
                           headers=auth_headers)
    assert response.status_code == 404