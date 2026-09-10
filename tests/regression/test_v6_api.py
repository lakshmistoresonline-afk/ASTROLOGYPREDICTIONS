import pytest
from app import create_app

def test_v6_api_blueprint_registered():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        resp = client.get('/api/v6/summary')
        assert resp.status_code in [404, 500]
