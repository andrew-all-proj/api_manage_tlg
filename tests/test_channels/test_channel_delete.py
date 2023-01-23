import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_channel import channel, channel2, channel3
from config import Config



def test_channel_delete(client, user, headers_user, channel):
    """
        Тест на удаление канала через delete запрос
    """
    id_channel = channel.id_channel
    response = client.delete(f'{Config.VERSION}/channels/1',
                           headers=headers_user)
    update_chanel = ChannelModel.query.get(id_channel)
    assert response.status_code == 200
    assert update_chanel.is_archive == True
    assert response.json == {}


def test_channel_delete_negative(client, user, headers_user, channel):
    """
        Тест на удаление не своего канала через delete запрос
    """
    response = client.delete(f'{Config.VERSION}/channels/2',
                           headers=headers_user)
    assert response.status_code == 404
    assert response.json == {'error': 'channel not found'}