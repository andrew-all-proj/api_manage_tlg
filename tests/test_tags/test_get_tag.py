
import pytest
from api import auth_manager
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.media_tags_model import TagModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, file_name
from tests.test_media.init_media import media
from tests.test_channels.init_channel import channel
from tests.test_tags.init_tags import tags
from config import Config


def test_get_tag(client, user, headers_user, media, channel, tags):
    """
        Тест на получение тега по id
    """
    response = client.get(f'{Config.VERSION}/tags/1',
                           headers=headers_user)

    assert response.status_code == 200
    assert response.json['tag_name'] == tags[0]['tag_name']


def test_get_tag_no_auth(client, user, headers_user, media, channel, tags):
    """
        Тест на получение тега по id не аутифицированным пользователем
    """
    response = client.get(f'{Config.VERSION}/tags/1')

    assert response.status_code == 401


def test_get_tag_no_exist_tags(client, user, headers_user, media, channel, tags):
    """
        Тест на получение тега по несуществуеющему id тега
    """
    response = client.get(f'{Config.VERSION}/tags/8995',
                           headers=headers_user)

    assert response.status_code == 404


def test_get_all_tag_channel(client, user, headers_user, media, channel, tags):
    """
        Тест на получение всех тегов для канала
    """
    response = client.get(f'{Config.VERSION}/tags/channel/{channel.id_channel}',
                           headers=headers_user)

    assert response.status_code == 200
    assert response.json[0]['tag_name'] == tags[0]['tag_name']
    assert response.json[1]['tag_name'] == tags[1]['tag_name']


def test_get_all_tag_channel_no_auth(client, user, headers_user, media, channel, tags):
    """
        Тест на получение всех тегов для канала не авторизованным пользователем
    """
    response = client.get(f'{Config.VERSION}/tags/channel/{channel.id_channel}')

    assert response.status_code == 401


def test_get_all_tag_no_exist_channel(client, user, headers_user, media, channel, tags):
    """
        Тест на получение всех тегов для канала не авторизованным пользователем
    """
    response = client.get(f'{Config.VERSION}/tags/channel/1589',
                           headers=headers_user)

    assert response.status_code == 404
