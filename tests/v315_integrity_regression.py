import os
import sys
import json
import uuid
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, PredictionOutcome, Chart

def test_metrics_isolation():
    app = create_app()
    with app.app_context():
        # Clean isolation test
        cid = "test-iso"
        if not Chart.query.get(cid):
            db.session.add(Chart(id=cid, name="Test Chart"))
            db.session.commit()

        p1 = PredictionOutcome(chart_id=cid, domain="Career", prediction_strength="ACTIVE", status="OCCURRED", source_type="HISTORICAL", engine_version="V3.15", prediction_text="Hist")
        p2 = PredictionOutcome(chart_id=cid, domain="Career", prediction_strength="ACTIVE", status="OCCURRED", source_type="SYNTHETIC", engine_version="V3.15", prediction_text="Synth")
        p3 = PredictionOutcome(chart_id=cid, domain="Career", prediction_strength="ACTIVE", status="OCCURRED", source_type="REAL_WORLD", engine_version="V3.15", prediction_text="Real")

        db.session.add_all([p1, p2, p3])
        db.session.commit()

        # Run Beta Metrics query
        beta_outcomes = PredictionOutcome.query.filter(
            PredictionOutcome.engine_version == "V3.15",
            PredictionOutcome.source_type == "REAL_WORLD",
            PredictionOutcome.status != "PENDING"
        ).all()

        print("\n[TEST: Metrics Isolation]")
        if len(beta_outcomes) == 1 and beta_outcomes[0].prediction_text == "Real":
             print("✅ PASS: Beta metrics strictly filtered by source_type.")
        else:
             print(f"❌ FAIL: Beta metrics contaminated. Count={len(beta_outcomes)}")

        # Clean up
        db.session.delete(p1); db.session.delete(p2); db.session.delete(p3)
        db.session.commit()

def test_prospective_enforcement():
    app = create_app()
    with app.app_context():
        print("\n[TEST: Prospective Enforcement]")
        # 1. Create a REAL_WORLD snapshot
        snapshot = PredictionOutcome(
            chart_id="test-iso",
            domain="Career",
            source_type="REAL_WORLD",
            engine_version="V3.15",
            status="PENDING",
            prediction_text="Prospective Test"
        )
        db.session.add(snapshot)
        db.session.commit()
        s_id = snapshot.id

        # 2. Attempt retrospective outcome via API simulation
        from app.api.tracking import report_snapshot_outcome
        with app.test_request_context(json={"status": "OCCURRED", "event_date": "1980-12-12"}):
            rv = report_snapshot_outcome(s_id)
            # Handle tuple (Response, status_code) or Response object
            if isinstance(rv, tuple):
                resp, code = rv
            else:
                resp, code = rv, rv.status_code

            if code == 400 and b"RETROSPECTIVE_OUTCOME_PROHIBITED" in resp.data:
                print("✅ PASS: Retrospective date rejected for REAL_WORLD.")
            else:
                print(f"❌ FAIL: Retrospective date accepted. Code={code} Data={resp.data}")

        # 3. Verify HISTORICAL still allows retrospective
        snapshot.source_type = "HISTORICAL"
        db.session.commit()
        with app.test_request_context(json={"status": "OCCURRED", "event_date": "1980-12-12"}):
            rv = report_snapshot_outcome(s_id)
            if isinstance(rv, tuple):
                resp, code = rv
            else:
                resp, code = rv, rv.status_code

            if code == 200:
                print("✅ PASS: Retrospective date allowed for HISTORICAL.")
            else:
                print(f"❌ FAIL: Retrospective date blocked for HISTORICAL. Code={code}")

        # Clean up
        db.session.delete(snapshot)
        db.session.commit()

if __name__ == "__main__":
    test_metrics_isolation()
    test_prospective_enforcement()
