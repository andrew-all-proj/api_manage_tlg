import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_channel import channel, channel2, channel3
from config import Config


def test_channel_get_all(client, headers_user, channel, channel2, channel3):
    """
        Тест на получение списка каналов через get запрос авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels', headers=headers_user)
    assert response.status_code == 200
    assert response.json[0]["name_channel"] == channel.name_channel
    assert response.json[1]["name_channel"] == channel2.name_channel
    assert len(response.json) == 2


def test_channel_get_all_no_auth(client, headers_user, channel, channel2):
    """
        Тест на получение списка каналов через get запрос  не авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels')
    assert response.status_code == 401
    assert len(response.json) == 1


def test_channel_get_by_id(client, headers_user, channel, channel2):
    """
        Тест на получение канала через get запрос по id авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels/1', headers=headers_user)
    assert response.status_code == 200
    assert response.json["name_channel"] == channel.name_channel


def test_channel_get_by_id_negative(client, headers_user, channel, channel2):
    """
        Тест на получение не существующего канала через get запрос по id авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels/4', headers=headers_user)
    assert response.status_code == 200
    assert response.json == {}

def test_channel_get_by_id_no_auth(client, headers_user, channel, channel2):
    """
        Тест на получение существующего канала через get запрос по id не авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels/1')
    assert response.status_code == 401
    assert response.json == {'message': 'Improperly formatted or missing Authorization header'}







