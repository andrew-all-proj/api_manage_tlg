import io
import os
import shutil

import pytest
from api import auth_manager
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2, file_name
from init_media import media
from config import Config



def test_media_edit(client, user, auth_headers, media):
    """
        Тест на изменение описания медиа
    """
    media_edited_data = {
        "description": "New description"
    }
    response = client.put(f'{Config.VERSION}/media/1',
                          json=media_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = MediaContentModel.query.get(1)
    assert response.status_code == 200
    assert new_data.description == media_edited_data["description"]
    assert data["description"] == media_edited_data["description"]



def test_media_edit_no_auth(client, user, auth_headers, media):
    """
        Тест на изменение на канале не авторизованным
    """
    media_edited_data = {
        "description": "New description"
    }
    response = client.put(f'{Config.VERSION}/media/1',
                          json=media_edited_data)
    data = response.json
    new_data = MediaContentModel.query.get(1)
    assert response.status_code == 401
    assert new_data.description != media_edited_data["description"]


def test_channel_edit_other_user(client, user, auth_headers, media):
    """
        Тест на изменение отсутствующего медия
    """
    media_edited_data = {
        "description": "New description"
    }
    response = client.put(f'{Config.VERSION}/media/96',
                          json=media_edited_data,
                          headers=auth_headers)
    data = response.json
    new_data = MediaContentModel.query.get(1)
    assert response.status_code == 404


