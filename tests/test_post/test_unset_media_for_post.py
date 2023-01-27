import pytest
from sqlalchemy.sql.elements import and_

from api import auth_manager
from api.models.media_contents_model import MediaContentModel
from api.models.posts_model import PostsModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user
from tests.test_post.init_post import post, post2
from tests.test_media.init_media import media
from config import Config

def test_unset_media_for_post(client, user, auth_headers, post, post2, media):
    """
        Тест на отвязку медиа к посту
    """
    post_id = post.id_post
    post = PostsModel.query.filter(and_(PostsModel.id_user == user.id_user,
                                        PostsModel.id_post == post.id_post,
                                        PostsModel.is_archive == False)).first()

    media = MediaContentModel.query.get(1)
    post.media.append(media)

    data_list_media = {
              "media": [
                1
              ]
            }

    response = client.delete(f'/{Config.VERSION}/posts/{post_id}/setmedia',
                           json=data_list_media,
                           headers=auth_headers)
    assert response.status_code == 200
    data = response.json
    assert data["media"] == []


def test_set_media_for_post_no_auth(client, user, auth_headers, post, post2, media):
    """
        Тест на отвязку медиа от поста не авторизованным пользователем
    """
    post_id = post.id_post
    data_list_media = {
              "media": [
                1
              ]
            }
    response = client.delete(f'/{Config.VERSION}/posts/{post_id}/setmedia',
                             json=data_list_media)
    assert response.status_code == 401


def test_unset_media_for_post_no_exist_id_media(client, user, auth_headers, post, post2, media):
    """
        Тест на отвязку медиа от поста. Не существующим id медиа
    """
    post_id = post.id_post
    post = PostsModel.query.filter(and_(PostsModel.id_user == user.id_user,
                                        PostsModel.id_post == post.id_post,
                                        PostsModel.is_archive == False)).first()

    media = MediaContentModel.query.get(1)
    post.media.append(media)

    data_list_media = {
              "media": [
                15855
              ]
            }

    response = client.delete(f'/{Config.VERSION}/posts/{post_id}/setmedia',
                           json=data_list_media,
                           headers=auth_headers)
    assert response.status_code == 404
    assert response.json == {'error': 'id media 15855 not found'}
