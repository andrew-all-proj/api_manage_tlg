import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.media_contents_model import MediaContentModel, TypeMediaModel
from api.models.posts_model import PostsModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from config import Config


@pytest.fixture()
def post(user):
    data_post = {
        "text": "кот на крыше",
        "id_user": user.id_user
    }
    post = PostsModel(**data_post)
    post.save()

    return post

@pytest.fixture()
def post2(user):
    data_post = {
        "text": "кот на крыше",
        "id_user": user.id_user
    }
    post = PostsModel(**data_post)
    post.save()

    return post
