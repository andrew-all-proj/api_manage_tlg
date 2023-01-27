import pytest
from api.models.events_model import EventModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from tests.test_post.init_post import post
from config import Config


@pytest.fixture()
def event(post, channel):
    """
        Фикстура по созданию в бд тестового медиа
    """
    event = {
      "id_post": 1,
      "id_message": None,
      "id_channel": 1,
      "date_start": "2023-01-16T09:53:31.536"
    }

    event = EventModel(**event)
    event.save()
    return event