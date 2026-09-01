import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

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

def main():
    os.environ["FLASK_SECRET_KEY"] = "audit-key-v312"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    # 1. Pre-calculate charts
    print("Pre-calculating charts...")
    case_charts = []
    with app.app_context():
        for i, case in enumerate(cases):
            print(f"Calculating chart {i+1}/{len(cases)}: {case['name']}")
            birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])
            case_charts.append((case, chart))

    ablation_scenarios = [
        {"label": "BASELINE", "overrides": {}},
        {"label": "NO_FOUNDATION", "overrides": {"DASHA_FOUNDATION": 0.0}},
        {"label": "NO_SECONDARY", "overrides": {"SECONDARY_PROMISE": 0.0}},
        {"label": "MINIMAL", "overrides": {"DASHA_FOUNDATION": 0.0, "SECONDARY_PROMISE": 0.0}},
    ]

    all_res = []
    original_weights = CorroborationEngine.WEIGHTS.copy()

    with app.app_context():
        for scenario in ablation_scenarios:
            label = scenario['label']
            overrides = scenario['overrides']
            print(f"Running scenario: {label}")

            # Apply overrides
            for key, val in overrides.items():
                CorroborationEngine.WEIGHTS[key] = val

            results = []
            for i, (case, chart) in enumerate(case_charts):
                print(f"  [{label}] Case {i+1}/{len(case_charts)}: {case['name']}")
                for event in case['events']:
                    event_date = datetime.strptime(event['date'], "%Y-%m-%d")
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

            all_res.append({
                "label": label,
                "precision": precision,
                "recall": recall,
                "specificity": specificity,
                "peak_n": len(peak_cases),
                "peak_precision": p_prec
            })

            # Reset weights
            for key in overrides:
                CorroborationEngine.WEIGHTS[key] = original_weights[key]

    # Generate Report
    report = "# Ablation Study: Jyotish OS Engine (V3.11 Baseline)\n\n"
    report += "| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec |\n"
    report += "| :--- | :---: | :---: | :---: | :---: | :---: |\n"

    for res in all_res:
        report += f"| {res['label']} | {res['precision']:.1%} | {res['recall']:.1%} | {res['specificity']:.1%} | {res['peak_n']} | {res['peak_precision']:.1%} |\n"

    report += "\n## Analysis\n"
    baseline = all_res[0]
    no_foundation = all_res[1]
    no_secondary = all_res[2]

    f_drop = baseline['specificity'] - no_foundation['specificity']
    s_drop = baseline['specificity'] - no_secondary['specificity']

    if f_drop > s_drop:
        report += f"**DASHA_FOUNDATION** contributes most to specificity regression (Drop: {f_drop:.1%}).\n"
    elif s_drop > f_drop:
        report += f"**SECONDARY_PROMISE** contributes most to specificity regression (Drop: {s_drop:.1%}).\n"
    else:
        report += "Both features contribute equally to specificity regression.\n"

    print(report)
    with open("ABLATION_STUDY_RESULTS.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()
