from server.config import settings

from tests.database import client, session

base_url = settings.base_url_test


# Sample test
def test_sample(client):
    url = base_url
    print("url = ", url)
    res = client.get(url=url)

    assert res.status_code == 200


def test_empty_route(client):
    url = base_url + '/no'
    res = client.get(url)
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}


""" checking schemas
result_user = schemas.UserOut(**res.json())
UserOut is just a sample name
"""


# Get all users
def test_get_all_users(client):
    url = base_url + '/user/all'
    print("url =", url)
    res = client.get(url=url)

    print("this is the res", res)
    # assert res.status_code == 200


def test_post_user(client):
    url = base_url + '/auth/signup'
    data = {
        "name": "name1",
        "email": "name1@example.com",
        "password": "pass1",
        "address": "address1",
        "image": "image1"
    }

    res = client.post(url, json=data)
    assert res.status_code == 201
