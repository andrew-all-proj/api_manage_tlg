import os
import shutil

import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2, file_name
from init_media import media
from config import Config


class MediaContentModeledial:
    pass


def test_channel_delete(client, user, headers_user, media):
    """
        Тест на удаление медиа через delete запрос (перенос в архив)
    """
    response = client.delete(f'{Config.VERSION}/media/1',
                           headers=headers_user)
    update_media = MediaContentModel.query.get(1)
    assert response.status_code == 200
    assert update_media.is_archive == True
    assert response.json == {}


def test_channel_delete_negative(client, user, headers_user, media):
    """
        Тест на удаление не своего медиа через delete запрос
    """
    response = client.delete(f'{Config.VERSION}/channels/1588',
                           headers=headers_user)
    assert response.status_code == 404
    assert response.json == {'error': 'channel not found'}