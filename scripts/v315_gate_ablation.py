import os
import sys
import json
from datetime import datetime, timedelta
from v314_validation import DOMAIN_MAP

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data

def main():
    os.environ["FLASK_SECRET_KEY"] = "val-key"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    # 1. Pre-calculate all predictions once
    all_data = []
    print("Pre-calculating base predictions...")
    with app.app_context():
        for case in cases:
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

                all_data.append({
                    "score": pred.score / 100.0,
                    "q": pred.quality_score,
                    "phase": pred.timing_window.get("phase"),
                    "weight": pred.timing_window.get("proximity_weight", 0),
                    "status": event['status']
                })

    # 2. Run ablation on cached data
    thresholds = [0.40, 0.45, 0.50, 0.55, 0.60]
    print("\n| Threshold | Precision | Recall | Specificity | WATCH Recall |")
    print("| :--- | :---: | :---: | :---: | :---: |")

    for t in thresholds:
        results = []
        for d in all_data:
            phase = d["phase"]
            weight = d["weight"]
            comp_score = d["score"]
            q_score = d["q"]

            is_peak = (phase == "PEAK_MANIFESTATION")
            is_active_orig = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

            is_active = is_active_orig
            if phase == "NEAR_TERM_ACTIVE" and weight < t:
                is_active = False

            strength = "BACKGROUND"
            if comp_score >= 0.65 and is_peak and q_score >= 52:
                 strength = "PEAK"
            elif comp_score >= 0.45 and is_active and q_score >= 38:
                 strength = "ACTIVE"
            elif comp_score >= 0.25 or (comp_score >= 0.15 and is_active_orig): # Key Fix: Use orig is_active for WATCH
                 strength = "WATCH"

            results.append({"strength": strength, "status": d["status"]})

        tp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
        fp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])
        fn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
        tn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])

        tp_watch = len([r for r in results if r['strength'] in ["WATCH", "ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
        fn_watch = len([r for r in results if r['strength'] not in ["WATCH", "ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        watch_recall = tp_watch / (tp_watch + fn_watch) if (tp_watch + fn_watch) > 0 else 0

        print(f"| {t:.2f} | {precision:.1%} | {recall:.1%} | {specificity:.1%} | {watch_recall:.1%} |")

if __name__ == "__main__":
    main()
