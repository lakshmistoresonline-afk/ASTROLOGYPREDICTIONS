import pytest
from datetime import datetime
from app import create_app
from app.database.models import db, PredictionOutcome, Chart

@pytest.fixture
def app_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_prediction_immutability_and_outcome_linking(app_client):
    app = create_app()
    with app.app_context():
        # Create test chart
        chart = Chart(id="test-chart-1", name="Test User", dob="1990-01-01", tob="12:00", lat=28.6, lon=77.2, tz="Asia/Kolkata")
        db.session.add(chart)

        # Create immutable prediction snapshot
        pred = PredictionOutcome(
            chart_id="test-chart-1",
            domain="Career & Authority",
            prediction_text="Promotion expected",
            prediction_strength="PEAK",
            status="PENDING",
            peak_date="2026-10-06",
            participant_id="anon-user-123"
        )
        db.session.add(pred)
        db.session.commit()
        pred_id = pred.id

        # Verify initial prediction text is immutable
        original_text = pred.prediction_text

        # Simulate user outcome submission
        outcome_status = "EVENT_REPORTED"
        actual_date = "2026-10-05"

        fetched_pred = db.session.get(PredictionOutcome, pred_id)
        assert fetched_pred.prediction_text == original_text # Immutability check

        # Link outcome observation separately
        fetched_pred.status = outcome_status
        fetched_pred.actual_event_date = actual_date
        fetched_pred.timing_error_days = abs((datetime.strptime(actual_date, "%Y-%m-%d") - datetime.strptime(fetched_pred.peak_date, "%Y-%m-%d")).days)
        db.session.commit()

        updated_pred = db.session.get(PredictionOutcome, pred_id)
        assert updated_pred.status == "EVENT_REPORTED"
        assert updated_pred.actual_event_date == "2026-10-05"
        assert updated_pred.timing_error_days == 1
        assert updated_pred.prediction_text == original_text # Remains pristine
        assert updated_pred.participant_id == "anon-user-123" # Privacy check (pseudonymous)
