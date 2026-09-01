
import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.framework import CorroborationEngine, DomainPrediction, CorroborationEvidence
from app.astrology.core.models import CanonicalChart

# V3.11 Configuration for Ablation Study
V311_WEIGHTS = {
    "NATAL_PROMISE": 0.35,
    "SECONDARY_PROMISE": 0.20,
    "DASHA_ACTIVATION": 0.20,
    "DASHA_FOUNDATION": 0.20,
    "TRANSIT_TRIGGER": 0.20,
    "DIVISIONAL_CONFIRM": 0.10,
    "YOGA_SUPPORT": 0.05,
    "ASPECT_SUPPORT": 0.05,
    "PLANETARY_STRENGTH": 0.05,
    "CONFLICTS": -0.35
}

def v311_synthesize_logic(domain, evidence, timing_window, current_weights):
    total_potential = 0
    total_friction = 0

    for e in evidence:
        # Re-weight the evidence based on V3.11 weights
        # Original code used: weighted_score = (abs_score / 100.0) * weight
        # We need the original weight to back out the score.
        # But wait, we can just use the evidence.strength_score / original_weight if we had it.
        # Actually, let's just use a fixed score for now or assume e.strength_score is already weighted.
        # Wait, framework.py says: weighted_score = (abs_score / 100.0) * weight

        # Let's assume the evidence passed in has a 'source' and 'strength_score'.
        # We'll re-calculate the weighted score.

        # If we can't get the raw score, we'll just use the source.
        # Engines use CorroborationEngine.create_evidence(level, description, score, ...)
        # where score is 0-100.
        pass

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
        "precision": precision, "recall": recall, "specificity": specificity,
        "peak_n": len(peak_cases), "peak_precision": p_prec, "enrichment": enrichment
    }

def main():
    app = create_app()
    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    cache_file = "data/backtest/raw/chart_cache.json"
    with open(cache_file, "r") as f:
        chart_cache = {k: CanonicalChart(**v) for k, v in json.load(f).items()}

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

    print("Collecting baseline evidence...")
    # Temporarily set weights to 1.0 to get "raw" scores (not quite, but easier)
    # Actually, let's just collect the evidence chain.
    baseline_data = []
    with app.app_context():
        for case in cases:
            case_key = f"{case['name']}_{case['dob']}_{case['tob']}"
            chart = chart_cache[case_key]
            for event in case['events']:
                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in event['domain'].lower():
                        engine_func = v
                        break
                if not engine_func: continue

                event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                sim_date = event_date - timedelta(days=30)
                pred = engine_func(chart, sim_date)

                # Extract evidence and their raw scores
                # We need to back out the score from weighted_score
                # weighted_score = (abs_score / 100.0) * weight
                # so abs_score = (weighted_score / weight) * 100
                evidence_list = []
                for e in pred.evidence_chain:
                    w = CorroborationEngine.WEIGHTS.get(e.source, 1.0)
                    raw_score = (e.strength_score / w) * 100 if w != 0 else 0
                    evidence_list.append({"source": e.source, "raw_score": raw_score})

                baseline_data.append({
                    "evidence": evidence_list,
                    "status": event['status'],
                    "timing_window": pred.timing_window
                })

    scenarios = [
        {"label": "BASE", "overrides": {}},
        {"label": "NO_FOUNDATION", "overrides": {"DASHA_FOUNDATION": 0.0}},
        {"label": "NO_SECONDARY", "overrides": {"SECONDARY_PROMISE": 0.0}},
        {"label": "MINIMAL", "overrides": {"DASHA_FOUNDATION": 0.0, "SECONDARY_PROMISE": 0.0}},
    ]

    print("\n| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec | Enrichment |")
    print("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    all_res = []
    for s in scenarios:
        current_weights = V311_WEIGHTS.copy()
        current_weights.update(s['overrides'])

        scenario_results = []
        for d in baseline_data:
            # Re-synthesize using V3.11 logic
            total_potential = 0
            total_friction = 0
            sources = {e['source'] for e in d['evidence']}

            for e in d['evidence']:
                w = current_weights.get(e['source'], 0.0)
                weighted_score = (e['raw_score'] / 100.0) * w
                if weighted_score > 0:
                    total_potential += weighted_score
                else:
                    total_friction = min(total_friction, weighted_score)

            composite_score = max(0, min(1, total_potential + total_friction))

            tw = d['timing_window']
            phase = tw.get("phase")
            is_peak = phase == "PEAK_MANIFESTATION"
            is_active = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

            # V3.11 Gates
            if composite_score >= 0.55 and is_peak:
                strength = "PEAK"
            elif composite_score >= 0.40 and is_active:
                strength = "ACTIVE"
            elif composite_score >= 0.25:
                strength = "WATCH"
            else:
                strength = "BACKGROUND"

            scenario_results.append({"strength": strength, "status": d['status']})

        metrics = calculate_metrics(scenario_results)
        print(f"| {s['label']} | {metrics['precision']:.1%} | {metrics['recall']:.1%} | {metrics['specificity']:.1%} | {metrics['peak_n']} | {metrics['peak_precision']:.1%} | {metrics['enrichment']:.2f}x |")
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
