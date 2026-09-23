import os
import pytest
from app import create_app
from app.database.models import db, UserAccount, OrderRecord, SubscriptionRecord, EntitlementRecord
from app.services.commercial import EntitlementService, PaymentService, AttributionService, AnalyticsService, AdService

@pytest.fixture(autouse=True)
def set_testing_env():
    os.environ["FLASK_ENV"] = "testing"
    yield
    os.environ.pop("FLASK_ENV", None)

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = UserAccount(id=1, firebase_uid="uid_test", email="test@astropredictions.app")
        db.session.add(user)
        db.session.commit()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_pricing_page(client):
    res = client.get("/pricing")
    assert res.status_code == 200
    assert b"Simple, Transparent Pricing" in res.data
    assert b"Astro Plus" in res.data

def test_checkout_and_fulfillment(client):
    with client.session_transaction() as sess:
        sess["firebase_id_token"] = "mock_token_uid_test"
        sess["firebase_uid"] = "uid_test"

    res = client.get("/checkout/plus_monthly")
    assert res.status_code == 200
    assert b"Complete UPI Payment" in res.data

    # Fulfill order
    success = PaymentService.fulfill_order("order_plus_monthly_123", "pay_abc123", 499.00)
    assert success is True

    # Verify Entitlement
    assert EntitlementService.has_subscription(1) is True
    assert EntitlementService.is_ad_free(1) is True
    assert AdService.is_ads_enabled(1) is False

def test_attribution_service():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        AttributionService.record("anon_xyz", "google", "cpc", "launch", "ref123")
        db.drop_all()

def test_analytics_service():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        AnalyticsService.log_event("landing_view", "anon_xyz", {"dob": "1990-09-10", "page": "home"})
        db.drop_all()

def test_protected_v315_hashes_commercial():
    import hashlib
    baselines = {
        'app/astrology/core/chart.py': '3875b891f1c2cd058f9859bd7c43f0be42c0ae40b346b8fdf826a336448103e5',
        'app/astrology/core/swe_proxy.py': 'a6584a3216853fdd8685dc2ce7e71091e9443818a969b56f01945af9603b1bf1',
        'app/astrology/core/ephemeris.py': 'a2a56bb7f277a061583fb39c73d9e534df212b5d70e7ba2704bbb4c17a2b3c6a'
    }
    for path, base_h in baselines.items():
        with open(path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        assert h == base_h
