import os
import pytest
from app import create_app
from app.database.models import db, UserAccount, Chart, PredictionOutcome
from app.services.auth import verify_firebase_id_token

@pytest.fixture(autouse=True)
def set_testing_env():
    os.environ["FLASK_ENV"] = "testing"
    yield
    os.environ.pop("FLASK_ENV", None)

@pytest.fixture
def app_instance():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app_instance):
    with app_instance.test_client() as client:
        yield client

def test_p04_r3_single_dashboard_route(app_instance):
    routes = [rule.rule for rule in app_instance.url_map.iter_rules()]
    dashboard_routes = [r for r in routes if r == "/dashboard"]
    assert len(dashboard_routes) == 1

def test_p04_r3_idor_outcome_protection(app_instance, client):
    with app_instance.app_context():
        uid_a = "user_a_sec"
        uid_b = "user_b_sec"

        chart_a = Chart(id="ch_a", owner_uid=uid_a, name="Chart A", dob="1990-09-10", tob="14:30")
        db.session.add(chart_a)
        db.session.commit()

        pred = PredictionOutcome(
            id=777,
            chart_id="ch_a",
            domain="CAREER",
            prediction_text="Test prediction",
            peak_date="2026-01-01"
        )
        db.session.add(pred)
        db.session.commit()

    # Attempt update as User B (mock token user_b_sec) without owning chart
    with client.session_transaction() as sess:
        sess["firebase_id_token"] = "mock_token_user_b_sec"
        sess["firebase_uid"] = "user_b_sec"

    res = client.post("/api/v1/outcome/update", json={"id": 777, "actual_date": "2026-01-01"})
    assert res.status_code in [403, 404]

def test_p04_r3_admin_key_elevation_removed(app_instance, client):
    res = client.post("/api/v1/user/settings", json={"admin_key": "astro-predictions-2026"})
    with client.session_transaction() as sess:
        assert sess.get("is_admin") is not True

def test_protected_v315_hashes_p04_r3():
    import hashlib
    baselines = {
        'app/astrology/core/chart.py': 'd755a5d501ff38769a42f15ecaecf825538cac2afc948e3aa74f66ea2ed3900d',
        'app/astrology/core/swe_proxy.py': 'a6584a3216853fdd8685dc2ce7e71091e9443818a969b56f01945af9603b1bf1',
        'app/astrology/core/ephemeris.py': 'a2a56bb7f277a061583fb39c73d9e534df212b5d70e7ba2704bbb4c17a2b3c6a'
    }
    for path, base_h in baselines.items():
        with open(path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        assert h == base_h
