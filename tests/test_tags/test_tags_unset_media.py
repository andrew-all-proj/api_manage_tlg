
import pytest
from sqlalchemy import and_

from api import auth_manager, db
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.media_tags_model import TagModel, tags
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, file_name
from tests.test_media.init_media import media
from tests.test_channels.init_channel import channel
from tests.test_tags.init_tags import tags as tg
from config import Config


def test_tag_unset_tags(client, user, headers_user, media, channel, tg):
    """
        Тест на отвязку тега от медиа
    """
    media = MediaContentModel.query.filter(and_(MediaContentModel.id_user == user.id_user,
                                                MediaContentModel.id_media == 1,
                                                MediaContentModel.is_archive == False)).first()
    id_tag = 1
    tag = TagModel.query.get(id_tag)
    media.tags.append(tag)

    data = {
        "tags": [
            id_tag
        ]
    }
    response = client.delete(f'{Config.VERSION}/media/1/settags',
                           json=data,
                           headers=headers_user)

    assert response.status_code == 200
    tags_list = db.session.query(tags).filter_by(id_tag=id_tag).all()
    assert tags_list == []


def test_tag_unset_tags_no_auth(client, user, headers_user, media, channel, tg):
    """
        Тест на отвязку тега от медиа не авторизованным пользователем
    """
    media = MediaContentModel.query.filter(and_(MediaContentModel.id_user == user.id_user,
                                                MediaContentModel.id_media == 1,
                                                MediaContentModel.is_archive == False)).first()
    id_tag = 1
    tag = TagModel.query.get(id_tag)
    media.tags.append(tag)

    data = {
        "tags": [
            id_tag
        ]
    }
    response = client.delete(f'{Config.VERSION}/media/1/settags',
                           json=data)

    assert response.status_code == 401
