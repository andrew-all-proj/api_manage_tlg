import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from config import Config


@pytest.fixture()
def media(user):
    """
        Фикстура по созданию в бд тестового канала
    """
    type_media = [{
      "type_media": "video",
      "name_dir": "video",
      "extension": "mp4"
    },
    {
        "type_media": "images",
        "name_dir": "images",
        "extension": "jpg"
    },
    {
        "type_media": "images",
        "name_dir": "images",
        "extension": "jpeg"
    }
    ]

    for t_media in type_media:
        res1 = TypeMediaModel(**t_media)
        res1.save()

    media_data = [{
          "id_type_media": 1,
          "name_file": "mem1.mp4",
          "description": "vidos1",
          "id_user": 1
        },
        {
            "id_type_media": 1,
            "name_file": "mem2.mp4",
            "description": "vidos2",
            "id_user": 1
        },
        {
            "id_type_media": 2,
            "name_file": "mem3.jpg",
            "description": "images3",
            "id_user": 1
        },
         {
             "id_type_media": 2,
             "name_file": "mem4.jpg",
             "description": "images4",
             "id_user": 1
         },
    ]
    for media in media_data:
        res = MediaContentModel(**media)
        res.save()
    return