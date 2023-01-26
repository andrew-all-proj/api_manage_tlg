
import pytest
from api import auth_manager
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.media_tags_model import TagModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, file_name
from tests.test_media.init_media import media
from tests.test_channels.init_channel import channel
from config import Config


def test_tag_creation(client, user, headers_user, media, channel):
    """
        Тест на создание тега
    """
    data = {
          "id_channel": channel.id_channel,
          "tag_name": "tag_1",
        }
    response = client.post(f'{Config.VERSION}/tags',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 201
    id_tag = response.json['id_tag']
    tag_bd = TagModel.query.filter_by(id_tag=id_tag).one()
    assert tag_bd.id_tag == id_tag
    assert tag_bd.tag_name == data["tag_name"]


def test_media_creation_no_auth(client, user, headers_user, media, channel):
    """
        Тест на создание тега не аутифицированного пользователя
    """
    data = {
        "id_channel": channel.id_channel,
        "tag_name": "tag_1",
    }
    response = client.post(f'{Config.VERSION}/tags',
                           json=data)

    assert response.status_code == 401


def test_media_creation_no_exist_channel(client, user, headers_user, media, channel):
    """
        Тест на создание тега для несуществующего канала
    """
    data = {
        "id_channel": channel.id_channel,
        "tag_name": "tag_1",
    }
    response = client.post(f'{Config.VERSION}/tags',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 201


def test_media_creation_exist_name_tag(client, user, headers_user, media, channel):
    """
        Тест на создание двух одинаковых тегов для канала
    """
    data = {
        "id_channel": channel.id_channel,
        "tag_name": "tag_1",
    }
    response = client.post(f'{Config.VERSION}/tags',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 201
    response = client.post(f'{Config.VERSION}/tags',
                           json=data,
                           headers=headers_user)
    assert response.status_code == 400