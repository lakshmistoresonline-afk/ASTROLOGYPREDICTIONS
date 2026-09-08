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

    print("# V3.15 FALSE POSITIVE AUDIT\n")
    print("| Name | Domain | Date | Score | Q | Weight | Phase | Groups |")
    print("| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |")

    with app.app_context():
        for case in cases:
            birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])

            # Events that DID NOT occur
            for event in case['events']:
                if event['status'] == "OCCURRED": continue

                event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                sim_date = event_date - timedelta(days=30)

                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in event['domain'].lower():
                        engine_func = v
                        break
                if not engine_func: continue

                pred = engine_func(chart, sim_date)

                if pred.prediction_strength in ["ACTIVE", "PEAK"]:
                     groups = set()
                     LAYER_GROUPS = {
                        "NATAL_PROMISE": "PROMISE", "SECONDARY_PROMISE": "PROMISE",
                        "DASHA_ACTIVATION": "DASHA", "DASHA_FOUNDATION": "DASHA",
                        "TRANSIT_TRIGGER": "TRANSIT", "DIVISIONAL_CONFIRM": "VARGA",
                        "YOGA_SUPPORT": "NATAL_OTHER", "ASPECT_SUPPORT": "NATAL_OTHER",
                        "PLANETARY_STRENGTH": "NATAL_OTHER"
                    }
                     for e in pred.evidence_chain:
                        if e.strength_score > 0:
                            groups.add(LAYER_GROUPS.get(e.source, "OTHER"))

                     print(f"| {case['name']} | {event['domain']} | {event['date']} | {pred.score:.2f} | {pred.quality_score:.2f} | {pred.timing_window.get('proximity_weight', 0):.2f} | {pred.timing_window.get('phase')} | {','.join(groups)} |")

if __name__ == "__main__":
    main()
