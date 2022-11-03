"""
Tests for /user endpoint
"""
from server.config import settings

from psql_db import schemas

from tests.database import client, session

base_url = settings.base_url_test


# Get all users
def test_get_all_users(client):
    url = base_url + '/user/all'
    res = client.get(url=url)

    assert res.status_code == 200

# TODO
# user details test
# user detail pure types test
# all routes tests for status codes, both pass and fail status codes
