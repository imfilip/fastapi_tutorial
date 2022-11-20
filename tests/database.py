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

# def override_get_db(): #-> Generator: # from typing
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# @pytest.fixture
# def session():
# I've finished here!!!

@pytest.fixture(scope = "function") # the argument scope with 'module' ensures that this fixtures are run once through all tests in one module (in my case module e.g. 'test_users')
# But this cause that our tests are dependent on previus tests in the module - it is BAD PRACTICE.
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope = "function") # 
def client(session):
    def override_get_db(): #-> Generator: # from typing
        db = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    # Alternative solution with alembic:
    # command.downgrade(alembic_cfg, "base") # Downgrade is not working. On the video he has not showed if it is correctly implemented. I won't spend too much time on that.
    # alembic_cfg = Config("alembic.ini")
    # command.upgrade(alembic_cfg, "head")
    # yield TestClient(app)

    # Base.metadata.drop_all(bind=engine)
    # # The flexibility 'yield' is providing:
    # # run our code before we run our test
    # Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) # return TestClient(app)
    # Base.metadata.drop_all(bind=engine) # 2) Perfectly would be to drop DB when test starts.
    # run our code after our test finishes
    # great solution - everytime you run test the DB is created and when the test is finished, the DB is dropped

