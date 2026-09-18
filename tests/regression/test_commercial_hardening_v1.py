import os
import pytest
from app import create_app
from app.database.models import db, UserAccount, OrderRecord, PaymentSettings
from app.services.commercial import PaymentService

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
        user = UserAccount(firebase_uid="uid_admin", email="admin@astropredictions.app", role="admin")
        db.session.add(user)
        db.session.commit()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_admin_upi_payment_workflow(client):
    with client.session_transaction() as sess:
        sess["firebase_id_token"] = "mock_token_uid_admin"
        sess["firebase_uid"] = "uid_admin"

    res = client.post("/admin/payments/settings", data={
        "upi_id": "teststore@upi",
        "payee_name": "Test Store",
        "is_active": "1",
        "instructions": "Pay via test UPI"
    }, follow_redirects=True)
    assert res.status_code == 200

    settings = PaymentService.get_settings()
    assert settings.upi_id == "teststore@upi"

    order = PaymentService.create_order(user_id=1, product_id="plus_monthly")
    assert order.id is not None

    PaymentService.submit_payment_proof(order.id, "UTR999888777")

    success = PaymentService.verify_and_approve_order(order.id)
    assert success is True

def test_mobile_api_dashboard(client):
    with client.session_transaction() as sess:
        sess["firebase_id_token"] = "mock_token_uid_admin"
        sess["firebase_uid"] = "uid_admin"

    res = client.get("/api/v1/mobile/dashboard")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"

def test_protected_v315_hashes_hardening_v1():
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
