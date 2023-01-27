import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from tests.test_channels.init_channel import channel, channel2, channel3
from init_events import event
from tests.test_post.init_post import post
from config import Config


def test_events_get_all(client, headers_user, event, channel, post):
    """
        Тест на получение списка событий через get запрос авторизованного пользователя
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.get(f'{Config.VERSION}/events/channels/{channel.id_channel}',
                          headers=headers_user)
    assert response.status_code == 200
    assert response.json[0]["id_channel"] == channel.id_channel
    assert response.json[0]["id_event"] == event_id


def test_events_get_all_no_auth(client, headers_user, event, channel, post):
    """
        Тест на получение списка событий через get запрос не авторизованного пользователя
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.get(f'{Config.VERSION}/events/channels/{channel.id_channel}')
    assert response.status_code == 401


def test_events_get_all_no_exist(client, headers_user, event, channel, post):
    """
        Тест на получение списка событий через get несуществующего канала
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.get(f'{Config.VERSION}/events/channels/1589',
                          headers=headers_user)
    assert response.status_code == 404


def test_events_get(client, headers_user, event, channel, post):
    """
        Тест на получение события через get запрос авторизованного пользователя
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.get(f'{Config.VERSION}/events/{event_id}',
                          headers=headers_user)
    assert response.status_code == 200
    assert response.json["id_channel"] == channel.id_channel
    assert response.json["id_event"] == event_id


def test_events_get_no_auth(client, headers_user, event, channel, post):
    """
        Тест на получение события через get запрос не авторизованного пользователя
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.get(f'{Config.VERSION}/events/{event_id}')
    assert response.status_code == 401


def test_events_get_no_exsis_id(client, headers_user, event, channel, post):
    """
        Тест на получение события через get запрос по не существующему id
    """
    response = client.get(f'{Config.VERSION}/events/585',
                          headers=headers_user)
    assert response.status_code == 404