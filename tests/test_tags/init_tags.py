import io
import os
import shutil

import pytest
from api import auth_manager
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.media_tags_model import TagModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2, file_name
from tests.test_media.init_media import media
from config import Config


@pytest.fixture()
def tags(channel):
    """
        Фикстура по созданию в тегов для канала
    """
    tags = [{
        "tag_name": "tag_1",
        "id_channel": channel.id_channel
    },
    {
        "tag_name": "tag_2",
        "id_channel": channel.id_channel
    }]

    for tag in tags:
        res1 = TagModel(**tag)
        res1.save()

    return tags
