import os
import sys
import json
import sqlite3
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart, PredictionOutcome
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.predictions.engines.career import CareerPredictionEngine
from app.astrology.predictions.engines.finance import FinancePredictionEngine
from app.astrology.predictions.engines.marriage import MarriagePredictionEngine
from app.astrology.predictions.engines.health import HealthPredictionEngine
from app.astrology.predictions.engines.travel import TravelPredictionEngine
from app.astrology.predictions.engines.education import EducationPredictionEngine
from app.astrology.predictions.engines.fame import FamePredictionEngine
from app.astrology.predictions.engines.business import BusinessPredictionEngine
from app.astrology.remedies.engine import get_personalized_remedies

def audit():
    app = create_app()
    with app.app_context():
        # PHASE 1: Profile Validation
        print("PHASE 1: PROFILE VALIDATION")
        chart = Chart.query.filter(Chart.name.like("%Subramanian T S%")).first()
        if not chart:
            print("ERROR: Profile 'Subramanian T S' not found in database.")
            return

        print(f"1. Profile ID: {chart.id}")
        print(f"2. Profile name: {chart.name}")
        print(f"3. Date of birth: {chart.dob}")
        print(f"4. Exact birth time: {chart.tob}")
        print(f"5. Birth place: {chart.place}")
        print(f"6. Latitude: {chart.lat}")
        print(f"7. Longitude: {chart.lon}")
        print(f"8. Timezone: {chart.tz}")

        mandatory_fields = [chart.dob, chart.tob, chart.lat, chart.lon, chart.tz]
        valid = all(mandatory_fields)
        print(f"11. All mandatory birth details present: {'YES' if valid else 'NO'}")
        print(f"12. Valid for prediction generation: {'YES' if valid else 'NO'}")

        if not valid:
            print("Stopping audit due to missing mandatory data.")
            return

        # PHASE 2 & 3: Calculation & Natal Chart
        print("\nPHASE 2 & 3: CALCULATION & NATAL CHART")
        birth_dt = datetime.strptime(f"{chart.dob} {chart.tob}", "%Y-%m-%d %H:%M")
        try:
            chart_obj = calculate_chart_data(birth_dt, chart.lat, chart.lon, chart.tz)
            print("Calculation successful.")
            print(f"Ascendant: {chart_obj.ascendant:.2f} ({chart_obj.asc_rashi})")
            for p_name, p in chart_obj.planets.items():
                print(f"  {p_name:10}: {p.rashi} Rashi, {p.degree:.2f} deg, House {p.house}, Retro={p.is_retrograde}")
        except Exception as e:
            print(f"Calculation failed: {e}")
            return

        # PHASE 4: Divisional Charts
        print("\nPHASE 4: DIVISIONAL CHARTS")
        for varga in ["D1", "D9", "D10"]:
            if varga in chart_obj.divisional_charts:
                print(f"{varga} Chart:")
                # print(chart_obj.divisional_charts[varga])

        # PHASE 5: Vimshottari Dasha
        print("\nPHASE 5: VIMSHOTTARI DASHA")
        from app.astrology.dasha import calculate_vimshottari
        dasha = calculate_vimshottari(chart_obj.planets["Moon"].longitude, chart_obj.birth_datetime)
        print(f"Current Maha: {dasha.get('current_maha', {}).get('lord')}")
        print(f"Current Antar: {dasha.get('current_antar', {}).get('lord')}")

        # PHASE 10: Prediction Engine
        print("\nPHASE 10: PREDICTION ENGINE")
        engines = [
            CareerPredictionEngine, FinancePredictionEngine, MarriagePredictionEngine,
            HealthPredictionEngine, TravelPredictionEngine, EducationPredictionEngine,
            FamePredictionEngine, BusinessPredictionEngine
        ]

        all_preds = []
        for eng in engines:
            pred = eng.get_prediction(chart_obj, datetime.now())
            all_preds.append(pred)
            print(f"Domain: {pred.domain}")
            print(f"  Strength: {pred.prediction_strength}")
            print(f"  Score: {pred.score}")
            print(f"  Timing: {pred.timing_window.get('phase')}")

        # PHASE 13: Remedies
        print("\nPHASE 13: REMEDIES")
        remedies = get_personalized_remedies(chart_obj)
        for r in remedies[:3]:
            print(f"Remedy: {r.get('remedy')}")

        # PHASE 17: Snapshot Integrity
        print("\nPHASE 17: SNAPSHOT INTEGRITY")
        snapshot = PredictionOutcome.query.filter_by(chart_id=chart.id).order_by(PredictionOutcome.created_at.desc()).first()
        if snapshot:
            print(f"Prediction ID: {snapshot.id}")
            print(f"Engine version: {snapshot.engine_version}")
            print(f"Source type: {snapshot.source_type}")
        else:
            print("No snapshot found for this profile.")

if __name__ == "__main__":
    audit()
