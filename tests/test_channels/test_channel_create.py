import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_channel import channel, channel2, channel3
from config import Config


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
    update_chanel = ChannelModel.query.filter_by(id_telegram="-25655995").one()
    assert response.status_code == 201
    assert update_chanel.id_telegram == "-25655995"
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
