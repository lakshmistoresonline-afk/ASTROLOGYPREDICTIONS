import json
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.astrology.core.chart import calculate_chart_data
from app.astrology.panchang import calculate_panchang_2_0

TEST_CASES = [
    {
        "id": "delhi_1980",
        "name": "Arjun",
        "dob": "1980-05-15",
        "tob": "10:30",
        "lat": 28.6139,
        "lon": 77.2090,
        "tz": "Asia/Kolkata",
        "place": "New Delhi, India"
    },
    {
        "id": "ny_1995",
        "name": "Sarah",
        "dob": "1995-10-25",
        "tob": "15:45",
        "lat": 40.7128,
        "lon": -74.0060,
        "tz": "America/New_York",
        "place": "New York, USA"
    },
    {
        "id": "london_1970",
        "name": "John",
        "dob": "1970-07-04",
        "tob": "04:20",
        "lat": 51.5074,
        "lon": -0.1278,
        "tz": "Europe/London",
        "place": "London, UK"
    },
    {
        "id": "sydney_2000",
        "name": "Kylie",
        "dob": "2000-01-01",
        "tob": "00:01",
        "lat": -33.8688,
        "lon": 151.2093,
        "tz": "Australia/Sydney",
        "place": "Sydney, Australia"
    }
]

def generate():
    output_dir = os.path.join(os.path.dirname(__file__), "baselines")
    os.makedirs(output_dir, exist_ok=True)

    for tc in TEST_CASES:
        print(f"Generating baseline for {tc['id']}...")
        birth_dt = datetime.strptime(f"{tc['dob']} {tc['tob']}", "%Y-%m-%d %H:%M")

        chart = calculate_chart_data(
            birth_dt, tc['lat'], tc['lon'], tc['tz']
        )

        panchang = calculate_panchang_2_0(
            birth_dt.date(), tc['lat'], tc['lon'], tc['tz']
        )

        baseline = {
            "test_case": tc,
            "chart": chart,
            "panchang": panchang
        }

        with open(os.path.join(output_dir, f"{tc['id']}.json"), "w") as f:
            json.dump(baseline, f, indent=2, default=str)

    print("Done.")

if __name__ == "__main__":
    generate()
