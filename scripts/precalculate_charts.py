import os
import sys
import json
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data

def main():
    os.environ["FLASK_SECRET_KEY"] = "audit-key-v312"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)

    cache_file = "data/backtest/raw/chart_cache.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    with app.app_context():
        for i, case in enumerate(cases):
            case_key = f"{case['name']}_{case['dob']}_{case['tob']}"
            if case_key in cache:
                print(f"[{i+1}/39] {case['name']} already in cache.")
                continue

            print(f"[{i+1}/39] Calculating {case['name']}...")
            birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case['lat'], case['lon'], case['tz'])
            cache[case_key] = chart.model_dump(mode='json')

            # Save every 5 cases to avoid total loss on timeout
            if (i + 1) % 5 == 0:
                with open(cache_file, "w") as f:
                    json.dump(cache, f)

    with open(cache_file, "w") as f:
        json.dump(cache, f)
    print("Precalculation complete.")

if __name__ == "__main__":
    main()
