import os
import sys
import json
import uuid
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart, PredictionOutcome
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engines.career import CareerPredictionEngine

def run_realtime_session():
    os.environ["FLASK_SECRET_KEY"] = "beta-test-key"
    app = create_app()

    # 1. PARTICIPANT DATA (Simulated)
    # Target: Steve Jobs 1980 Breakthrough
    birth_dt = datetime(1955, 2, 24, 19, 15)
    lat, lon, tz = 37.77, -122.42, "America/Los_Angeles"
    event_actual_date = "1980-12-12"

    print("\n--- PHASE 1: PREDICTION GENERATION ---")
    with app.app_context():
        # Create unique chart entry
        chart_id = str(uuid.uuid4())[:8]
        chart_obj = calculate_chart_data(birth_dt, lat, lon, tz)

        db_chart = Chart(id=chart_id, name="Beta Participant 01", dob="1955-02-24", tob="19:15")
        db_chart.set_data(chart_obj.model_dump())
        db.session.add(db_chart)

        # Run Frozen V3.15 Engine
        # Simulation Date: 30 days before event
        sim_date = datetime.strptime(event_actual_date, "%Y-%m-%d") - timedelta(days=30)
        prediction = CareerPredictionEngine.get_prediction(chart_obj, sim_date)

        print(f"Generated Prediction: {prediction.prediction_strength} ({prediction.score}%)")
        print(f"Predicted Peak: {prediction.timing_window.get('peak')}")

        # 2. SAVE IMMUTABLE SNAPSHOT
        snapshot = PredictionOutcome(
            chart_id=chart_id,
            group_id="BETA_GROUP_1",
            participant_id="USER_001",
            session_id="SESS_999",
            engine_version="V3.15",
            domain="Career & Authority",
            prediction_strength=prediction.prediction_strength,
            confluence_score=prediction.score / 100.0,
            quality_score=prediction.quality_score,
            prediction_text=prediction.summary,
            evidence_snapshot=json.dumps([e.model_dump() for e in prediction.evidence_chain]),
            start_date=prediction.timing_window.get("activation"),
            peak_date=prediction.timing_window.get("peak"),
            end_date=prediction.timing_window.get("decline"),
            proximity_weight=prediction.timing_window.get("proximity_weight"),
            status="PENDING",
            source_type="SYNTHETIC" # V3.15 Calibration
        )
        db.session.add(snapshot)
        db.session.commit()
        s_id = snapshot.id
        print(f"Snapshot Saved! ID: {s_id} (Engine V3.15 Locked)")

    print("\n--- PHASE 2: OUTCOME RECORDING ---")
    with app.app_context():
        # User reports event occurred on 1980-12-12
        s = PredictionOutcome.query.get(s_id)
        s.status = "OCCURRED"
        s.actual_event_date = event_actual_date
        s.event_description = "Apple IPO - Huge professional breakthrough."
        s.verification_level = "DOCUMENTED"
        s.user_reported_confidence = 5
        s.reported_at = datetime.utcnow()

        # Post-process Timing Quality
        actual = datetime.strptime(s.actual_event_date, "%Y-%m-%d")
        peak = datetime.strptime(s.peak_date, "%Y-%m-%d")
        error = (actual - peak).days
        s.timing_error_days = error

        if abs(error) <= 7: s.timing_quality = "PEAK_HIT_7"
        elif abs(error) <= 15: s.timing_quality = "ACTIVE_WINDOW_HIT"
        else: s.timing_quality = "BROAD_MATCH"

        db.session.commit()
        print(f"Outcome Recorded for Snapshot {s_id}")
        print(f"Timing Error: {error} days ({s.timing_quality})")

    print("\n--- PHASE 3: BETA METRICS SUMMARY ---")
    from scripts.v315_beta_metrics import main as run_metrics
    run_metrics()

if __name__ == "__main__":
    run_realtime_session()
