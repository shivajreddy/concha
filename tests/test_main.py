from fastapi.testclient import TestClient

from server import app

from server.config import settings

# client = TestClient(app)

base_url = settings.base_url_dev


# base_url = "http://localhost:8000"


# Sample test
def test_sample():
    url = base_url
    print("url = ", url)
    with TestClient(app) as client:
        res = client.get(url=url)

        assert res.status_code == 200


# Get all users
def test_get_all_users():
    url = base_url + '/user/all'
    print("url =", url)
    with TestClient(app) as client:
        res = client.get(url=url)

        assert res.status_code == 200

        # test the response type and values
        print("json=", res.json())
