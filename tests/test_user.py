"""
Tests for /user endpoint
"""
from server.config import settings

from psql_db import schemas
from psql_db.models import User

from tests.database import client, session

base_url = settings.base_url_test


def test_user_get_all(client):
    url = base_url + '/user/all'
    res = client.get(url=url)

    # test -> get all users
    assert res.status_code == 200
    schemas.UserAllSchema(**res.json())  # response schema validation
    assert isinstance(res.json()["all_users"], list)  # only list, not other collections


def test_user_search(client, test_fixture_user_1):
    url = base_url + '/user/search'

    # test -> /user root
    correct_body = {
        "email": test_fixture_user_1["email"]
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
    schemas.UserDbSchema(**res.json()['search_result'][0])  # schema validation
    assert len(res.json()['search_result']) >= 1

    # test -> only same part of email given
    partial_email_body = {
        "email": "1@example.com"
    }
    res = client.get(url=url, json=partial_email_body)
    assert res.status_code == 200
    schemas.UserDbSchema(**res.json()['search_result'][0])      # schema validation
    assert len(res.json()['search_result']) >= 1

    # test -> not an actual email, just a string
    wrong_email_format_body = {
        "email": "not-an-email"
    }
    res = client.get(url=url, json=wrong_email_format_body)
    assert res.status_code == 422


def test_user_get_by_id(client, test_fixture_user_1):
    url = base_url + '/user/id'

    # test -> correct id given
    params = {"user_id": test_fixture_user_1["id"]}
    res = client.get(url=url, params=params)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())        # schema validation

    # test -> give email instead of id
    wrong_params = {"user_email": test_fixture_user_1["email"]}
    res = client.get(url=url, params=wrong_params)
    assert res.status_code == 422


def test_user_email(client, test_fixture_user_1):
    url = base_url + '/user/email'

    # test -> correct email given
    params = {"user_email": test_fixture_user_1["email"]}
    res = client.get(url=url, params=params)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())        # schema validation

    # test -> give id instead of email
    wrong_params = {"user_id": test_fixture_user_1["id"]}
    res = client.get(url=url, params=wrong_params)
    assert res.status_code == 422


def test_user_update(test_fixture_user_1, test_fixture_user_2, test_fixture_user_token, client):
    url = base_url + '/user/update'
    token = test_fixture_user_token.json()['token']

    headers_user_1 = {"Authorization": f"Bearer {token}"}

    # test -> try using pre-existing email
    res = client.patch(url=url, headers=headers_user_1, json={"email": test_fixture_user_1["email"]})
    assert res.status_code == 404
    assert res.json() == {'detail': f'User already exists with email: {test_fixture_user_1["email"]}'}

    # test -> update name
    new_data_name = {"name": "user3"}
    res = client.patch(url=url, headers=headers_user_1, json=new_data_name)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())        # schema validation
    assert new_data_name["name"] == res.json()["name"]

    # test -> update address
    new_data_address = {"address": "updated-address1"}
    res = client.patch(url=url, headers=headers_user_1, json=new_data_address)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())        # schema validation
    assert new_data_address["address"] == res.json()["address"]

    # test -> update image
    new_data_image = {"image": "updated-image1"}
    res = client.patch(url=url, headers=headers_user_1, json=new_data_image)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())        # schema validation
    assert new_data_image["image"] == res.json()["image"]


def test_user_update_email(test_fixture_user_1, test_fixture_user_token, client):
    url = base_url + '/user/update'
    token = test_fixture_user_token.json()['token']

    headers_user_1 = {"Authorization": f"Bearer {token}"}

    # test -> update email
    new_data_email = {"email": "updated-test1@example.com"}
    res = client.patch(url=url, headers=headers_user_1, json=new_data_email)
    assert res.status_code == 200
    schemas.UserResponseSchema(**res.json())        # schema validation
    assert new_data_email["email"] == res.json()["email"]


def test_user_delete(test_fixture_user_1, test_fixture_user_2, test_fixture_user_token, client, session):
    url = base_url + '/user/delete'
    token = test_fixture_user_token.json()['token']

    # test -> delete an existing user
    params_user_1 = {"email": test_fixture_user_1["email"]}
    headers_user_1 = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params_user_1, headers=headers_user_1)
    assert res.status_code == 200
    assert res.json() == {'result': f'user with email {test_fixture_user_1["email"]} is deleted'}

    # test -> try to delete non-exiting user
    params_wrong = {"email": "wrong-mail@email.com"}
    res = client.delete(url=url, params=params_wrong, headers=headers_user_1)
    assert res.status_code == 404
    assert res.json() == {'detail': f'No user with email: {params_wrong["email"]}'}

    # test -> try to delete twice
    user_query = session.query(User).filter(User.email == test_fixture_user_1["email"])
    user_query.delete()
    session.commit()
    res = client.delete(url=url, params=params_user_1, headers=headers_user_1)
    assert res.status_code == 404
    assert res.json() == {'detail': f'No user with email: {test_fixture_user_1["email"]}'}


def test_user_delete_other_users(test_fixture_user_2, test_fixture_user_token, client, session):
    url = base_url + '/user/delete'
    token = test_fixture_user_token.json()['token']

    # test -> try deleting another user's account
    params_user_2 = {"email": test_fixture_user_2["email"]}
    headers_user_1 = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params_user_2, headers=headers_user_1)
    assert res.status_code == 403
    assert res.json() == {'detail': 'You can only delete your account, or have admin privileges'}


def test_user_admin_delete_other_users(test_fixture_user_1, test_fixture_admin_token, client):
    url = base_url + '/user/delete'
    token = test_fixture_admin_token.json()['token']  # admins token

    # test -> admin deleting another existing user
    params_user = {"email": test_fixture_user_1["email"]}
    headers_admin = {"Authorization": f"Bearer {token}"}
    res = client.delete(url=url, params=params_user, headers=headers_admin)
    assert res.status_code == 200
    assert res.json() == {'result': f'user with email {test_fixture_user_1["email"]} is deleted'}
