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
                    "name": case['name'],
                    "domain": event['domain'],
                    "score": pred.score / 100.0,
                    "q": pred.quality_score,
                    "phase": pred.timing_window.get("phase"),
                    "weight": pred.timing_window.get("proximity_weight", 0),
                    "status": event['status']
                })

    # 2. Run ablation on cached data with domain-specific Q thresholds
    # We'll test lowering gate_q for Fame
    q_thresholds = [30, 34, 38, 40, 44]
    print("\n| Fame Gate Q | Fame Recall | Global Precision | Global Recall | Specificity |")
    print("| :--- | :---: | :---: | :---: | :---: |")

    for q_fame in q_thresholds:
        results = []
        fame_hits = 0
        fame_total = 0

        for d in all_data:
            domain = d["domain"]
            phase = d["phase"]
            weight = d["weight"]
            comp_score = d["score"]
            q_score = d["q"]

            is_peak = (phase == "PEAK_MANIFESTATION")
            is_active_orig = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

            is_active = is_active_orig
            if phase == "NEAR_TERM_ACTIVE" and weight < 0.50:
                is_active = False

            # Domain-Specific Thresholds
            gate_score = 0.45
            gate_q = 38
            if any(dm in domain for dm in ["Career", "Education", "Fame"]):
                 gate_score = 0.38
                 gate_q = 44 # V3.14 default
                 if "Fame" in domain:
                      gate_q = q_fame

            strength = "BACKGROUND"
            if comp_score >= 0.65 and is_peak and q_score >= 52:
                 strength = "PEAK"
            elif comp_score >= gate_score and is_active and q_score >= gate_q:
                 strength = "ACTIVE"
            elif comp_score >= 0.25 or (comp_score >= 0.15 and is_active_orig):
                 strength = "WATCH"

            results.append({"strength": strength, "status": d["status"]})

            if "Fame" in domain and d["status"] == "OCCURRED":
                fame_total += 1
                if strength in ["ACTIVE", "PEAK"]:
                    fame_hits += 1

        tp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
        fp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])
        fn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
        tn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f_recall = fame_hits / fame_total if fame_total > 0 else 0

        print(f"| {q_fame} | {f_recall:.1%} | {precision:.1%} | {recall:.1%} | {specificity:.1%} |")

if __name__ == "__main__":
    main()
