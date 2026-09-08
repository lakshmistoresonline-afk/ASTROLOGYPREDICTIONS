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
from app.astrology.store import save_prediction_snapshot

def test_hardening():
    os.environ["FLASK_SECRET_KEY"] = "hardening-test-key"
    app = create_app()

    # 1. SETUP DATA
    birth_dt = datetime(1986, 9, 28, 16, 30)
    lat, lon, tz = 10.78, 76.47, "Asia/Kolkata"

    print("\n[TEST] Verifying Pipeline Hardening...")
    with app.app_context():
        # Create test chart
        chart_id = "h-test-" + str(uuid.uuid4())[:4]
        chart_obj = calculate_chart_data(birth_dt, lat, lon, tz)

        # 2. GENERATE PREDICTION
        # Ensure we have some evidence and timing
        prediction = CareerPredictionEngine.get_prediction(chart_obj, datetime.now())

        # 3. SAVE SNAPSHOT (REAL_WORLD context)
        s_id = save_prediction_snapshot(chart_id, prediction.model_dump(),
                                         source_type="REAL_WORLD",
                                         participant_id="HARDENING_USER",
                                         session_id="SESS_HARD")

        # 4. VERIFY DATABASE RECORD
        snapshot = PredictionOutcome.query.get(s_id)

        print(f"--- Snapshot {s_id} Audit ---")
        print(f"Domain: {snapshot.domain}")
        print(f"Source Type: {snapshot.source_type}")
        print(f"Start Date: {snapshot.start_date}")
        print(f"Peak Date: {snapshot.peak_date}")
        print(f"End Date: {snapshot.end_date}")
        print(f"Timing Phase: {snapshot.timing_phase}")
        print(f"Proximity Weight: {snapshot.proximity_weight}")

        # Check Evidence Persistence
        if snapshot.evidence_snapshot:
            ev = json.loads(snapshot.evidence_snapshot)
            print(f"Evidence Persisted: YES ({len(ev)} items)")
        else:
            print(f"Evidence Persisted: NO (FAILED)")

        # 5. TEST IMMUTABILITY
        original_text = snapshot.prediction_text
        original_score = snapshot.confluence_score

        # Attempt outcome update
        from app.api.tracking import report_snapshot_outcome
        with app.test_request_context(json={"status": "OCCURRED", "event_date": datetime.now().strftime("%Y-%m-%d")}):
            report_snapshot_outcome(s_id)

        snapshot_after = PredictionOutcome.query.get(s_id)
        if snapshot_after.prediction_text == original_text and snapshot_after.confluence_score == original_score:
             print("Immutability Verified: YES")
        else:
             print("Immutability Verified: NO (FAILED - original fields changed)")

        # 6. TEST PROSPECTIVE ENFORCEMENT
        with app.test_request_context(json={"status": "OCCURRED", "event_date": "1980-01-01"}):
            resp = report_snapshot_outcome(s_id)
            if isinstance(resp, tuple): resp = resp[0] # handle tuple
            if resp.status_code == 400:
                print("Prospective Enforcement: YES (Rejected 1980 date)")
            else:
                print(f"Prospective Enforcement: NO (Accepted 1980 date) - Status {resp.status_code}")

        # Clean up
        db.session.delete(snapshot_after)
        db.session.commit()
        print("\nHardening Test Complete.")

if __name__ == "__main__":
    test_hardening()
