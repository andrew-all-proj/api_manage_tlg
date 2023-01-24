import io
import os
import shutil

import pytest
from api import auth_manager
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2, file_name
from init_media import media
from config import Config



def test_media_creation(client, user, headers_user, media, file_name):
    """
        Тест на загрузку медиа через post запрос сохранение б бд и на сервер
    """
    user_id = user.id_user
    data = {
        'file': (open(file_name, 'rb'), file_name)
    }
    response = client.post(f'{Config.VERSION}/media/',
                           data=data,
                           headers=headers_user,
                           content_type='multipart/form-data')
    id_media = response.json['id_media']
    media = MediaContentModel.query.filter_by(id_media=id_media).one()
    type_media = TypeMediaModel.query.filter_by(id_type_media=media.id_type_media).one()
    assert True == os.path.exists(f"{Config.BASE_DIR}/{user_id}/{type_media.name_dir}/{media.name_file}")
    assert response.status_code == 201
    shutil.rmtree(f"{Config.BASE_DIR}/{user_id}")



def test_media_creation_no_auth(client, user, headers_user, media, file_name):
    """
        Тест на загрузку медиа через post запрос сохранение б бд и на сервер
    """
    user_id = user.id_user
    data = {
        'file': (open(file_name, 'rb'), file_name)
    }
    response = client.post(f'{Config.VERSION}/media/',
                           data=data,
                           content_type='multipart/form-data')
    assert response.status_code == 401


