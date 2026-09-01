
import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Enforce project root and environment
PROJECT_ROOT = os.getcwd()
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'calculation_service'))

# Set Ephemeris Path
os.environ["SE_EPHE_PATH"] = os.path.join(PROJECT_ROOT, "ephe")

# Mock the calc_client
from calculation_service.app.core.engine import calculate_natal_chart, calculate_transits_for_range
from app.astrology.core.calc_client import calc_client

calc_client.get_natal_chart = calculate_natal_chart
calc_client.get_transit_range = calculate_transits_for_range

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.framework import CorroborationEngine

# Domain Map
from app.astrology.predictions.engines.career import CareerPredictionEngine
from app.astrology.predictions.engines.finance import FinancePredictionEngine
from app.astrology.predictions.engines.marriage import MarriagePredictionEngine
from app.astrology.predictions.engines.health import HealthPredictionEngine
from app.astrology.predictions.engines.travel import TravelPredictionEngine
from app.astrology.predictions.engines.education import EducationPredictionEngine
from app.astrology.predictions.engines.personality import PersonalityPredictionEngine
from app.astrology.predictions.engines.property import PropertyPredictionEngine
from app.astrology.predictions.engines.business import BusinessPredictionEngine
from app.astrology.predictions.engines.children import ChildrenPredictionEngine
from app.astrology.predictions.engines.spirituality import SpiritualityPredictionEngine
from app.astrology.predictions.engines.foreign import ForeignSettlementEngine
from app.astrology.predictions.engines.family import FamilyPredictionEngine
from app.astrology.predictions.engines.vehicles import VehiclesPredictionEngine
from app.astrology.predictions.engines.legal import LegalPredictionEngine
from app.astrology.predictions.engines.fame import FamePredictionEngine

DOMAIN_MAP = {
    "Career": CareerPredictionEngine.get_prediction,
    "Finance": FinancePredictionEngine.get_prediction,
    "Marriage": MarriagePredictionEngine.get_prediction,
    "Health": HealthPredictionEngine.get_prediction,
    "Travel": TravelPredictionEngine.get_prediction,
    "Education": EducationPredictionEngine.get_prediction,
    "Personality": PersonalityPredictionEngine.get_prediction,
    "Property": PropertyPredictionEngine.get_prediction,
    "Business": BusinessPredictionEngine.get_prediction,
    "Children": ChildrenPredictionEngine.get_prediction,
    "Spirituality": SpiritualityPredictionEngine.get_prediction,
    "Foreign Settlement": ForeignSettlementEngine.get_prediction,
    "Family": FamilyPredictionEngine.get_prediction,
    "Vehicles": VehiclesPredictionEngine.get_prediction,
    "Legal": LegalPredictionEngine.get_prediction,
    "Fame": FamePredictionEngine.get_prediction
}

def run_scenario(app, cases, label, overrides):
    # Apply overrides
    orig = CorroborationEngine.WEIGHTS.copy()
    for k, v in overrides.items():
        CorroborationEngine.WEIGHTS[k] = v

    results = []
    with app.app_context():
        for case in cases:
            birth_dt = datetime.strptime(case["dob"] + " " + case["tob"], "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case["lat"], case["lon"], case["tz"])
            for event in case["events"]:
                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in event["domain"].lower():
                        engine_func = v
                        break
                if not engine_func: continue
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                sim_date = event_date - timedelta(days=30)
                pred = engine_func(chart, sim_date)
                results.append({"strength": pred.prediction_strength, "status": event["status"]})

    # Restore
    CorroborationEngine.WEIGHTS = orig

    # Metrics
    tp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
    fp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])
    tn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])
    fn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    peak_cases = [r for r in results if r['strength'] == "PEAK"]
    p_tp = len([r for r in peak_cases if r['status'] == "OCCURRED"])
    p_prec = p_tp / len(peak_cases) if len(peak_cases) > 0 else 0

    # Enrichment
    active_peak_group = [r for r in results if r['strength'] in ["ACTIVE", "PEAK"]]
    background_group = [r for r in results if r['strength'] == "BACKGROUND"]
    active_rate = len([r for r in active_peak_group if r['status'] == "OCCURRED"]) / len(active_peak_group) if len(active_peak_group) > 0 else 0
    bg_rate = len([r for r in background_group if r['status'] == "OCCURRED"]) / len(background_group) if len(background_group) > 0 else 0
    enrichment = active_rate / bg_rate if bg_rate > 0 else 0

    return {
        "label": label, "precision": precision, "recall": recall, "specificity": specificity,
        "peak_n": len(peak_cases), "peak_precision": p_prec, "enrichment": enrichment
    }

def main():
    app = create_app()
    with open('data/backtest/raw/historical_cases.json', 'r') as f:
        cases = json.load(f)

    scenarios = [
        {"label": "BASE", "overrides": {}},
        {"label": "NO_FOUNDATION", "overrides": {"DASHA_FOUNDATION": 0.0}},
        {"label": "NO_SECONDARY", "overrides": {"SECONDARY_PROMISE": 0.0}},
        {"label": "MINIMAL", "overrides": {"DASHA_FOUNDATION": 0.0, "SECONDARY_PROMISE": 0.0}},
    ]

    print("| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec | Enrichment |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")
    for s in scenarios:
        res = run_scenario(app, cases, s['label'], s['overrides'])
        print(f"| {res['label']} | {res['precision']:.1%} | {res['recall']:.1%} | {res['specificity']:.1%} | {res['peak_n']} | {res['peak_precision']:.1%} | {res['enrichment']:.2f}x |")

if __name__ == "__main__":
    main()
