
import os
import sys
import json
from datetime import datetime, timedelta

PROJECT_ROOT = os.getcwd()
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'calculation_service'))
os.environ["SE_EPHE_PATH"] = os.path.join(PROJECT_ROOT, "ephe")

from calculation_service.app.core.engine import calculate_natal_chart, calculate_transits_for_range
from app.astrology.core.calc_client import calc_client
calc_client.get_natal_chart = calculate_natal_chart
calc_client.get_transit_range = calculate_transits_for_range

from app.astrology.core.chart import calculate_chart_data
from app.astrology.timing.precision import HighPrecisionTransitEngine

def test():
    # Steve Jobs
    case = {
        "name": "Steve Jobs",
        "dob": "1955-02-24",
        "tob": "19:15",
        "lat": 37.7749,
        "lon": -122.4194,
        "tz": "America/Los_Angeles"
    }
    birth_dt = datetime.strptime(case["dob"] + " " + case["tob"], "%Y-%m-%d %H:%M")
    chart = calculate_chart_data(birth_dt, case["lat"], case["lon"], case["tz"])

    event_date = datetime.strptime("1980-12-12", "%Y-%m-%d")

    print(f"Ascendant: {chart.ascendant} (Rashi {chart.asc_rashi})")
    print(f"House Lords: {chart.house_lords}")

    # Career triggers: Jupiter and 10th Lord
    l10 = chart.house_lords[10]
    supporting = ["Jupiter", l10]
    houses = [10, 11, 1]

    print(f"Supporting: {supporting}, Houses: {houses}")

    scan_start = event_date - timedelta(days=30)
    scan_end = event_date + timedelta(days=30)

    events = HighPrecisionTransitEngine.get_transit_events(chart, scan_start, scan_end)
    print(f"Total events found: {len(events)}")
    for e in events:
        print(f"  {e.planet} {e.event_type} on {e.peak_date} (Target: {e.target_natal}, Orb: {e.orb:.2f}, House: {e.house})")

if __name__ == "__main__":
    test()
