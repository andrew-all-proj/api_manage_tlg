import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from config import Config

@pytest.fixture()
def channel(user):
    """
        Фикстура по созданию в бд тестового канала
    """
    user_data = {"name_channel": "testchannel",
                 "link_channel": "link_test",
                 "id_telegram": "-2565555",
                 "id_user_admin": user.id_user}
    channel = ChannelModel(**user_data)
    channel.save()
    user_channel = UserChannelModel(channel.id_channel, user.id_user)
    user_channel.save()
    return channel

@pytest.fixture()
def channel2(user):
    """
        Фикстура по созданию в бд тестового канала
    """
    user_data = {"name_channel": "testchannel2",
                 "link_channel": "link_test2",
                 "id_telegram": "-25655995",
                 "id_user_admin": user.id_user}
    channel = ChannelModel(**user_data)
    channel.save()
    user_channel = UserChannelModel(channel.id_channel, user.id_user)
    user_channel.save()
    return channel

def test_channel_get_all(client, headers_user, channel, channel2):
    """
        Тест на получение канала через get запрос по id авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels', headers=headers_user)
    assert response.status_code == 200
    assert response.json[0]["name_channel"] == channel.name_channel
    assert response.json[1]["name_channel"] == channel2.name_channel


def test_channel_get_all_no_auth(client, headers_user, channel, channel2):
    """
        Тест на получение канала через get запрос по id не авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/channels')
    assert response.status_code == 401
    assert len(response.json) == 1


def test_channel_creation(client, user, headers_user):
    """
        Тест на создание канала через post запрос
    """
    user_data = {"name_channel": "testchannel2",
                 "link_channel": "link_test2",
                 "id_telegram": "-25655995"}

    response = client.post(f'{Config.VERSION}/channels',
                           json=user_data,
                           headers=headers_user,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 201
    assert 'testchannel2' in data.values()


def test_channel_creation_no_auth(client, user, headers_user):
    """
        Тест на создание канала через post запрос не авторизованным
    """
    user_data = {"name_channel": "testchannel2",
                 "link_channel": "link_test2",
                 "id_telegram": "-25655995"}

    response = client.post(f'{Config.VERSION}/channels',
                           json=user_data,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 401
    assert 'testchannel2' not in data.values()


def test_channel_creation_duplicate(client, user, headers_user, channel):
    """
        Тест на создание канала через post запрос
    """
    user_data = {"name_channel": "testchannel2",
                 "link_channel": "link_test2",
                 "id_telegram": "-2565555"}

    response = client.post(f'{Config.VERSION}/channels',
                           json=user_data,
                           headers=headers_user,
                           content_type='application/json')
    data = response.json
    assert response.status_code == 400
    assert 'testchannel2' not in data.values()
