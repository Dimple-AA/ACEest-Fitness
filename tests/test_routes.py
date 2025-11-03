import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

import pytest
from app import app, init_db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    # ✅ Initialize the SQLite DB before tests
    with app.app_context():
        init_db()
    
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_api_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200

def test_api_workouts(client):
    response = client.get('/api/workouts')
    assert response.status_code == 200
