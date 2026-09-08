import os
import sys
import json
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, PredictionOutcome, Chart

def test_snapshot_integrity():
    app = create_app()
    with app.app_context():
        # Create a test chart if needed
        chart = Chart.query.first()
        if not chart:
             print("FAIL: No chart found for test.")
             return

        # 1. Create Snapshot
        snapshot = PredictionOutcome(
            chart_id=chart.id,
            domain="Career & Authority",
            prediction_text="Original Text",
            engine_version="V3.15",
            status="PENDING"
        )
        db.session.add(snapshot)
        db.session.commit()
        s_id = snapshot.id
        print(f"SUCCESS: Snapshot {s_id} created.")

        # 2. Attempt to Update (Simulate Outcome)
        s = PredictionOutcome.query.get(s_id)
        s.status = "OCCURRED"
        s.actual_event_date = "2026-09-03"
        db.session.commit()
        print(f"SUCCESS: Outcome recorded.")

        # 3. Verify Prediction Text hasn't changed
        s_verify = PredictionOutcome.query.get(s_id)
        if s_verify.prediction_text == "Original Text" and s_verify.status == "OCCURRED":
             print("SUCCESS: Integrity Check Passed (Original fields preserved).")
        else:
             print("FAIL: Integrity Check Failed.")

        # Clean up
        db.session.delete(s_verify)
        db.session.commit()

if __name__ == "__main__":
    test_snapshot_integrity()
