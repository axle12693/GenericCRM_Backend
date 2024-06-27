import falcon
from falcon import testing
import pytest

from app import create_app

@pytest.fixture
def client():
    return testing.TestClient(create_app())

def test_example(client):
    response = client.simulate_get('/example')
    assert response.status == falcon.HTTP_200
    assert response.json == {'message': 'Hello, world!'}