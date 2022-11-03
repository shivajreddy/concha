from server.config import settings

from psql_db import schemas

from tests.database import client, session

base_url = settings.base_url_test


# Sample test
def test_sample(client):
    url = base_url
    res = client.get(url=url)

    assert res.status_code == 200


def test_empty_route(client):
    url = base_url + '/no'
    res = client.get(url)
    assert res.status_code == 404
    assert res.json() == {"detail": "Not Found"}
