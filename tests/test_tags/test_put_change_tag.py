
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
        Тест на изменения имени тега
    """
    data = {
        "tag_name": "tag_5",
    }
    response = client.put(f'{Config.VERSION}/tags/1',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 200
    assert response.json['tag_name'] == data['tag_name']


def test_get_tag_no_auth(client, user, headers_user, media, channel, tags):
    """
        Тест на изменения имени тега не авторизованного пользователя
    """
    data = {
        "tag_name": "tag_5",
    }
    response = client.put(f'{Config.VERSION}/tags/1',
                           json=data)

    assert response.status_code == 401



def test_get_tag_no_exsist_tag(client, user, headers_user, media, channel, tags):
    """
        Тест на изменения имени тега не авторизованного пользователя
    """
    data = {
        "tag_name": "tag_5",
    }
    response = client.put(f'{Config.VERSION}/tags/8666',
                          json=data,
                          headers=headers_user)

    assert response.status_code == 404