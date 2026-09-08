import os
import sys
import json
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart, PredictionOutcome
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.store import save_prediction_snapshot

def rerun():
    os.environ["FLASK_SECRET_KEY"] = "rerun-key"
    app = create_app()
    with app.app_context():
        # Load profile
        cid = 'baae1f5a'
        chart_data = Chart.query.get(cid)
        if not chart_data:
            print("Chart not found.")
            return

        raw = chart_data.get_data()
        birth_dt_str = raw.get("birth_datetime")
        # Handle ISO or space format
        if "T" in birth_dt_str:
            birth_dt = datetime.fromisoformat(birth_dt_str)
        else:
            birth_dt = datetime.strptime(birth_dt_str, "%Y-%m-%d %H:%M:%S")

        chart_obj = calculate_chart_data(birth_dt, chart_data.lat, raw.get("longitude"), chart_data.tz)

        # 1. GENERATE PREDICTIONS
        print("Generating new predictions...")
        preds_output = generate_evidence_based_predictions(chart_obj)

        # 2. SAVE NEW SNAPSHOTS (Marked as SYNTHETIC to avoid contamination)
        print("Saving hardened snapshots...")
        new_ids = []
        for p in preds_output['predictions']:
            sid = save_prediction_snapshot(cid, p, source_type="SYNTHETIC",
                                            participant_id="RERUN_AUDIT",
                                            session_id="SESS_RERUN")
            new_ids.append(sid)

        print(f"Rerun complete. New Snapshot IDs: {new_ids}")

        # 3. VERIFY ONE SNAPSHOT
        s = PredictionOutcome.query.get(new_ids[0])
        print(f"\nVerification of hardened Snapshot {s.id}:")
        print(f"Domain: {s.domain}")
        print(f"End Date: {s.end_date}")
        print(f"Timing Phase: {s.timing_phase}")
        print(f"Evidence Snapshot (len): {len(s.evidence_snapshot) if s.evidence_snapshot else 'NULL'}")
        print(f"What To Do (len): {len(s.what_to_do) if s.what_to_do else 'NULL'}")
        print(f"Remedy Text (len): {len(s.remedy_text) if s.remedy_text else 'NULL'}")

if __name__ == "__main__":
    rerun()
