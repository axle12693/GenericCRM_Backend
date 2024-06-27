import falcon
from falcon import testing
import pytest
from app import create_app

@pytest.fixture
def client():
    return testing.TestClient(create_app())

def test_user_registration(client):
    response = client.simulate_post('/register', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status == falcon.HTTP_201
    assert response.json == {'message': 'User created successfully'}

def test_user_registration_duplicate(client):
    client.simulate_post('/register', json={'username': 'testuser', 'password': 'testpass'})
    response = client.simulate_post('/register', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status == falcon.HTTP_409

def test_user_login(client):
    client.simulate_post('/register', json={'username': 'testuser', 'password': 'testpass'})
    response = client.simulate_post('/login', json={'username': 'testuser', 'password': 'testpass'})
    assert response.status == falcon.HTTP_200
    assert 'token' in response.json

def test_protected_resource(client):
    client.simulate_post('/register', json={'username': 'testuser', 'password': 'testpass'})
    login_response = client.simulate_post('/login', json={'username': 'testuser', 'password': 'testpass'})
    token = login_response.json['token']

    response = client.simulate_get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert response.status == falcon.HTTP_200
    assert response.json == {'message': 'Hello, testuser!'}

def test_protected_resource_no_auth(client):
    response = client.simulate_get('/protected')
    assert response.status == falcon.HTTP_401