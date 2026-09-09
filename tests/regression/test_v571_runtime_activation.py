import pytest
from datetime import datetime
from app import create_app
from app.database.models import db, Chart
from app.astrology.predictions.v57_prospective import V57ProspectiveLedgerRecord

def test_v571_runtime_activation_pipeline():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()

        # Test 1: Automatic ledger and snapshot creation with hash
        record = V57ProspectiveLedgerRecord(
            person_id="user_prod_1",
            domain="CAREER",
            event_type="promotion",
            prediction_text="Production promotion window active",
            evidence_snapshot={"natal": "strong", "transit": "favorable"},
            engine_version="V5.7.1"
        )

        assert record.prediction_id is not None
        assert record.snapshot_hash is not None
        assert record.verify_integrity() is True

        # Test 2: Tamper detection
        record.prediction_text = "Mutated text"
        assert record.verify_integrity() is False

        # Test 3: Location propagation check
        chart = Chart(id="loc-test-1", name="Location User", place="New Delhi, India", lat=28.61, lon=77.20, tz="Asia/Kolkata")
        db.session.add(chart)
        db.session.commit()

        fetched = db.session.get(Chart, "loc-test-1")
        assert fetched.place == "New Delhi, India"
        db.drop_all()
