import pytest

from api import auth_manager
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user
from tests.test_post.init_post import post, post2
from tests.test_media.init_media import media
from config import Config

def test_set_media_for_post(client, user, auth_headers, post, post2, media):
    """
        Тест на привязку медиа к посту
    """
    post_id = post.id_post
    data_list_media = {
              "media": [
                1
              ]
            }
    response = client.put(f'/{Config.VERSION}/posts/{post_id}/setmedia',
                           json=data_list_media,
                           headers=auth_headers)
    assert response.status_code == 200
    data = response.json
    assert data["media"][0]["id_media"] == 1


def test_set_media_for_post_no_auth(client, user, auth_headers, post, post2, media):
    """
        Тест на привязку медиа к посту не авторизованным пользователем
    """
    post_id = post.id_post
    data_list_media = {
              "media": [
                1
              ]
            }
    response = client.put(f'/{Config.VERSION}/posts/{post_id}/setmedia',
                           json=data_list_media)
    assert response.status_code == 401


def test_set_media_for_post_no_exist(client, user, auth_headers, post, post2, media):
    """
        Тест на привязку медиа к посту не авторизованным пользователем
    """
    post_id = post.id_post
    data_list_media = {
              "media": [
                158
              ]
            }
    response = client.put(f'/{Config.VERSION}/posts/{post_id}/setmedia',
                           headers=auth_headers,
                           json=data_list_media)
    assert response.status_code == 404
