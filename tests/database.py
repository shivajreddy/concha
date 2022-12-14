import pytest

from fastapi.testclient import TestClient

from server import app
from server.config import settings
from server.database import get_db, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_test_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()  # scope="module" as arg, for setup, destroy per module
def session():
    Base.metadata.drop_all(bind=engine)  # DROP all tables
    Base.metadata.create_all(bind=engine)  # CREATE all tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        # Base.metadata.drop_all(bind=engine)  # DROP all tables
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
