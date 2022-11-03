"""
Tests for /user endpoint
"""
from server.config import settings

from psql_db import schemas
from psql_db.models import User

from tests.database import client, session

base_url = settings.base_url_test


# Get all users
def test_user_get_all(client):
    url = base_url + '/user/all'
    res = client.get(url=url)

    assert res.status_code == 200
    schemas.UserAllSchema(**res.json())  # response schema validation
    assert isinstance(res.json()["all_users"], list)  # only list, not other collections


# TODO
# user details test
# user detail pure types test
# all routes tests for status codes, both pass and fail status codes

def test_user_search(client, test_fixture_user):
    url = base_url + '/user/search'

    # test -> /user root
    correct_body = {
        "email": test_fixture_user["email"]
    }
    res = client.get(url=url, json=correct_body)
    assert res.status_code == 200
    assert isinstance(res.json()["search_result"], list)

    # test -> unacceptable body sent
    wrong_body_1 = {
        "name": "name1",
        "email": "email1@email.com"
    }
    res = client.get(url=url, json=wrong_body_1)
    assert res.status_code == 403
    assert res.json() == {"detail": "Only email or name should be provided not both"}

    # test -> no existing user
    unknown_user_body = {
        "name": "name1",
    }
    res = client.get(url=url, json=unknown_user_body)
    assert res.status_code == 200
    assert len(res.json()['search_result']) == 0

    # test -> no existing email
    unknown_email_body = {
        "name": "name1",
    }
    res = client.get(url=url, json=unknown_email_body)
    assert res.status_code == 200
    assert len(res.json()['search_result']) == 0

    # test -> only same part of name given
    partial_name_body = {
        "name": 'tes'
    }
    res = client.get(url=url, json=partial_name_body)
    assert res.status_code == 200
    schemas.UserDbSchema(**res.json()['search_result'][0])
    assert len(res.json()['search_result']) >= 1

    # test -> only same part of email given
    partial_email_body = {
        "email": "1@example.com"
    }
    res = client.get(url=url, json=partial_email_body)
    assert res.status_code == 200
    schemas.UserDbSchema(**res.json()['search_result'][0])
    assert len(res.json()['search_result']) >= 1

    # test -> not an actual email, just a string
    wrong_email_format_body = {
        "email": "not-an-email"
    }
    res = client.get(url=url, json=wrong_email_format_body)
    assert res.status_code == 422


def test_user_get_by_id(client, test_fixture_user):
    url = base_url + '/user/id'

    # test -> correct id given
    params = {"user_id": test_fixture_user["id"]}
    res = client.get(url=url, params=params)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())

    # test -> give email instead of id
    wrong_params = {"user_email": test_fixture_user["email"]}
    res = client.get(url=url, params=wrong_params)
    assert res.status_code == 422


def test_user_email(client, test_fixture_user):
    url = base_url + '/user/email'

    # test -> correct email given
    params = {"user_email": test_fixture_user["email"]}
    res = client.get(url=url, params=params)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())

    # test -> give id instead of email
    wrong_params = {"user_id": test_fixture_user["id"]}
    res = client.get(url=url, params=wrong_params)
    assert res.status_code == 422


def test_user_update(client, test_fixture_user):
    url = base_url + '/user/update'

    # print('res = ', res, res.json())
    # print("test_user =", test_user)

    # test -> correct update details
    # TODO
    pass


def test_user_delete(test_fixture_user, test_fixture_user_token, client, session):
    url = base_url + '/user/delete'
    token = test_fixture_user_token.json()['token']

    # test -> delete an existing user
    params = {"email": test_fixture_user["email"]}
    headers = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'result': f'user with email {test_fixture_user["email"]} is deleted'}

    # test -> try to delete non-exiting user
    params_wrong = {"email": "wrong-mail@email.com"}
    headers = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params_wrong, headers=headers)
    assert res.status_code == 404
    assert res.json() == {'detail': f'No user with email: {params_wrong["email"]}'}

    # test -> try to delete twice
    # TODO
    params = {"email": test_fixture_user["email"]}
    headers = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params, headers=headers)
    res = client.delete(url=url, params=params, headers=headers)
