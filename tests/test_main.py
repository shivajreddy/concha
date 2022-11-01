from fastapi.testclient import TestClient

from server import app

from server.config import settings

# client = TestClient(app)

base_url = settings.base_url_dev


# Sample test
def test_sample():
    url = base_url
    with TestClient(app) as client:
        res = client.get(url=base_url)


# Get all users
def test_get_all_users():
    a