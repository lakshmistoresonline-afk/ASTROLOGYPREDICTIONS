import os
import pytest
from datetime import datetime
from flask import g
from app import create_app
from app.database.models import db, UserAccount, Chart, ReportRecord
from app.services.auth import verify_firebase_id_token, get_current_user_uid, login_required
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

def test_p04_r2_two_user_isolation(app_instance):
    with app_instance.app_context():
        uid_a = "user_alpha_r2"
        uid_b = "user_beta_r2"

        chart_data_a = {
            "name": "Alpha Chart R2",
            "birth_dob": "1990-09-10",
            "birth_tob": "14:30",
            "place": "Mumbai, India",
            "latitude": 19.0760,
            "longitude_coord": 72.8777,
            "timezone": "Asia/Kolkata"
        }
        cid_a = save_chart(uid_a, chart_data_a)
        assert cid_a is not None

        report_a = ReportRecord(
            report_id="rep_alpha_1",
            owner_uid=uid_a,
            chart_id=cid_a,
            report_type="CAREER",
            title="Alpha Career Report",
            content_json='{"score": 0.85}',
            engine_version="P0.3-R42"
        )
        db.session.add(report_a)
        db.session.commit()

        assert get_chart(uid_a, cid_a) is not None
        assert ReportRecord.query.filter_by(report_id="rep_alpha_1", owner_uid=uid_a).first() is not None

        assert get_chart(uid_b, cid_a) is None
        assert ReportRecord.query.filter_by(report_id="rep_alpha_1", owner_uid=uid_b).first() is None

        assert len(list_charts(uid_b)) == 0
        assert len(list_charts(uid_a)) == 1

def test_p04_r2_production_mock_token_rejection():
    old_env = os.environ.get("FLASK_ENV")
    os.environ["FLASK_ENV"] = "production"
    try:
        claims = verify_firebase_id_token("mock_token_user_alpha")
        assert claims is None
    finally:
        if old_env:
            os.environ["FLASK_ENV"] = old_env
        else:
            os.environ.pop("FLASK_ENV", None)

def test_protected_v315_hashes_p04_r2():
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
