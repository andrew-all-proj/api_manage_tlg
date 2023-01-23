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

@pytest.fixture()
def channel3(user2):
    """
        Фикстура по созданию в бд тестового канала
    """
    user_data = {"name_channel": "testchannel2",
                 "link_channel": "link_test2",
                 "id_telegram": "-256555564",
                 "id_user_admin": user2.id_user}
    channel = ChannelModel(**user_data)
    channel.save()
    user_channel = UserChannelModel(channel.id_channel, user2.id_user)
    user_channel.save()
    return channel