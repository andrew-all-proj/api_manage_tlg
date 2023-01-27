
import pytest
from api import auth_manager, db
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.media_tags_model import TagModel, tags
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, file_name
from tests.test_media.init_media import media
from tests.test_channels.init_channel import channel
from tests.test_tags.init_tags import tags as tg
from config import Config


def test_tag_set_media(client, user, headers_user, media, channel, tg):
    """
        Тест на привязку тега к медиа
    """
    id_tag = 1
    data = {
        "tags": [
            id_tag
        ]
    }
    response = client.put(f'{Config.VERSION}/media/1/settags',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 200
    tag_bd = TagModel.query.filter_by(id_tag=id_tag).one()
    tags_list = db.session.query(tags).filter_by(id_tag=id_tag).all()
    assert id_tag in tags_list[0]
    assert tag_bd.id_tag == id_tag


def test_media_no_exist_id_tag(client, user, headers_user, media, channel, tg):
    """
        Тест на привязку тега к медиа не существующего id  тега
    """
    id_tag = 588
    data = {
        "tags": [
            id_tag
        ]
    }
    response = client.put(f'{Config.VERSION}/media/1/settags',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 404


def test_tag_creation_no_auth(client, user, headers_user, media, channel, tg):
    """
        Тест на привязку тега к медиа
    """
    id_tag = 1
    data = {
        "tags": [
            id_tag
        ]
    }
    response = client.put(f'{Config.VERSION}/media/1/settags',
                           json=data)

    assert response.status_code == 401

