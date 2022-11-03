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
def test_fixture_user_token(test_fixture_user_1, client):
    url = base_url + '/auth/login'
    data = {
        "username": test_fixture_user_1["email"],
        "password": test_fixture_user_1["password"]
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
