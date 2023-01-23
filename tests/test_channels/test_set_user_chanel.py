import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_channel import channel, channel2, channel3
from config import Config


def test_channel_set_user(client, user, user2, auth_headers, channel):
    """
        Тест на привязку канала к пользователю
    """
    channel_id = channel.id_channel
    user_id_new_pair = user2.id_user
    response = client.put(f'{Config.VERSION}/channels/1/users/{user_id_new_pair}',
                          headers=auth_headers)

    new_data = UserChannelModel.query.filter_by(id_user=user_id_new_pair).first()
    assert response.status_code == 200
    assert new_data.id_channel == channel_id


def test_channel_set_user_negative(client, user, user2, auth_headers, channel):
    """
        Тест на привязку канала к несуществующему каналу
    """
    channel_id = channel.id_channel
    user_id_new_pair = user2.id_user
    response = client.put(f'{Config.VERSION}/channels/2/users/{user_id_new_pair}',
                          headers=auth_headers)

    new_data = UserChannelModel.query.filter_by(id_user=user_id_new_pair).first()
    assert response.status_code == 404


def test_channel_set_user_negativ_user(client, user, user2, auth_headers, channel):
    """
        Тест на привязку канала к несуществующему пользователю
    """
    channel_id = channel.id_channel
    user_id_new_pair = user2.id_user
    response = client.put(f'{Config.VERSION}/channels/1/users/4',
                          headers=auth_headers)

    assert response.status_code == 400


def test_channel_set_user_no_auth(client, user, user2, auth_headers, channel):
    """
        Тест на привязку канала к пользователю
    """
    channel_id = channel.id_channel
    user_id_new_pair = user2.id_user
    response = client.put(f'{Config.VERSION}/channels/1/users/{user_id_new_pair}')

    assert response.status_code == 401
