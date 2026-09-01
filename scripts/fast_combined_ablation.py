import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.core.models import CanonicalChart, DomainPrediction, CorroborationEvidence
from app.astrology.predictions.framework import CorroborationEngine
from v312_audit_engine import DOMAIN_MAP

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
    os.environ["FLASK_SECRET_KEY"] = "audit-key-v312"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    cache_file = "data/backtest/raw/chart_cache.json"
    with open(cache_file, "r") as f:
        chart_cache = json.load(f)

    ORIGINAL_WEIGHTS = CorroborationEngine.WEIGHTS.copy()

    print("Running Baseline to collect evidence chain...")
    baseline_predictions = []
    with app.app_context():
        for i, case in enumerate(cases):
            case_key = f"{case['name']}_{case['dob']}_{case['tob']}"
            chart = CanonicalChart(**chart_cache[case_key])

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
                baseline_predictions.append({
                    "domain": event['domain'],
                    "status": event['status'],
                    "evidence_chain": [e.model_dump() for e in pred.evidence_chain],
                    "timing_window": pred.timing_window,
                    "baseline_strength": pred.prediction_strength
                })

    print(f"\nBaseline collected. Total events: {len(baseline_predictions)}")

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
        current_weights = ORIGINAL_WEIGHTS.copy()
        current_weights.update(s['overrides'])

        scenario_results = []
        for p in baseline_predictions:
            new_evidence = []
            for e_dict in p['evidence_chain']:
                e = CorroborationEvidence(**e_dict)
                w = ORIGINAL_WEIGHTS.get(e.source, 0)
                raw_ratio = e.strength_score / w if w != 0 else 0
                new_weight = current_weights.get(e.source, w)
                new_score = raw_ratio * new_weight

                new_evidence.append(CorroborationEvidence(
                    source=e.source,
                    level=e.level,
                    planet_involved=e.planet_involved,
                    house_involved=e.house_involved,
                    strength_score=new_score,
                    description=e.description,
                    rationale=e.rationale
                ))

            new_pred = CorroborationEngine.synthesize(p['domain'], "MODERATE", new_evidence, "Summary", p['timing_window'])
            scenario_results.append({
                "strength": new_pred.prediction_strength,
                "status": p['status']
            })

        metrics = calculate_metrics(scenario_results)
        print(f"| {s['label']} | {metrics['precision']:.1%} | {metrics['recall']:.1%} | {metrics['specificity']:.1%} | {metrics['peak_n']} | {metrics['peak_precision']:.1%} | {metrics['enrichment']:.2f}x |")
        metrics['label'] = s['label']
        all_results.append(metrics)

    base_spec = all_results[0]['specificity']
    no_foundation_spec = all_results[1]['specificity']
    no_secondary_spec = all_results[2]['specificity']

    foundation_gain = no_foundation_spec - base_spec
    secondary_gain = no_secondary_spec - base_spec

    print(f"\nAnalysis:")
    if foundation_gain > secondary_gain:
        print(f"DASHA_FOUNDATION is the primary driver of specificity regression.")
    elif secondary_gain > foundation_gain:
        print(f"SECONDARY_PROMISE is the primary driver of specificity regression.")
    elif foundation_gain > 0:
        print(f"Both features contribute to specificity regression.")
    else:
        print("Neither feature alone significantly improves specificity. Likely a deeper engine change.")

if __name__ == "__main__":
    main()
