import os
import pytest
from datetime import datetime
from app import create_app
from app.database.models import db, UserAccount, Chart, ReportRecord
from app.services.auth import verify_firebase_id_token, get_current_user_uid
from app.astrology.store import save_chart, list_charts, get_chart, delete_chart

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

def test_p04_r1_token_verification():
    claims = verify_firebase_id_token("mock_token_user_alpha")
    assert claims is not None
    assert claims["uid"] == "user_alpha"

    invalid_claims = verify_firebase_id_token(None)
    assert invalid_claims is None

def test_p04_r1_owner_scoped_store(app_instance):
    with app_instance.app_context():
        uid_a = "user_alpha"
        uid_b = "user_beta"

        chart_data_a = {
            "name": "Alpha Chart",
            "birth_dob": "1990-09-10",
            "birth_tob": "14:30",
            "place": "Kochi, India",
            "latitude": 10.5276,
            "longitude_coord": 76.2144,
            "timezone": "Asia/Kolkata"
        }
        cid_a = save_chart(uid_a, chart_data_a)
        assert cid_a is not None

        # User A lists charts
        charts_a = list_charts(uid_a)
        assert len(charts_a) == 1
        assert charts_a[0]["id"] == cid_a

        # User B lists charts -> should be empty
        charts_b = list_charts(uid_b)
        assert len(charts_b) == 0

        # User B cannot get User A chart
        fetched_by_b = get_chart(uid_b, cid_a)
        assert fetched_by_b is None

        # User A gets User A chart
        fetched_by_a = get_chart(uid_a, cid_a)
        assert fetched_by_a is not None
        assert fetched_by_a["name"] == "Alpha Chart"

def test_p04_r1_durable_report_persistence(app_instance):
    with app_instance.app_context():
        report = ReportRecord(
            report_id="rep_101",
            owner_uid="user_alpha",
            chart_id="chart_123",
            report_type="CAREER",
            title="Career Timing Snapshot",
            content_json='{"analysis": "Peak transit active"}',
            engine_version="P0.3-R42"
        )
        db.session.add(report)
        db.session.commit()

        # User A retrieves report
        fetched = ReportRecord.query.filter_by(report_id="rep_101", owner_uid="user_alpha").first()
        assert fetched is not None
        assert fetched.title == "Career Timing Snapshot"

        # User B cannot retrieve report
        unauthorized = ReportRecord.query.filter_by(report_id="rep_101", owner_uid="user_beta").first()
        assert unauthorized is None

def test_protected_v315_hashes_p04_r1():
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
