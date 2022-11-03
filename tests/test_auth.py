"""
Tests for /auth endpoint
"""

from server.config import settings
from jose import jwt

from psql_db import schemas
from psql_db.models import User

from .conftest import sample_login_credentials_1

base_url = settings.base_url_test


def test_auth_signup(session, test_fixture_user_1):
    res = session.query(User).filter(User.email == test_fixture_user_1["email"]).first()
    assert res.email == test_fixture_user_1["email"]
    session.close()


def test_auth_login_wrong_username(client, ):
    url = base_url + '/auth/login'
    data = sample_login_credentials_1

    res = client.post(url=url, data=data)

    assert res.status_code == 403
    assert res.json() == {'detail': f'No user found with email:{data["username"]}'}


def test_auth_correct_login(test_fixture_user_token, client):
    res = test_fixture_user_token

    assert res.status_code == 200
    schemas.Token(**res.json())


def test_auth_verify_user_token(test_fixture_user_1, user_token_details, client):
    payload = user_token_details["user_payload"]

    user_id: str = payload.get('user_id')
    user_email: str = payload.get('user_email')
    is_admin: bool = payload.get('is_admin')

    assert user_id == test_fixture_user_1['id']
    assert user_email == test_fixture_user_1['email']
    assert is_admin is False


def test_auth_verify_admin_token(test_fixture_user_admin, user_token_details, client):
    payload = user_token_details["admin_payload"]

    user_id: str = payload.get('user_id')
    user_email: str = payload.get('user_email')
    is_admin: bool = payload.get('is_admin')

    assert user_id == test_fixture_user_admin['id']
    assert user_email == test_fixture_user_admin['email']
    assert is_admin is True


def test_auth_wrong_token(test_fixture_user_1, test_fixture_user_token, client):
    url = base_url + '/user/delete'
    token = test_fixture_user_token.json()['token'] + "oops"

    # test -> admin deleting another existing user
    params_user = {"email": test_fixture_user_1["email"]}
    headers_user = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params_user, headers=headers_user)
    assert res.status_code == 401
    assert res.json() == {'detail': 'Could not validate credentials'}
