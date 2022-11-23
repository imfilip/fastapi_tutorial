# conftest.py is automatically accessible by pytest. So you can put here all fixtures.

import pytest
from .database import client, session # I should not do this in that way, but I am lazy. I should have copied all fixtures to this file.
from app.oauth2 import create_acces_token
from app import models


@pytest.fixture
def test_user(client):
    user_data = {"email": "imfilip@imfilip.com",
                 "password": "admin"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "imfilip1@imfilip.com",
                 "password": "admin1"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_acces_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first_content",
            "owner_id": test_user["id"]
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user["id"]
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user["id"]
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user2["id"]
        }
    ]
    
    # The following solution was proposed by the course author. My enhencment was to use lambda:
    # def create_post_model(post):
    #     return models.Posts(**post)
    # post_map = map(create_post_model, posts_data)
    
    post_map = map(lambda post: models.Posts(**post), posts_data)

    posts = list(post_map)
    session.add_all(posts)  
    session.commit()

    posts_return = session.query(models.Posts).all()

    return posts_return

