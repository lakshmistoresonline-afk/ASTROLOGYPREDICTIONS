import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart, TimelineEventSnapshot
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.predictions.v317_timeline import lifetime_timeline_engine_v17
from app.astrology.predictions.accuracy_engine import accuracy_engine
from app.utils.pdf_generator import generate_complete_pdf

def generate():
    app = create_app()
    with app.app_context():
        # 1. Load User Profile
        chart_id = "de9427a1" # Subramanian T S
        chart = Chart.query.get(chart_id)
        if not chart:
            print("❌ User profile not found in database.")
            return

        print(f"🔄 Processing Intelligence for: {chart.name}...")

        # 2. Reconstruct Canonical Chart
        c_data = chart.get_data()
        birth_dt = datetime.strptime(f"{chart.dob} {chart.tob}", "%Y-%m-%d %H:%M")
        chart_obj = calculate_chart_data(birth_dt, chart.lat, chart.lon, chart.tz)

        # 3. Generate Predictions (Present)
        print("   -> Generating Domain Predictions...")
        preds = generate_evidence_based_predictions(chart_obj)

        # 4. Generate Lifetime Timeline (Lifecycle)
        print("   -> Mapping Lifecycle Timeline...")
        # Note: Using coarser sampling for PDF speed as implemented in V3.20 performance fix
        timeline = lifetime_timeline_engine_v17.generate_lifetime_timeline(chart_obj, chart_id)
        phases = timeline.phases

        # 5. Load Historical Replay Data
        cases_path = os.path.join(app.root_path, '..', 'data', 'backtest', 'raw', 'historical_cases.json')
        demo_cases_results = []
        with open(cases_path, 'r') as f:
            all_cases = json.load(f)

        case = next((c for c in all_cases if c['name'] == 'Steve Jobs'), None)
        if case:
            event = case['events'][0]
            cutoff = datetime.strptime(event['date'], "%Y-%m-%d") - timedelta(days=30)
            c_replay = calculate_chart_data(datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M"), case['lat'], case['lon'], case['tz'])
            p_replay = generate_evidence_based_predictions(c_replay, selected_date=cutoff)
            demo_cases_results.append({
                "case_name": "Steve Jobs",
                "event": event['description'],
                "actual_date": event['date'],
                "cutoff_date": cutoff.strftime("%Y-%m-%d"),
                "prediction": next((p for p in p_replay['predictions'] if p['domain'] == event['domain']), None)
            })

        # 6. Accuracy Metrics
        print("   -> Compiling Calibration Metrics...")
        accuracy_data = {
            "real_world": accuracy_engine.get_cohort_metrics("REAL_WORLD"),
            "historical": accuracy_engine.get_cohort_metrics("HISTORICAL"),
            "calibration": accuracy_engine.get_calibration_data()
        }

        # 7. Package Data
        data = {
            "profile": {
                "name": chart.name,
                "dob": chart.dob,
                "tob": chart.tob,
                "place": chart.place,
                "lat": chart.lat,
                "lon": chart.lon,
                "tz": chart.tz
            },
            "present": {
                "as_of": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "top_signals": [p for p in preds['predictions'] if p['prediction_strength'] in ['PEAK', 'ACTIVE']][:3],
                "predictions": preds['predictions'],
                "timeline": preds.get('timeline', [])
            },
            "lifecycle": {
                "events": [e.model_dump() for e in timeline.events],
                "phases": phases
            },
            "past_validation": demo_cases_results,
            "accuracy": accuracy_data,
            "metadata": {
                "engine": "V3.20 Hardened",
                "calculation": "CALC-SWE-2.10.3",
                "ayanamsa": "Lahiri",
                "baseline_precision": "60.7%",
                "baseline_recall": "43.6%"
            }
        }

        # 8. Generate PDF
        print("   -> Rendering Consolidated PDF Report...")
        pdf_bytes = generate_complete_pdf(data)

        filename = f"Complete_Intelligence_Report_{chart.name.replace(' ', '_')}.pdf"
        output_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), filename)

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"✅ SUCCESS: Complete report generated at: {output_path}")

if __name__ == "__main__":
    generate()
