import pytest
from api import auth_manager
from api.models.channels_model import ChannelModel, UserChannelModel
from api.models.users_model import UserModel
from tests.init_test import client, application, auth_headers, user_admin, headers_user, user, user2
from init_media import media
from config import Config


def test_media_get_all(client, headers_user, media):
    """
        Тест на получение списка медиа через get запрос авторизованного пользователя,
        ограничено настройками, количество записей на одну страницу
    """
    response = client.get(f'{Config.VERSION}/media/', headers=headers_user)
    assert len(response.json) == 3 #  настройка количества записей
    assert response.status_code == 200


def test_media_get_all_no_auth(client, headers_user, media):
    """
        Тест на получение списка каналов через get запрос не авторизованного пользователя
    """
    response = client.get(f'{Config.VERSION}/media/')
    assert response.status_code == 401


def test_media_get_all_paginator(client, headers_user, media):
    """
        Тест на получение списка медиа через get запрос авторизованного пользователя,
        ограничено настройками, количество записей на одну страницу
    """
    response = client.get(f'{Config.VERSION}/media/?per_page=4', headers=headers_user)
    assert len(response.json) == 4
    assert response.status_code == 200

def test_media_get_all_paginator_page(client, headers_user, media):
    """
        Тест на получение списка медиа через get запрос авторизованного пользователя,
        ограничено настройками, количество записей на одну страницу
    """
    response = client.get(f'{Config.VERSION}/media/?per_page=2&page=2', headers=headers_user)
    assert len(response.json) == 2
    assert response.status_code == 200


def test_media_get(client, headers_user, media):
    """
        Тест на получение списка медиа через get запрос авторизованного пользователя  по id
    """
    response = client.get(f'{Config.VERSION}/media/1', headers=headers_user)
    assert response.status_code == 200


def test_media_get_no_auth(client, headers_user, media):
    """
        Тест на получение списка медиа через get запрос авторизованного пользователя  по id
    """
    response = client.get(f'{Config.VERSION}/media/1')
    assert response.status_code == 401