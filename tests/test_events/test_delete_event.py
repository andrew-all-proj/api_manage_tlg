import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from tests.test_channels.init_channel import channel, channel2, channel3
from init_events import event
from tests.test_post.init_post import post, post2
from config import Config


def test_events_delete(client, headers_user, event, channel, post):
    """
        Тест на изменение статуса выполнено(удалено)
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.delete(f'{Config.VERSION}/events/{event_id}',
                          headers=headers_user)
    assert response.status_code == 200
    assert response.json["completed"] == True


def test_events_delete_no_id_event(client, headers_user, event, channel, post):
    """
        Тест на изменение статуса выполнено(удалено) не существующего события
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.delete(f'{Config.VERSION}/events/8989',
                          headers=headers_user)
    assert response.status_code == 404


def test_events_delete_no_auth(client, headers_user, event, channel, post):
    """
        Тест на изменение статуса выполнено(удалено) не авторизованным пользователем
    """
    post_id = post.id_post
    event_id = event.id_event
    response = client.delete(f'{Config.VERSION}/events/8989')
    assert response.status_code == 401
