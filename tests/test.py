import json

from base64 import b64encode

from api import db
from app import app
from unittest import TestCase
from api.models.users_model import UserModel
from config import Config

class TestUser(TestCase):
    def setUp(self) -> None:
        """
            данный метод запускается перед каждым тестом
        """
        # Клиент для отправки запросов
        self.app = app
        self.client = self.app.test_client()
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
        with self.app.app_context():
            db.create_all()

    def test_user_get(self):
        users_data = [
            {
                "name": "admin",
                "id_telegram": 14562391,
                "email": "q@mail.ru",
                "password": "admin"
            },
            {
                "name": "user1",
                "id_telegram": 14562,
                "email": "q5@mail.ru",
                "password": "user1"
            },
        ]

        for user_data in users_data:
            user = UserModel(**user_data)
            db.session.add(user)
        db.session.commit()
        responce = self.client.get(f'/{Config.VERSION}/users')
        data = json.loads(responce.data)
        self.assertEqual(users_data[0]["name"], data[0]["name"])
        self.assertEqual(users_data[0]["email"], data[0]["email"])
        self.assertEqual(responce.status_code, 200)
        self.assertNotIn("password", data[0].keys())


    def tearDown(self):
        """
        Данный метод запускается после каждого теста
        """
        db.session.remove()
        db.drop_all()


def division():
    return None