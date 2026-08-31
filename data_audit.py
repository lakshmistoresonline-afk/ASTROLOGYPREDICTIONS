
import sys
import os
import json
from datetime import datetime

# Enforce project root and environment
PROJECT_ROOT = os.getcwd()
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'calculation_service'))

# Set Ephemeris Path
os.environ["SE_EPHE_PATH"] = os.path.join(PROJECT_ROOT, "ephe")

# Mock the calc_client
from calculation_service.app.core.engine import calculate_natal_chart
from app.astrology.core.calc_client import calc_client

def mock_get_natal_chart(year, month, day, hour, lat, lon, ayanamsa="LAHIRI"):
    return calculate_natal_chart(year, month, day, hour, lat, lon, ayanamsa)

calc_client.get_natal_chart = mock_get_natal_chart

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

FEATURE_NAMES = [
    "NATAL_PROMISE", "SECONDARY_PROMISE", "DASHA_ACTIVATION",
    "TRANSIT_TRIGGER", "DIVISIONAL_CONFIRM", "YOGA_SUPPORT",
    "PLANETARY_STRENGTH", "CONFLICTS"
]

STATE_NAMES = ["BACKGROUND", "WATCH", "ACTIVE", "PEAK"]

def get_engine(domain_str):
    if "Career" in domain_str: return CareerPredictionEngine
    if "Finance" in domain_str or "Wealth" in domain_str: return FinancePredictionEngine
    if "Marriage" in domain_str or "Relationship" in domain_str: return MarriagePredictionEngine
    if "Education" in domain_str or "Knowledge" in domain_str: return EducationPredictionEngine
    if "Business" in domain_str: return BusinessPredictionEngine
    if "Fame" in domain_str or "Reputation" in domain_str: return FamePredictionEngine
    if "Spirituality" in domain_str or "Growth" in domain_str: return SpiritualityPredictionEngine
    if "Health" in domain_str: return HealthPredictionEngine
    if "Property" in domain_str: return PropertyPredictionEngine
    if "Travel" in domain_str: return TravelPredictionEngine
    if "Children" in domain_str: return ChildrenPredictionEngine
    if "Foreign" in domain_str: return ForeignSettlementEngine
    if "Family" in domain_str: return FamilyPredictionEngine
    if "Vehicles" in domain_str: return VehiclesPredictionEngine
    if "Legal" in domain_str: return LegalPredictionEngine
    return None

def run_audit():
    with open('data/backtest/raw/historical_cases.json', 'r') as f:
        cases = json.load(f)

    feature_counts = {f: {"present": 0, "absent": 0, "present_occurred": 0, "absent_occurred": 0} for f in FEATURE_NAMES}
    state_counts = {s: {"total": 0, "occurred": 0} for s in STATE_NAMES}

    total_events = 0
    for case in cases:
        try:
            birth_dt = datetime.strptime(case["dob"] + " " + case["tob"], "%Y-%m-%d %H:%M")
            chart = calculate_chart_data(birth_dt, case["lat"], case["lon"], case["tz"])

            for event in case["events"]:
                domain = event["domain"]
                engine = get_engine(domain)
                if not engine:
                    continue

                total_events += 1
                event_date = datetime.strptime(event["date"], "%Y-%m-%d")
                prediction = engine.get_prediction(chart, event_date)

                evidence_sources = {e.source for e in prediction.evidence_chain}
                occurred = event["status"] == "OCCURRED"

                for f in FEATURE_NAMES:
                    if f in evidence_sources:
                        feature_counts[f]["present"] += 1
                        if occurred:
                            feature_counts[f]["present_occurred"] += 1
                    else:
                        feature_counts[f]["absent"] += 1
                        if occurred:
                            feature_counts[f]["absent_occurred"] += 1

                state = prediction.prediction_strength
                if state in state_counts:
                    state_counts[state]["total"] += 1
                    if occurred:
                        state_counts[state]["occurred"] += 1
        except Exception as e:
            # print(f"Error processing case {case.get('name')}: {e}")
            pass

    # Results Calculation
    print("# Feature Discrimination Audit Results")
    print("| Feature | ERE | Hit Rate (Present) | Hit Rate (Absent) | Presence Rate |")
    print("|---|---|---|---|---|")

    non_discriminative = []

    for f in FEATURE_NAMES:
        counts = feature_counts[f]
        hr_present = counts["present_occurred"] / counts["present"] if counts["present"] > 0 else 0
        hr_absent = counts["absent_occurred"] / counts["absent"] if counts["absent"] > 0 else 0
        ere = hr_present / hr_absent if hr_absent > 0 else 1.0
        presence_rate = counts["present"] / (counts["present"] + counts["absent"]) if (counts["present"] + counts["absent"]) > 0 else 0

        print(f"| {f} | {ere:.2f} | {hr_present:.2%} | {hr_absent:.2%} | {presence_rate:.2%} |")

        if 0.85 <= ere <= 1.15:
            non_discriminative.append(f)

    print("\n# State Enrichment Results")
    print("| State | Hit Rate | Total Cases |")
    print("|---|---|---|")
    for s in STATE_NAMES:
        counts = state_counts[s]
        hr = counts["occurred"] / counts["total"] if counts["total"] > 0 else 0
        print(f"| {s} | {hr:.2%} | {counts['total']} |")

    print("\n# Analysis")
    print(f"- **Non-discriminative features (ERE ≈ 1.0)**: {', '.join(non_discriminative) if non_discriminative else 'None'}")
    print(f"- **Total Events Processed**: {total_events}")

if __name__ == "__main__":
    run_audit()
