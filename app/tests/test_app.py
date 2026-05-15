import pytest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_index(client):
    r = client.get('/')
    assert r.status_code == 200
    assert b'DevOps Project API' in r.data

def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert b'healthy' in r.data

def test_metrics(client):
    r = client.get('/metrics')
    assert r.status_code == 200
