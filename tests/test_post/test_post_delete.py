import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user
from tests.test_post.init_post import post, post2
from config import Config

def test_get_delete(client, user, auth_headers, post, post2):
    """
        Тест на удаление поста(перенос в архив)
    """
    post_id = post.id_post
    response = client.delete(f'/{Config.VERSION}/posts/{post_id}',
                           headers=auth_headers)
    assert response.status_code == 200
    assert response.json == {}


def test_get_delete_no_auth(client, user, auth_headers, post, post2):
    """
        Тест на удаление поста(перенос в архив) не авторизованным пользователем
    """
    post_id = post.id_post
    response = client.delete(f'/{Config.VERSION}/posts/{post_id}')
    assert response.status_code == 401


def test_get_delete_no_exsist_id(client, user, auth_headers, post, post2):
    """
        Тест на удаление поста(перенос в архив)
    """
    response = client.delete(f'/{Config.VERSION}/posts/558555',
                           headers=auth_headers)
    assert response.status_code == 404
