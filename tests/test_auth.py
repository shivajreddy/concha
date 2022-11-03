"""
Tests for /auth endpoint
"""

from server.config import settings
from jose import jwt

from psql_db import schemas
from psql_db.models import User

from .conftest import sample_login_credentials_1

base_url = settings.base_url_test


def test_auth_signup(session, test_user):
    res = session.query(User).filter(User.email == test_user["email"]).first()
    assert res.email == test_user["email"]
    session.close()


def test_auth_login_wrong_username(client, ):
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


def test_auth_verify_user_token(test_user, user_token_details, client):
    payload = user_token_details["user_payload"]

    user_id: str = payload.get('user_id')
    user_email: str = payload.get('user_email')
    is_admin: bool = payload.get('is_admin')

    assert user_id == test_user['id']
    assert user_email == test_user['email']
    assert is_admin is False


def test_auth_verify_admin_token(test_user_admin, user_token_details, client):

    payload = user_token_details["admin_payload"]

    user_id: str = payload.get('user_id')
    user_email: str = payload.get('user_email')
    is_admin: bool = payload.get('is_admin')

    assert user_id == test_user_admin['id']
    assert user_email == test_user_admin['email']
    assert is_admin is True
