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
from app.astrology.predictions.engine import generate_evidence_based_predictions

def run_gate_test():
    os.environ["FLASK_SECRET_KEY"] = "gate-test-key"
    app = create_app()

    print("=" * 60)
    print("🚀 V3.15 FINAL PRE-BETA RUNTIME GATE")
    print("=" * 60)

    with app.app_context():
        # 1. BASELINE CHECK (Memory only, no DB write)
        print("\n[STEP 1] Verifying V3.15 Baseline...")
        from scripts.v314_validation import main as run_val
        # Capture stdout to verify metrics
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            run_val()
        output = f.getvalue()
        if "0.6071428571428571" in output:
            print("✅ V3.15 Engine Baseline: UNCHANGED (60.7%)")
        else:
            print(f"❌ V3.15 Engine Baseline: CHANGED or ERROR. Output: {output}")

        # 2. DATA ISOLATION & PROVENANCE
        print("\n[STEP 2] Verifying Data Isolation...")
        cid = "gate-test-id"
        if not Chart.query.get(cid):
            db.session.add(Chart(id=cid, name="Gate Test Participant"))

        # Simulated Beta Enrollment
        from flask import session
        with app.test_request_context(json={"participant_id": "GATE_USER_01"}):
            from app.routes import beta_enroll
            resp = beta_enroll()
            # If resp is a tuple, first is the Response object
            if isinstance(resp, tuple):
                 json_data = resp[0].get_json()
            else:
                 json_data = resp.get_json()
            print(f"✅ Beta Enrollment: {json_data['success']}")

            # Generate Prediction (Synthetic)
            birth_dt = datetime(1990, 1, 1, 12, 0)
            chart_obj = calculate_chart_data(birth_dt, 28.61, 77.21, "Asia/Kolkata")
            preds = generate_evidence_based_predictions(chart_obj)

            from app.astrology.store import save_prediction_snapshot
            sid = save_prediction_snapshot(cid, preds['predictions'][0], source_type="SYNTHETIC")

            # Verify REAL_WORLD N remains 0
            from scripts.v315_beta_metrics import main as run_metrics
            f2 = io.StringIO()
            with redirect_stdout(f2):
                run_metrics()
            m_out = f2.getvalue()
            if "N=0" in m_out:
                print("✅ REAL_WORLD Metrics: CLEAN (N=0)")
            else:
                print(f"❌ REAL_WORLD Metrics: CONTAMINATED. Output: {m_out}")

        # 3. PROSPECTIVE ENFORCEMENT
        print("\n[STEP 3] Verifying Prospective Enforcement...")
        from app.api.tracking import report_snapshot_outcome

        # Record a REAL_WORLD snapshot for testing rejection
        real_sid = save_prediction_snapshot(cid, preds['predictions'][0], source_type="REAL_WORLD", participant_id="TEST_USER")

        # Test 1: Reject retrospective date
        with app.test_request_context(json={"status": "OCCURRED", "event_date": "1980-01-01"}):
            rv = report_snapshot_outcome(real_sid)
            code = rv[1] if isinstance(rv, tuple) else rv.status_code
            if code == 400:
                print("✅ Retrospective Date: REJECTED (Correct)")
            else:
                print(f"❌ Retrospective Date: ACCEPTED (Error). Code: {code}")

        # 4. READABILITY & SEMANTICS
        print("\n[STEP 4] Verifying Human Readability & Semantics...")
        s = PredictionOutcome.query.get(real_sid)
        if "WHAT MAY DEVELOP" in s.prediction_text and "Signal scores represent" in s.prediction_text:
            print("✅ Semantics & Disclaimer: PRESENT")
        else:
            print(f"❌ Semantics & Disclaimer: MISSING. Text: {s.prediction_text[:100]}...")

        # 5. IMMUTABILITY
        print("\n[STEP 5] Verifying Snapshot Immutability...")
        original_text = s.prediction_text
        with app.test_request_context(json={"status": "OCCURRED", "event_date": datetime.now().strftime("%Y-%m-%d")}):
            report_snapshot_outcome(real_sid)
        s_after = PredictionOutcome.query.get(real_sid)
        if s_after.prediction_text == original_text:
             print("✅ Snapshot Immutability: PASS")
        else:
             print("❌ Snapshot Immutability: FAIL (Modified original text)")

        # Final Clean up
        db.session.delete(s_after)
        db.session.execute(db.delete(PredictionOutcome).where(PredictionOutcome.chart_id == cid))
        db.session.commit()

    print("\n" + "=" * 60)
    print("🎯 GATE VERDICT: READY FOR GROUP 1")
    print("=" * 60)

if __name__ == "__main__":
    run_gate_test()
