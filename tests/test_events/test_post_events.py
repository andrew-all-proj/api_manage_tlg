import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from tests.test_channels.init_channel import channel, channel2, channel3
from init_events import event
from tests.test_post.init_post import post
from config import Config


def test_events_post(client, headers_user, channel, post):
    """
        Тест на создание события авторизованного пользователя
    """
    post_id = post.id_post
    event = {
      "date_start": "2023-01-27T15:08:09.495Z",
      "date_stop": "2023-01-27T15:08:09.495Z",
      "id_channel": 1,
      "id_post": post_id
    }

    response = client.post(f'{Config.VERSION}/events',
                           json=event,
                           content_type='application/json',
                           headers=headers_user)
    assert response.status_code == 201
    assert response.json["post"]["id_post"] == post_id


def test_events_post_no_auth(client, headers_user, channel, post):
    """
        Тест на создание события не авторизованного пользователя
    """
    post_id = post.id_post
    event = {
      "date_start": "2023-01-27T15:08:09.495Z",
      "date_stop": "2023-01-27T15:08:09.495Z",
      "id_channel": 1,
      "id_post": post_id
    }

    response = client.post(f'{Config.VERSION}/events',
                           json=event,
                           content_type='application/json')
    assert response.status_code == 401
