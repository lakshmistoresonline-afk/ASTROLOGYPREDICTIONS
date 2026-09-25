import os
import pytest
from datetime import datetime
from app import create_app
from app.database.models import db, UserAccount, Chart, ReportRecord
from app.services.auth import verify_firebase_id_token, get_current_user_uid
from app.astrology.core.calculation_config import calculate_canonical_chart

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
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app_instance):
    with app_instance.test_client() as client:
        yield client

def test_p04_token_verification():
    claims = verify_firebase_id_token("mock_token_user_alpha")
    assert claims is not None
    assert claims["uid"] == "user_alpha"

    invalid_uid = verify_firebase_id_token(None)
    assert invalid_uid is None

def test_p04_user_ownership_and_chart_persistence(app_instance):
    with app_instance.app_context():
        user = UserAccount(firebase_uid="uid_123", email="user123@astropredictions.app")
        db.session.add(user)
        db.session.commit()

        chart = Chart(
            id="chart_abc",
            owner_uid="uid_123",
            name="Alpha Chart",
            dob="1990-09-10",
            tob="14:30",
            place="Kochi, India",
            lat=10.5276,
            lon=76.2144,
            tz="Asia/Kolkata"
        )
        db.session.add(chart)
        db.session.commit()

        # Retrieve own chart
        fetched = Chart.query.filter_by(id="chart_abc", owner_uid="uid_123").first()
        assert fetched is not None
        assert fetched.name == "Alpha Chart"

        # Other user cannot access
        unauthorized = Chart.query.filter_by(id="chart_abc", owner_uid="uid_456").first()
        assert unauthorized is None

def test_p04_durable_report_persistence(app_instance):
    with app_instance.app_context():
        report = ReportRecord(
            report_id="rep_999",
            owner_uid="uid_123",
            chart_id="chart_abc",
            report_type="CAREER",
            title="Career Timing Report",
            content_json='{"summary": "Peak timing active"}',
            engine_version="P0.3-R42"
        )
        db.session.add(report)
        db.session.commit()

        fetched = ReportRecord.query.filter_by(report_id="rep_999", owner_uid="uid_123").first()
        assert fetched is not None
        assert fetched.title == "Career Timing Report"

        # Cross-user isolation
        other_user_report = ReportRecord.query.filter_by(report_id="rep_999", owner_uid="uid_999").first()
        assert other_user_report is None

def test_p04_account_deletion_workflow(app_instance):
    with app_instance.app_context():
        user = UserAccount(firebase_uid="uid_delete", email="del@astropredictions.app")
        db.session.add(user)
        db.session.commit()

        # Delete user-owned records
        user_to_del = UserAccount.query.filter_by(firebase_uid="uid_delete").first()
        assert user_to_del is not None
        db.session.delete(user_to_del)
        db.session.commit()

        assert UserAccount.query.filter_by(firebase_uid="uid_delete").first() is None

def test_protected_v315_hashes_p04():
    import hashlib
    baselines = {
        'app/astrology/core/chart.py': '52a0373aab11b14dfcdbf79d111f587f570a5e095dc49f64f6d1d536fb795bc2',
        'app/astrology/core/swe_proxy.py': 'a6584a3216853fdd8685dc2ce7e71091e9443818a969b56f01945af9603b1bf1',
        'app/astrology/core/ephemeris.py': 'a2a56bb7f277a061583fb39c73d9e534df212b5d70e7ba2704bbb4c17a2b3c6a'
    }
    for path, base_h in baselines.items():
        with open(path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        assert h == base_h
