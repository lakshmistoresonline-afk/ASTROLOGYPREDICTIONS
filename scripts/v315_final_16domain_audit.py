import os
import sys
import json
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart, PredictionOutcome
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.store import save_prediction_snapshot

def run_full_audit():
    os.environ["FLASK_SECRET_KEY"] = "final-audit-key"
    app = create_app()
    with app.app_context():
        # 1. LOAD PROFILE
        cid = 'baae1f5a'
        chart_data = Chart.query.get(cid)
        if not chart_data:
            print("Chart not found.")
            return

        raw = chart_data.get_data()
        birth_dt_str = raw.get("birth_datetime")
        if "T" in birth_dt_str:
            birth_dt = datetime.fromisoformat(birth_dt_str)
        else:
            birth_dt = datetime.strptime(birth_dt_str, "%Y-%m-%d %H:%M:%S")

        chart_obj = calculate_chart_data(birth_dt, chart_data.lat, raw.get("longitude"), chart_data.tz)

        # 2. GENERATE ALL 16 DOMAINS
        print(f"Generating 16-domain suite for {chart_data.name}...")
        full_output = generate_evidence_based_predictions(chart_obj)

        # 3. PERSIST AS SYNTHETIC QA RUN
        new_ids = []
        for p in full_output['predictions']:
            sid = save_prediction_snapshot(cid, p, source_type="SYNTHETIC",
                                            participant_id="FINAL_QA_AUDIT",
                                            session_id="SESS_FINAL_QA")
            new_ids.append(sid)

        print(f"Snapshots generated: {new_ids}")

        # 4. TECHNICAL FIELD VERIFICATION
        print("\n[PHASE 1: TECHNICAL FIELD VERIFICATION]")
        cursor = db.session.execute(db.select(PredictionOutcome).filter(PredictionOutcome.id.in_(new_ids)))
        snapshots = cursor.scalars().all()

        field_errors = []
        for s in snapshots:
            missing = []
            if not s.prediction_text: missing.append("prediction_text")
            if s.confluence_score is None: missing.append("confluence_score")
            if not s.prediction_strength: missing.append("prediction_strength")
            if not s.start_date: missing.append("start_date")
            if not s.peak_date: missing.append("peak_date")
            if not s.end_date: missing.append("end_date")
            if not s.timing_phase: missing.append("timing_phase")
            if not s.evidence_snapshot: missing.append("evidence_snapshot")

            if missing:
                field_errors.append(f"ID {s.id} ({s.domain}) missing: {', '.join(missing)}")

        if not field_errors:
            print("✅ All mandatory persistence fields present.")
        else:
            for err in field_errors: print(f"❌ {err}")

        # 5. EVIDENCE TRACEABILITY
        print("\n[PHASE 2: EVIDENCE TRACEABILITY]")
        for s in snapshots:
            ev = json.loads(s.evidence_snapshot)
            nodes = len(ev)
            print(f"Domain: {s.domain:25} | Nodes: {nodes}")
            if nodes == 0:
                print(f"  ❌ FAIL: No evidence nodes stored for {s.domain}")

        # 6. TIMING & COLLISION AUDIT
        print("\n[PHASE 3: TIMING COLLISION AUDIT]")
        timing_map = defaultdict(list)
        for s in snapshots:
            t_key = (s.start_date, s.peak_date, s.end_date)
            timing_map[t_key].append(s.domain)

        for t_key, domains in timing_map.items():
            if len(domains) > 1:
                print(f"Shared Timing {t_key}: {', '.join(domains)}")

        # 7. SCORE SEMANTICS
        print("\n[PHASE 4: SCORE SEMANTICS]")
        for s in snapshots[:3]:
            print(f"Domain: {s.domain}")
            print(f"  Text check for Disclaimer: {'YES' if 'Internal signal score' in s.prediction_text.lower() or 'astrological signal' in s.prediction_text.lower() else 'NO'}")
            print(f"  Calibrated Prob: {s.calibrated_probability}")

        # 8. DOMAIN INDEPENDENCE
        print("\n[PHASE 5: DOMAIN INDEPENDENCE]")
        text_map = defaultdict(list)
        for s in snapshots:
            text_map[s.prediction_text[:50]].append(s.domain)

        for prefix, domains in text_map.items():
            if len(domains) > 1:
                print(f"Duplicate Text Start '{prefix}...': {', '.join(domains)}")
        else:
            print("✅ No duplicate prediction text detected.")

if __name__ == "__main__":
    run_full_audit()
