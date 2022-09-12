import pytest
from app.main import app
from app.oauth2 import create_access_token



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        yield app.test_client()


# Creating an acess token for user 1
@pytest.fixture
def token():
    return create_access_token({"id": 1})


# Creating an access token for user 2
@pytest.fixture
def another_token():
    return create_access_token({"id": 2})





