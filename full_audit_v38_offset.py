
import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Enforce project root and environment
PROJECT_ROOT = os.getcwd()
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'calculation_service'))

# Set Ephemeris Path
os.environ["SE_EPHE_PATH"] = os.path.join(PROJECT_ROOT, "ephe")

# Mock the calc_client
from calculation_service.app.core.engine import calculate_natal_chart, calculate_transits_for_range
from app.astrology.core.calc_client import calc_client

def mock_get_natal_chart(year, month, day, hour, lat, lon, ayanamsa="LAHIRI"):
    return calculate_natal_chart(year, month, day, hour, lat, lon, ayanamsa)

def mock_get_transit_range(start, end, lat, lon):
    return calculate_transits_for_range(start, end, lat, lon)

calc_client.get_natal_chart = mock_get_natal_chart
calc_client.get_transit_range = mock_get_transit_range

# Imports
from app.astrology.core.chart import calculate_chart_data
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

FEATURE_NAMES = [
    "NATAL_PROMISE", "SECONDARY_PROMISE", "DASHA_ACTIVATION",
    "TRANSIT_TRIGGER", "DIVISIONAL_CONFIRM", "YOGA_SUPPORT",
    "PLANETARY_STRENGTH", "CONFLICTS"
]

STATE_NAMES = ["BACKGROUND", "WATCH", "ACTIVE", "PEAK"]

def run_audit():
    with open('data/backtest/raw/historical_cases.json', 'r') as f:
        cases = json.load(f)

    # Dictionary to store stats
    feature_stats = {f: {"event_present": 0, "event_absent": 0, "stable_present": 0, "stable_absent": 0} for f in FEATURE_NAMES}
    state_stats = {s: {"event": 0, "stable": 0} for s in STATE_NAMES}

    total_events = 0
    errors = []
    for case in cases:
        try:
            birth_dt = datetime.strptime(case["dob"] + " " + case["tob"], "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case["lat"], case["lon"], case["tz"])

            for event in case["events"]:
                domain_str = event["domain"]

                engine_func = None
                for k, v in DOMAIN_MAP.items():
                    if k.lower() in domain_str.lower():
                        engine_func = v
                        break

                if not engine_func: continue

                total_events += 1
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")

                # SIMULATION OFFSET: 15 days before the event
                sim_date = event_date - timedelta(days=15)

                # Run the relevant domain engine
                prediction = engine_func(chart, sim_date)

                is_event = event["status"] == "OCCURRED"

                # Presence/Absence of features
                active_features = {e.source for e in prediction.evidence_chain}

                for feat in FEATURE_NAMES:
                    present = feat in active_features
                    if is_event:
                        if present: feature_stats[feat]["event_present"] += 1
                        else: feature_stats[feat]["event_absent"] += 1
                    else:
                        if present: feature_stats[feat]["stable_present"] += 1
                        else: feature_stats[feat]["stable_absent"] += 1

                # State
                state = prediction.prediction_strength
                if state in state_stats:
                    if is_event:
                        state_stats[state]["event"] += 1
                    else:
                        state_stats[state]["stable"] += 1
        except Exception as e:
            errors.append(f"{case.get('name')}: {e}")

    # Results Generation
    print("# Feature Discrimination Audit Results (V3.8 Engine - 15 Day Lead)")
    print("| Feature | ERE | Hit Rate (Present) | Hit Rate (Absent) | Presence Rate |")
    print("|---|---|---|---|---|")

    for f in FEATURE_NAMES:
        stats = feature_stats[f]
        total_present = stats["event_present"] + stats["stable_present"]
        total_absent = stats["event_absent"] + stats["stable_absent"]

        hr_present = stats["event_present"] / total_present if total_present > 0 else 0
        hr_absent = stats["event_absent"] / total_absent if total_absent > 0 else 0

        ere = hr_present / hr_absent if hr_absent > 0 else 1.0
        presence_rate = total_present / (total_present + total_absent) if (total_present + total_absent) > 0 else 0

        print(f"| {f} | {ere:.2f} | {hr_present:.1%} | {hr_absent:.1%} | {presence_rate:.1%} |")

    print("\n# State Enrichment Results")
    print("| State | Hit Rate | Total Events |")
    print("|---|---|---|")
    for s in STATE_NAMES:
        stats = state_stats[s]
        total = stats["event"] + stats["stable"]
        hr = stats["event"] / total if total > 0 else 0
        print(f"| {s} | {hr:.1%} | {total} |")

    print("\n# Summary Statistics")
    print(f"- **Total Events Audited**: {total_events}")

if __name__ == "__main__":
    run_audit()
