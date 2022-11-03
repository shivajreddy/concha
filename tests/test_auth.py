"""
Tests for /auth endpoint
"""
from server.config import settings

from psql_db import schemas

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


def test_auth_signup(client):
    url = base_url + '/auth/signup'
    data = sample_new_user

    res = client.post(url, json=data)

    created_user = schemas.UserNewResponseSchema(**res.json())  # schema validation for created user

    assert res.status_code == 201


def test_wrong_username_auth_login(client):
    url = base_url + '/auth/login'
    data = sample_login_credentials_1

    res = client.post(url=url, data=data)

    assert res.status_code == 403
    assert res.json() == {'detail': f'No user found with email:{data["username"]}'}


def test_correct_name_wrong_password_auth_login(client):
    signup_url = base_url + '/auth/signup'
    login_url = base_url + '/auth/login'
    signup_data = sample_new_user

    data = {
        "username": signup_data["email"],
        "password": signup_data["password"]
    }

    client.post(signup_url, json=signup_data)

    res = client.post(url=login_url, data=data)

    token = schemas.Token(**res.json())

    assert res.status_code == 200
