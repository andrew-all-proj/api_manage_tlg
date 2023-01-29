import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from tests.test_channels.init_channel import channel, channel2, channel3
from init_events import event
from tests.test_post.init_post import post, post2
from config import Config


def test_events_put(client, headers_user, event, channel, post, post2):
    """
        Тест на изменение события
    """
    post_id = post.id_post
    event_id = event.id_event
    post_id_2 = post2.id_post
    data = {
      "date_start": "2023-01-27T16:59:49.749000",
      "date_stop": "2023-01-27T16:59:49.749000",
      "id_post": post_id_2
    }
    response = client.put(f'{Config.VERSION}/events/{event_id}',
                          json=data,
                          headers=headers_user)
    assert response.status_code == 200
    assert response.json["date_start"] == data["date_start"]
    assert response.json["post"]["id_post"] == post_id_2


def test_events_put_no_id_post(client, headers_user, event, channel, post, post2):
    """
        Тест на изменение события
    """
    post_id = post.id_post
    event_id = event.id_event
    post_id_2 = post2.id_post
    data = {
      "date_start": "2023-01-27T16:59:49.749000",
      "date_stop": "2023-01-27T16:59:49.749000",
      "id_post": 5999
    }
    response = client.put(f'{Config.VERSION}/events/5999',
                          json=data,
                          headers=headers_user)
    assert response.status_code == 404


def test_events_put_no_auth(client, headers_user, event, channel, post, post2):
    """
        Тест на изменение события
    """
    post_id = post.id_post
    event_id = event.id_event
    post_id_2 = post2.id_post
    data = {
      "date_start": "2023-01-27T16:59:49.749000",
      "date_stop": "2023-01-27T16:59:49.749000",
      "id_post": 5999
    }
    response = client.put(f'{Config.VERSION}/events/5999',
                          json=data)
    assert response.status_code == 401
