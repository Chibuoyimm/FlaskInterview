from jose import jwt
import pytest

from app.oauth2 import SECRET_KEY, ALGORITHM


# To test if a user is created or registered successfully
def test_create_user(client):
    res = client.post("/register", json={"first_name": "cactus", "last_name": "jack", "email": "cactusjack@gmail.com", "password": "cactus"})
    assert res.status_code == 201


# To test logging in a created user
def test_login_user(client):
    res = client.post("/login", json={"email": "cactusjack@gmail.com", "password": "cactus"})
    payload = jwt.decode(res.json["access_token"], SECRET_KEY, algorithms=ALGORITHM) # i think this does the verification
    id = payload.get("id")

    assert res.json["token_type"] == "bearer"
    assert res.status_code == 200


# To test invalid login credentials
@pytest.mark.parametrize("email, password, status_code", [
    ("stuff@gmail.com", "bigsteppers", 403),
    ("bigsteppers@gmail.com", "wrong", 403),
    ("wrong@gmail.com", "wrong", 403),
    (None, "bigsteppers", 403),
    ("bigsteppers@gmail.com", None, 403)
    ])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", json={"email": email, "password": password})
    assert res.status_code == status_code
