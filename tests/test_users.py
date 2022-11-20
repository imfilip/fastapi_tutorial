
import pytest
from app import schemas
# from .database import client, session
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    # print(res.json())
    print(res.json().get("message"))
    assert res.json().get("message") == "chyba nie?"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {"email": "jakis123@123.pl", "password": "pass123"})
    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "jakis123@123.pl"
    assert res.status_code == 201

def test_login_user(client, test_user):

    res = client.post("/login", data = {"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@213455.com", "admin", 403),
    ("imfilip@imfilip.com", "passssssss", 403),
    ("wrongemail@213455.com", "passssssss", 403),
    (None, "passssssss", 422),
    ("imfilip@imfilip.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    print(res)
    assert res.status_code == status_code
#     assert res.json().get("detail") == "Invalid credentials."