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


def test_media_get_download(client, user, headers_user, media, file_name):
    """
        Тест на загрузку медиа с сервера
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
    response = client.get(f'{Config.VERSION}/media/download/{id_media}', headers=headers_user)
    assert response.data
    assert response.status_code == 200
