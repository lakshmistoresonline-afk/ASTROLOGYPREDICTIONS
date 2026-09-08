import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from v314_validation import DOMAIN_MAP

def main():
    os.environ["FLASK_SECRET_KEY"] = "val-key"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    print("# V3.15 FULL OCCURRED EVENT AUDIT\n")
    print("| Name | Domain | Date | Strength | Score | Q | Weight | Phase |")
    print("| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |")

    with app.app_context():
        for case in cases:
            birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])

            for event in case['events']:
                if event['status'] != "OCCURRED": continue

                event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                sim_date = event_date - timedelta(days=30)

                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in event['domain'].lower():
                        engine_func = v
                        break
                if not engine_func: continue

                pred = engine_func(chart, sim_date)

                print(f"| {case['name']} | {event['domain']} | {event['date']} | {pred.prediction_strength} | {pred.score:.2f} | {pred.quality_score:.2f} | {pred.timing_window.get('proximity_weight', 0):.2f} | {pred.timing_window.get('phase')} |")

if __name__ == "__main__":
    main()
