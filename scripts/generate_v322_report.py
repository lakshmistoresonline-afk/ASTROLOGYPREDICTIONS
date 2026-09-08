import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.predictions.v317_timeline import lifetime_timeline_engine_v17
from app.astrology.predictions.accuracy_engine import accuracy_engine
from app.utils.pdf_generator import generate_complete_pdf

def generate():
    app = create_app()
    with app.app_context():
        chart_id = "de9427a1" # Subramanian T S
        chart = db.session.get(Chart, chart_id)
        if not chart:
            print("❌ User profile not found.")
            return

        print(f"🔄 Generating V3.22 Intelligence Audit for: {chart.name}...")

        # 1. Calculation
        birth_dt = datetime.strptime(f"{chart.dob} {chart.tob}", "%Y-%m-%d %H:%M")
        chart_obj = calculate_chart_data(birth_dt, chart.lat, chart.lon, chart.tz)

        # 2. Predictions & Timeline
        preds = generate_evidence_based_predictions(chart_obj)
        timeline = lifetime_timeline_engine_v17.generate_lifetime_timeline(chart_obj, chart_id)

        # 3. Packaging
        data = {
            "profile": {"name": chart.name, "dob": chart.dob, "tob": chart.tob, "place": chart.place, "lat": chart.lat, "lon": chart.lon, "tz": chart.tz},
            "present": {
                "as_of": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "top_signals": [p for p in preds['predictions'] if p['prediction_strength'] in ['PEAK', 'ACTIVE']][:3],
                "predictions": preds['predictions']
            },
            "lifecycle": {"events": [e.model_dump() for e in timeline.events]},
            "metadata": {"engine": "V3.22 Premium", "calculation": "CALC-SWE-2.10.3", "ayanamsa": "Lahiri"}
        }

        # 4. PDF
        pdf_bytes = generate_complete_pdf(data)
        filename = f"V322_Intelligence_Audit_{chart.name.replace(' ', '_')}.pdf"
        with open(filename, "wb") as f:
            f.write(pdf_bytes)
        print(f"✅ SUCCESS: {filename} generated in root.")

if __name__ == "__main__":
    generate()
