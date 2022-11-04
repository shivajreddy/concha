"""
Tests for /audio-data endpoint
"""
from server.config import settings

from psql_db import schemas
from psql_db.models import AudioData

from tests.database import client, session

base_url = settings.base_url_test


def test_audio_get_all(client):
    url = base_url + '/audio-data/all'
    res = client.get(url=url)

    # test -> get all audio-data
    assert res.status_code == 200
    if res.json():
        schemas.AudioDataResponseSchema(**res.json())  # response schema validation
    assert isinstance(res.json(), list)  # only list, not other collections


def test_audio_new(test_fixture_audio_1, client):
    url = base_url + '/audio-data/new'
    res = test_fixture_audio_1

    # test -> insert new audio with proper fields
    assert res.status_code == 200
    schemas.AudioDataResponseSchema(**res.json())  # schema validation


def test_audio_get_all_by_userid(test_fixture_audio_1, test_fixture_user_token, client):
    url = base_url + "/audio-data/all-by-userid"
    token = test_fixture_user_token.json()['token']

    headers_user_1 = {"Authorization": f"Bearer {token}"}

    res = client.get(url=url, headers=headers_user_1)
    assert res.status_code == 200
    schemas.AudioDataDbSchema(**res.json()[0])
    assert isinstance(res.json(), list)
