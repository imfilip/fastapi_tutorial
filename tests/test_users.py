# Notes to remember:
# pytest -v -s: increased verbosity + printing feature
# --disable-warnings
# -x: stop conducting further tests if an error occured

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base

from alembic.config import Config
from alembic import command

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:admin@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine) # Take a look at solution with fixture client

# Base = declarative_base()

def override_get_db(): #-> Generator: # from typing
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# @pytest.fixture
# def session():
# I've finished here!!!


@pytest.fixture
def client():
    # Alternative solution with alembic:
    # command.downgrade(alembic_cfg, "base") # Downgrade is not working. On the video he has not showed if it is correctly implemented. I won't spend too much time on that.
    # alembic_cfg = Config("alembic.ini")
    # command.upgrade(alembic_cfg, "head")
    # yield TestClient(app)

    Base.metadata.drop_all(bind=engine)
    # The flexibility 'yield' is providing:
    # run our code before we run our test
    Base.metadata.create_all(bind=engine)
    yield TestClient(app) # return TestClient(app)
    # Base.metadata.drop_all(bind=engine) # 2) Perfectly would be to drop DB when test starts.
    # run our code after our test finishes
    # great solution - everytime you run test the DB is created and when the test is finished, the DB is dropped


def test_root(client):
    res = client.get("/")
    # print(res.json())
    print(res.json().get("message"))
    assert res.json().get("message") == "chyba nie?"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email": "jakis12@123.pl", "password": "pass123"})
    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "jakis12@123.pl"
    assert res.status_code == 201