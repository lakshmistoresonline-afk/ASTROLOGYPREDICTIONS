import os
import sys
import json
from datetime import datetime, timedelta
from v314_validation import DOMAIN_MAP
from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.timing.precision import TimingWindowEngine

def run_test(domain_to_test, lag_value):
    # Override lag
    TimingWindowEngine.MANIFESTATION_LAG[domain_to_test] = lag_value

    app = create_app()
    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    hits = 0
    total = 0
    with app.app_context():
        for case in cases:
            birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])

            for event in case['events']:
                if event['status'] != "OCCURRED": continue
                if domain_to_test.lower() not in event['domain'].lower(): continue

                total += 1
                event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                sim_date = event_date - timedelta(days=30)

                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in event['domain'].lower():
                        engine_func = v
                        break

                pred = engine_func(chart, sim_date)
                if pred.prediction_strength in ["ACTIVE", "PEAK"]:
                    hits += 1

    return hits, total

def main():
    os.environ["FLASK_SECRET_KEY"] = "ablation-key"

    domains = ["Career & Authority", "Education & Knowledge"]
    lags = [0, 7, 14, 21, 28, 35, 42, 50]

    print("# V3.14 Timing Ablation Study\n")
    for d in domains:
        print(f"## Domain: {d}")
        print("| Lag (Days) | Hits | Recall |")
        print("| :--- | :---: | :---: |")
        for l in lags:
            h, t = run_test(d, l)
            recall = h / t if t > 0 else 0
            print(f"| {l} | {h}/{t} | {recall:.1%} |")
        print("\n")

if __name__ == "__main__":
    main()
