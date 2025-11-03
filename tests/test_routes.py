import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_register_user(client):
    response = client.post('/users', data={
        'name': 'TestUser',
        'age': 25,
        'gender': 'Male',
        'height': 175,
        'weight': 70
    }, follow_redirects=True)
    assert response.status_code == 200
