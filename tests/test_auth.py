"""
Tests for /auth endpoint
"""
import pytest
from jose import jwt

from server.config import settings

from psql_db import schemas
from psql_db.models import User

from tests.database import client, session

base_url = settings.base_url_test

# sample data sets for testing
sample_new_user = {
    "name": "test1",
    "email": "test1@example.com",
    "password": "pass1",
    "address": "address1",
    "image": "image1"
}

sample_login_credentials_1 = {
    "username": "x@email.com",
    "password": "not-a-great-password"
}


@pytest.fixture
def test_user(client):
    url = base_url + '/auth/signup'
    data = sample_new_user

    res = client.post(url, json=data)
    schemas.UserNewResponseSchema(**res.json())  # schema validation for created user
    created_user = res.json()["created_user_details"]
    created_user["password"] = data["password"]

    assert res.status_code == 201
    # print('return this. test_user=', created_user)
    return created_user


def test_auth_signup(session, test_user):
    res = session.query(User).filter(User.email == test_user["email"]).first()
    assert res.email == test_user["email"]
    session.close()


def test_auth_login_wrong_username(client):
    url = base_url + '/auth/login'
    data = sample_login_credentials_1

    res = client.post(url=url, data=data)

    assert res.status_code == 403
    assert res.json() == {'detail': f'No user found with email:{data["username"]}'}


def test_auth_correct_login(test_user, client):
    url = base_url + '/auth/login'
    data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }

    res = client.post(url=url, data=data)
    token = schemas.Token(**res.json())

    assert res.status_code == 200


def test_auth_verify_access_token(test_user, client):
    url = base_url + '/auth/login'
    data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    res = client.post(url=url, data=data)
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.token, settings.secret_key, algorithms=[settings.algorithm])

    user_id: str = payload.get('user_id')
    user_email: str = payload.get('user_email')
    is_admin: bool = payload.get('is_admin')

    assert user_id == test_user['id']
    assert user_email == test_user['email']
    pass
