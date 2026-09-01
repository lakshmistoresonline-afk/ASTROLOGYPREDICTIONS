
import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.framework import CorroborationEngine, DomainPrediction

# V3.11 Configuration for Ablation Study
V311_WEIGHTS = {
    "NATAL_PROMISE": 0.35,
    "SECONDARY_PROMISE": 0.15,
    "DASHA_ACTIVATION": 0.20,
    "DASHA_FOUNDATION": 0.15,
    "TRANSIT_TRIGGER": 0.20,
    "DIVISIONAL_CONFIRM": 0.10,
    "YOGA_SUPPORT": 0.05,
    "ASPECT_SUPPORT": 0.05,
    "PLANETARY_STRENGTH": 0.05,
    "CONFLICTS": -0.40
}

def v311_synthesize(domain, promise_level, evidence, summary_template, timing_window=None):
    # Simplified V3.11 logic
    total_potential = 0
    total_friction = 0
    sources = {e.source for e in evidence if e.strength_score > 0}

    for e in evidence:
        if e.strength_score > 0:
            total_potential += e.strength_score
        else:
            total_friction = min(total_friction, e.strength_score)

    composite_score = max(0, min(1, total_potential + total_friction))

    tw = timing_window or {"phase": "SCANNING"}
    phase = tw.get("phase")
    is_peak = phase == "PEAK_MANIFESTATION"
    is_active = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

    # V3.11 Gates
    if composite_score >= 0.60 and is_peak:
        strength = "PEAK"
    elif composite_score >= 0.45 and is_active:
        strength = "ACTIVE"
    elif composite_score >= 0.30:
        strength = "WATCH"
    else:
        strength = "BACKGROUND"

    return DomainPrediction(
        domain=domain,
        headline=f"{strength}: {domain}",
        score=round(composite_score * 100, 2),
        quality_score=0.0,
        confidence="V3.11",
        prediction_strength=strength,
        validation_status="UNDER REVIEW",
        summary="",
        evidence_chain=evidence,
        supporting_factors=[],
        contradicting_factors=[],
        timing_window=tw,
        practical_actions=[]
    )

# Patch the engine
CorroborationEngine.synthesize = staticmethod(v311_synthesize)

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

def calculate_metrics(results):
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

    active_peak_group = [r for r in results if r['strength'] in ["ACTIVE", "PEAK"]]
    background_group = [r for r in results if r['strength'] == "BACKGROUND"]

    active_rate = len([r for r in active_peak_group if r['status'] == "OCCURRED"]) / len(active_peak_group) if len(active_peak_group) > 0 else 0
    bg_rate = len([r for r in background_group if r['status'] == "OCCURRED"]) / len(background_group) if len(background_group) > 0 else 0
    enrichment = active_rate / bg_rate if bg_rate > 0 else 0

    return {
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "peak_n": len(peak_cases),
        "peak_precision": p_prec,
        "enrichment": enrichment
    }

def main():
    app = create_app()
    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    # Use cache if available
    cache_file = "data/backtest/raw/chart_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            from app.astrology.core.models import CanonicalChart
            chart_cache = {k: CanonicalChart(**v) for k, v in json.load(f).items()}
    else:
        chart_cache = {}

    scenarios = [
        {"label": "BASE", "overrides": {}},
        {"label": "NO_FOUNDATION", "overrides": {"DASHA_FOUNDATION": 0.0}},
        {"label": "NO_SECONDARY", "overrides": {"SECONDARY_PROMISE": 0.0}},
        {"label": "MINIMAL", "overrides": {"DASHA_FOUNDATION": 0.0, "SECONDARY_PROMISE": 0.0}},
    ]

    print("| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec | Enrichment |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    all_res = []
    with app.app_context():
        for s in scenarios:
            # Apply weights
            current_weights = V311_WEIGHTS.copy()
            current_weights.update(s['overrides'])
            CorroborationEngine.WEIGHTS = current_weights

            results = []
            for case in cases:
                case_key = f"{case['name']}_{case['dob']}_{case['tob']}"
                chart = chart_cache.get(case_key)
                if not chart:
                     birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
                     chart = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])

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
                    results.append({"strength": pred.prediction_strength, "status": event['status']})

            metrics = calculate_metrics(results)
            print(f"| {s['label']} | {metrics['precision']:.1%} | {metrics['recall']:.1%} | {metrics['specificity']:.1%} | {metrics['peak_n']} | {metrics['peak_precision']:.1%} | {metrics['enrichment']:.2f}x |")
            metrics['label'] = s['label']
            all_res.append(metrics)

    base_spec = all_res[0]['specificity']
    no_foundation_spec = all_res[1]['specificity']
    no_secondary_spec = all_res[2]['specificity']

    f_gain = no_foundation_spec - base_spec
    s_gain = no_secondary_spec - base_spec

    print(f"\nAnalysis:")
    if f_gain > s_gain:
        print(f"DASHA_FOUNDATION is the primary driver of specificity regression (Gain when removed: {f_gain:.1%}).")
    else:
        print(f"SECONDARY_PROMISE is the primary driver of specificity regression (Gain when removed: {s_gain:.1%}).")

if __name__ == "__main__":
    main()
