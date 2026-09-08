import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart, PredictionOutcome
from app.astrology.core.chart import calculate_chart_data
from app.astrology.core.calc_client import calc_client
from app.astrology.dasha import calculate_vimshottari
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.remedies.engine import get_personalized_remedies
from app.astrology.predictions.engines.career import CareerPredictionEngine
from app.astrology.predictions.engines.finance import FinancePredictionEngine
from app.astrology.predictions.engines.marriage import MarriagePredictionEngine
from app.astrology.predictions.engines.health import HealthPredictionEngine
from app.astrology.predictions.engines.travel import TravelPredictionEngine
from app.astrology.predictions.engines.education import EducationPredictionEngine
from app.astrology.predictions.engines.fame import FamePredictionEngine
from app.astrology.predictions.engines.business import BusinessPredictionEngine

def run_audit():
    app = create_app()
    with app.app_context():
        # DATA
        cid = "baae1f5a"
        name = "Subramanian T S"
        dob = "1986-09-28"
        tob = "16:30"
        lat = 10.7873692
        lon = 76.4742172
        tz = "Asia/Kolkata"

        print(f"--- PHASE 1: PROFILE VALIDATION ---")
        print(f"ID: {cid}")
        print(f"Name: {name}")
        print(f"DOB: {dob}")
        print(f"TOB: {tob}")
        print(f"Coords: {lat}, {lon}")
        print(f"TZ: {tz}")

        print(f"\n--- PHASE 2: CALCULATION SERVICE ---")
        health = calc_client.check_health()
        print(f"Service Online: {health}")
        birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        chart = calculate_chart_data(birth_dt, lat, lon, tz)
        print("Calculation PASS.")

        print(f"\n--- PHASE 3: NATAL CHART ---")
        print(f"Ascendant: {chart.ascendant:.2f} ({chart.asc_rashi})")
        for p_name, p in chart.planets.items():
            print(f"{p_name:10}: {p.rashi} R, {p.degree:6.2f}D, H{p.house}, Retro={p.is_retrograde}")

        print(f"\n--- PHASE 4: DIVISIONAL CHARTS ---")
        for v in ["D1", "D9", "D10"]:
            print(f"{v}: {chart.divisional_charts.get(v)}")

        print(f"\n--- PHASE 5: VIMSHOTTARI DASHA ---")
        dasha = calculate_vimshottari(chart.planets["Moon"].longitude, chart.birth_datetime)
        print(f"Current Maha: {dasha.get('current_maha', {}).get('lord')}")
        print(f"Current Antar: {dasha.get('current_antar', {}).get('lord')}")
        print(f"Dates: {dasha.get('current_antar', {}).get('start')} to {dasha.get('current_antar', {}).get('end')}")

        print(f"\n--- PHASE 8: YOGA ANALYSIS ---")
        for y in chart.yogas:
            if y.get('present'):
                print(f"- {y.get('name')}: {y.get('strength')} ({y.get('interpretation')})")

        print(f"\n--- PHASE 10: PREDICTION ENGINE ---")
        engines = [
            CareerPredictionEngine, FinancePredictionEngine, MarriagePredictionEngine,
            HealthPredictionEngine, TravelPredictionEngine, EducationPredictionEngine,
            FamePredictionEngine, BusinessPredictionEngine
        ]
        for eng in engines:
            p = eng.get_prediction(chart, datetime.now())
            print(f"DOMAIN: {p.domain}")
            print(f"  STRENGTH: {p.prediction_strength}")
            print(f"  SCORE: {p.score}")
            print(f"  TIMING: {p.timing_window.get('phase')}")
            print(f"  WHY: {p.summary}")

        print(f"\n--- PHASE 13: REMEDIES ---")
        remedies = get_personalized_remedies(chart)
        for r in remedies[:3]:
            print(f"Remedy: {r.get('remedy')} for {r.get('planet')}")

if __name__ == "__main__":
    run_audit()
