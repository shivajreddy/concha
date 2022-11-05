import pytest

from server.config import settings

from psql_db import schemas
from jose import jwt

from tests.database import client, session

base_url = settings.base_url_test

# sample data sets for testing
sample_new_user_1 = {
    "name": "test1",
    "email": "test1@example.com",
    "password": "pass1",
    "address": "address1",
    "image": "image1"
}

sample_new_user_2 = {
    "name": "test2",
    "email": "test2@example.com",
    "password": "pass2",
    "address": "address2",
    "image": "image2"
}

sample_new_admin = {
    "name": "admin1",
    "email": "admin@concha.com",
    "password": "admin-pass",
    "address": "admin-address",
    "image": "admin-image"
}

sample_login_credentials_1 = {
    "username": "x@email.com",
    "password": "not-a-great-password"
}


@pytest.fixture
def test_fixture_user_1(client):
    url = base_url + '/auth/signup'
    data = sample_new_user_1

    res = client.post(url, json=data)
    created_user = res.json()["created_user_details"]
    created_user["password"] = data["password"]

    assert res.status_code == 201
    return created_user


@pytest.fixture
def test_fixture_user_2(client):
    url = base_url + '/auth/signup'
    data = sample_new_user_2

    res = client.post(url, json=data)
    created_user = res.json()["created_user_details"]
    created_user["password"] = data["password"]

    assert res.status_code == 201
    return created_user


@pytest.fixture
def test_fixture_user_admin(client):
    url = base_url + '/auth/signup'
    data = sample_new_admin

    res = client.post(url, json=data)
    schemas.UserNewResponseSchema(**res.json())  # schema validation for created user
    created_user = res.json()["created_user_details"]
    created_user["password"] = data["password"]

    assert res.status_code == 201
    return created_user


@pytest.fixture
def test_fixture_user_1_token(test_fixture_user_1, client):
    url = base_url + '/auth/login'
    data = {
        "username": test_fixture_user_1["email"],
        "password": test_fixture_user_1["password"]
    }

    res = client.post(url=url, data=data)

    return res


@pytest.fixture
def test_fixture_user_2_token(test_fixture_user_2, client):
    url = base_url + '/auth/login'
    data = {
        "username": test_fixture_user_2["email"],
        "password": test_fixture_user_2["password"]
    }

    res = client.post(url=url, data=data)

    return res


@pytest.fixture
def test_fixture_admin_token(test_fixture_user_admin, client):
    url = base_url + '/auth/login'
    data = {
        "username": test_fixture_user_admin["email"],
        "password": test_fixture_user_admin["password"]
    }

    res = client.post(url=url, data=data)

    return res


@pytest.fixture
def user_token_details(client, test_fixture_user_1, test_fixture_user_admin):
    url = base_url + '/auth/login'
    user_data = {
        "username": test_fixture_user_1["email"],
        "password": test_fixture_user_1["password"]
    }
    admin_data = {
        "username": test_fixture_user_admin["email"],
        "password": test_fixture_user_admin["password"]
    }
    user_res = client.post(url=url, data=user_data)
    admin_res = client.post(url=url, data=admin_data)
    user_login_res = schemas.Token(**user_res.json())
    admin_login_res = schemas.Token(**admin_res.json())
    user_payload = jwt.decode(user_login_res.token, settings.secret_key, algorithms=[settings.algorithm])
    admin_payload = jwt.decode(admin_login_res.token, settings.secret_key, algorithms=[settings.algorithm])
    return {"user_payload": user_payload, "admin_payload": admin_payload}


# Sample audio data for testing
sample_new_audio_data_1 = {
    "ticks": [-96.33, -96.33, -93.47, -89.03999999999999, -84.61, -80.18, -75.75, -71.32, -66.89, -62.46, -58.03, -53.6,
              -49.17, -44.74, -40.31],
    "selected_tick": 5,
    "session_id": 3448,
    "step_count": 1}

sample_new_audio_data_2 = {
    "ticks": [-69.33, -69.33, -39.47, -98.03999999999999, -48.61, -8.18, -57.75, -17.32, -66.89, -26.46, -58.03, -53.6,
              -49.17, -44.74, -40.31],
    "selected_tick": 6,
    "session_id": 3449,
    "step_count": 2}


@pytest.fixture
def test_fixture_audio_1(test_fixture_user_1, test_fixture_user_1_token, client):
    url = base_url + '/audio-data/new'
    data = sample_new_audio_data_1

    token = test_fixture_user_1_token.json()['token']

    params_user = {"email": test_fixture_user_1["email"]}
    headers_user = {"Authorization": f"Bearer {token}"}

    res = client.post(url=url, params=params_user, headers=headers_user, json=data)

    return res
