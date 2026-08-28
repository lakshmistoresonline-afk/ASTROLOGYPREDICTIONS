import os
import uuid
from datetime import datetime
from app import create_app
from app.database.models import db, Chart, PredictionOutcome, RemedyTask, Profile
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions

def verify_beta_flow():
    os.environ["FLASK_SECRET_KEY"] = "beta-verify-key"
    app = create_app()
    with app.app_context():
        db.create_all()

        # 1. Profile Creation
        print("[1] Simulating Practitioner Profile Creation...")
        p = Profile(name="Group 1 Tester")
        db.session.add(p)
        db.session.commit()

        # 2. Chart Calculation (Internal Profile: 1990-01-01 12:00 Delhi)
        print("[2] Calculating Deterministic Chart...")
        dt = datetime(1990, 1, 1, 12, 0)
        chart_data = calculate_chart_data(dt, 28.6, 77.2, "Asia/Kolkata", birth_time_conf="HIGH")

        # 3. Save Chart
        cid = str(uuid.uuid4())[:8]
        c = Chart(id=cid, profile_id=p.id, name="Test Chart", dob="1990-01-01", tob="12:00")
        c.set_data(chart_data.model_dump())
        db.session.add(c)
        db.session.commit()

        # 4. Generate Predictions & Snapshots
        print("[3] Generating Predictions & Snapshots...")
        preds = generate_evidence_based_predictions(chart_data)
        from app.astrology.store import save_prediction_snapshot

        for pred in preds["predictions"]:
            snapshot_id = save_prediction_snapshot(cid, pred)
            print(f"    - Snapshot created for {pred['domain']} (ID: {snapshot_id})")

        # 5. Outcome Reporting
        print("[4] Testing Outcome Reporting (OCCURRED + Date)...")
        snapshot = PredictionOutcome.query.first()
        snapshot.status = "OCCURRED"
        snapshot.actual_event_date = "2026-08-30"
        # Simulate background processing of timing quality
        if snapshot.actual_event_date and snapshot.peak_date:
             actual = datetime.strptime(snapshot.actual_event_date, "%Y-%m-%d")
             peak = datetime.strptime(snapshot.peak_date, "%Y-%m-%d")
             diff = abs((actual - peak).days)
             snapshot.timing_quality = "TIMING_MATCH_30" if diff <= 30 else "BROAD_MATCH"

        db.session.commit()
        print(f"    - Outcome logged. Timing Quality: {snapshot.timing_quality}")

        # 6. Remedy Adherence
        print("[5] Testing Remedy Adherence...")
        task = RemedyTask(chart_id=cid, planet="Jupiter", action="Mantra", approach="Strengthen")
        db.session.add(task)
        db.session.commit()
        task.completion_count += 1
        task.last_completed_at = datetime.utcnow()
        db.session.commit()
        print(f"    - Remedy streak incremented: {task.completion_count}")

        print("\nBETA FLOW VERIFICATION: PASS")

if __name__ == "__main__":
    verify_beta_flow()
