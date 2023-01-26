
import pytest
from api import auth_manager
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.media_tags_model import TagModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, file_name
from tests.test_media.init_media import media
from tests.test_channels.init_channel import channel
from tests.test_tags.init_tags import tags
from config import Config


def test_delete_tag(client, user, headers_user, media, channel, tags):
    """
        Тест на удаление тега по id
    """
    id_tag = 1
    response = client.delete(f'{Config.VERSION}/tags/{id_tag}',
                           headers=headers_user)
    tag = TagModel.query.filter_by(id_tag=id_tag).first()
    assert tag == None
    assert response.status_code == 200
    assert response.json == {}


def test_delete_tag_auth(client, user, headers_user, media, channel, tags):
    """
        Тест на удаление тега по id
    """
    id_tag = 1
    response = client.delete(f'{Config.VERSION}/tags/{id_tag}')
    tag = TagModel.query.filter_by(id_tag=id_tag).first()
    assert response.status_code == 401


def test_delete_tag_no_excsist_id_tag(client, user, headers_user, media, channel, tags):
    """
        Тест на удаление тега по id
    """
    id_tag = 5959
    response = client.delete(f'{Config.VERSION}/tags/{id_tag}',
                           headers=headers_user)
    assert response.status_code == 404
