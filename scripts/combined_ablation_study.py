import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
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
from app.astrology.predictions.framework import CorroborationEngine

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

def run_audit_extended(app, cases, charts, label, config_overrides=None):
    # Apply temporary weight overrides if any
    original_weights = CorroborationEngine.WEIGHTS.copy()
    if config_overrides:
        for key, val in config_overrides.items():
            if key in CorroborationEngine.WEIGHTS:
                CorroborationEngine.WEIGHTS[key] = val

    results = []
    with app.app_context():
        for case in cases:
            case_key = f"{case['name']}_{case['dob']}_{case['tob']}"
            chart = charts[case_key]

            for event in case['events']:
                event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                # Simulate 30 days before event
                sim_date = event_date - timedelta(days=30)

                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in event['domain'].lower():
                        engine_func = v
                        break

                if not engine_func: continue
                pred = engine_func(chart, sim_date)

                results.append({
                    "strength": pred.prediction_strength,
                    "status": event['status']
                })

    # Restore weights
    CorroborationEngine.WEIGHTS = original_weights

    # Calculate Metrics
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

    # Event Enrichment Ratio
    active_peak_group = [r for r in results if r['strength'] in ["ACTIVE", "PEAK"]]
    background_group = [r for r in results if r['strength'] == "BACKGROUND"]

    active_rate = len([r for r in active_peak_group if r['status'] == "OCCURRED"]) / len(active_peak_group) if len(active_peak_group) > 0 else 0
    bg_rate = len([r for r in background_group if r['status'] == "OCCURRED"]) / len(background_group) if len(background_group) > 0 else 0
    enrichment = active_rate / bg_rate if bg_rate > 0 else 0

    return {
        "label": label,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "peak_n": len(peak_cases),
        "peak_precision": p_prec,
        "enrichment": enrichment
    }

def main():
    os.environ["FLASK_SECRET_KEY"] = "audit-key-v311"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    print("Caching charts for 39 profiles...")
    charts = {}
    with app.app_context():
        for i, case in enumerate(cases):
            print(f"  [{i+1}/39] Caching {case['name']}...", end='\r')
            case_key = f"{case['name']}_{case['dob']}_{case['tob']}"
            birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
            charts[case_key] = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])
    print("\nCharts cached.")

    scenarios = [
        {"label": "BASE", "overrides": {}},
        {"label": "NO_FOUNDATION", "overrides": {"DASHA_FOUNDATION": 0.0}},
        {"label": "NO_SECONDARY", "overrides": {"SECONDARY_PROMISE": 0.0}},
        {"label": "MINIMAL", "overrides": {"DASHA_FOUNDATION": 0.0, "SECONDARY_PROMISE": 0.0}},
    ]

    print("\n| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec | Enrichment |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    all_results = []
    for s in scenarios:
        res = run_audit_extended(app, cases, charts, s['label'], s['overrides'])
        print(f"| {res['label']} | {res['precision']:.1%} | {res['recall']:.1%} | {res['specificity']:.1%} | {res['peak_n']} | {res['peak_precision']:.1%} | {res['enrichment']:.2f}x |")
        all_results.append(res)

    base_spec = all_results[0]['specificity']
    no_foundation_spec = all_results[1]['specificity']
    no_secondary_spec = all_results[2]['specificity']

    foundation_gain = no_foundation_spec - base_spec
    secondary_gain = no_secondary_spec - base_spec

    print(f"\nAnalysis:")
    if foundation_gain > secondary_gain:
        print(f"DASHA_FOUNDATION is the primary driver of specificity regression (Gain when removed: {foundation_gain:.1%}).")
    elif secondary_gain > foundation_gain:
        print(f"SECONDARY_PROMISE is the primary driver of specificity regression (Gain when removed: {secondary_gain:.1%}).")
    else:
        print("Both features contribute significantly to the specificity regression.")

if __name__ == "__main__":
    main()
