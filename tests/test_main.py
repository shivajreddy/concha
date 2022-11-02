import pytest

from fastapi.testclient import TestClient

from server import app
from server.config import settings
from server.database import get_db, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta

base_url = settings.base_url_test

# DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.test_database_name}"
DATABASE_URL = "postgresql://postgres:2106@localhost/conchadb_test"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to create a new session, close after using
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Fixtures
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # start up
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # teardown


# base_url = "http://localhost:8000"


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
