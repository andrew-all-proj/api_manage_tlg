import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_channel import channel, channel2, channel3
from config import Config


def test_channel_unset_user(client, user, user2, auth_headers, channel):
    """
        Тест на отвязку канала от пользователю
    """
    user2_id_user = user2.id_user
    user_channel = UserChannelModel(id_user=user2_id_user, id_channel=channel.id_channel)
    user_channel.save()

    response = client.delete(f'{Config.VERSION}/channels/1/users/{user2_id_user}',
                          headers=auth_headers)
    new_data = UserChannelModel.query.filter_by(id_user=user2_id_user).first()
    assert response.status_code == 200
    assert new_data == None


def test_channel_unset_user_negative(client, user, user2, auth_headers, channel):
    """
         Тест на отвязку канала от пользователю несуществующего канала
    """
    user2_id_user = user2.id_user
    id_channel = channel.id_channel
    user_channel = UserChannelModel(id_user=user2_id_user, id_channel=id_channel)
    user_channel.save()

    response = client.delete(f'{Config.VERSION}/channels/5/users/{user2_id_user}',
                             headers=auth_headers)
    new_data = UserChannelModel.query.filter_by(id_user=user2_id_user).first()
    assert response.status_code == 404
    assert new_data.id_channel == id_channel


def test_channel_set_user_negativ_user(client, user, user2, auth_headers, channel):
    """
        Тест на привязку канала к несуществующему пользователю
    """
    user2_id_user = user2.id_user
    id_channel = channel.id_channel
    user_channel = UserChannelModel(id_user=user2_id_user, id_channel=id_channel)
    user_channel.save()

    response = client.delete(f'{Config.VERSION}/channels/{id_channel}/users/500',
                             headers=auth_headers)
    new_data = UserChannelModel.query.filter_by(id_user=user2_id_user).first()
    assert response.status_code == 400
    assert new_data.id_channel == id_channel


def test_channel_set_user_no_auth(client, user, user2, auth_headers, channel):
    """
        Тест на привязку канала к пользователю
    """
    id_channel = channel.id_channel
    user2_id_user = user2.id_user
    response = client.delete(f'{Config.VERSION}/channels/{id_channel}/users/{user2_id_user}')

    assert response.status_code == 401