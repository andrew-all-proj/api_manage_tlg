import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_channel import channel, channel2, channel3
from config import Config


def test_channel_edit_name(client, user, auth_headers, channel):
    """
        Тест на изменение name_channel канала
    """
    channel_edited_data = {
        "name_channel": "new_name1"
    }
    response = client.put(f'{Config.VERSION}/channels/1',
                          json=channel_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = ChannelModel.query.get(1)
    assert response.status_code == 200
    assert new_data.name_channel == channel_edited_data["name_channel"]
    assert data["name_channel"] == channel_edited_data["name_channel"]


def test_channel_edit_all(client, user, auth_headers, channel):
    """
        Тест на изменение name_channel канала
    """
    channel_edited_data = {
          "id_telegram": "12589635",
          "link_channel": "new_channel123",
          "name_channel": "@new_channel123"
    }
    response = client.put(f'{Config.VERSION}/channels/1',
                          json=channel_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = ChannelModel.query.get(1)
    assert response.status_code == 200
    assert new_data.id_telegram == channel_edited_data["id_telegram"]
    assert new_data.link_channel == channel_edited_data["link_channel"]
    assert new_data.name_channel == channel_edited_data["name_channel"]
    assert data["name_channel"] == channel_edited_data["name_channel"]


def test_channel_edit_all_no_auth(client, user, auth_headers, channel):
    """
        Тест на изменение на канале не авторизованным
    """
    channel_edited_data = {
          "id_telegram": "12589635",
          "link_channel": "new_channel123",
          "name_channel": "@new_channel123"
    }
    response = client.put(f'{Config.VERSION}/channels/1',
                          json=channel_edited_data,)
    data = response.json
    new_data = ChannelModel.query.get(1)
    assert response.status_code == 401
    assert new_data.id_telegram != channel_edited_data["id_telegram"]


def test_channel_edit_other_user(client, user, auth_headers, channel, channel2, channel3):
    """
        Тест на изменение в каналe другого пользователя
    """
    channel_edited_data = {
          "id_telegram": "12589635",
          "link_channel": "new_channel123",
          "name_channel": "@new_channel123"
    }
    response = client.put(f'{Config.VERSION}/channels/3',
                          json=channel_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = ChannelModel.query.get(3)
    assert response.status_code == 404
    assert new_data.id_telegram != channel_edited_data["id_telegram"]


def test_channel_edit_no_valid(client, user, auth_headers, channel):
    """
        Тест на изменение на каналe не валидными данными
    """
    channel_edited_data = {
          "id_telegram": "12",
          "link_channel": "new_channel123",
          "name_channel": "@new_channel123"
    }
    response = client.put(f'{Config.VERSION}/channels/3',
                          json=channel_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = ChannelModel.query.get(1)
    assert response.status_code == 422
    assert new_data.id_telegram != channel_edited_data["id_telegram"]
