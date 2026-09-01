
import os
import sys
import json
from datetime import datetime, timedelta
from statistics import median

PROJECT_ROOT = os.getcwd()
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'calculation_service'))
os.environ["SE_EPHE_PATH"] = os.path.join(PROJECT_ROOT, "ephe")

from calculation_service.app.core.engine import calculate_natal_chart, calculate_transits_for_range
from app.astrology.core.calc_client import calc_client
calc_client.get_natal_chart = calculate_natal_chart
calc_client.get_transit_range = calculate_transits_for_range

from app.astrology.core.chart import calculate_chart_data
from app.astrology.timing.precision import TimingWindowEngine, timing_engine, HighPrecisionTransitEngine
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

CURRENT_SHIFT = 14

def patched_calculate_window(self, chart, supporting_planets, houses, calculation_date=None):
    if calculation_date is None: start_date = datetime.now()
    else: start_date = calculation_date

    # Use original logic: scan 60 days ahead
    transit_events = HighPrecisionTransitEngine.get_transit_events(chart, start_date, start_date + timedelta(days=60))
    relevant_natal_planets = {chart.house_lords.get(h) for h in houses}

    triggers = []
    for e in transit_events:
        if e.planet in supporting_planets:
            if e.house in houses or e.target_natal in relevant_natal_planets:
                triggers.append(e)

    triggers.sort(key=lambda x: x.peak_date)

    valid_peak_event = None
    # Pick the first trigger in the window
    if triggers:
        valid_peak_event = triggers[0]

    if valid_peak_event:
        peak_dt = datetime.strptime(valid_peak_event.peak_date, "%Y-%m-%d")
        manifest_peak = peak_dt + timedelta(days=CURRENT_SHIFT)
        return {"phase": "PEAK", "peak": manifest_peak.strftime("%Y-%m-%d"), "proximity_weight": 1.0}
    else:
        return {"phase": "NONE", "peak": None}

TimingWindowEngine.calculate_window = patched_calculate_window

def run_ablation():
    with open('data/backtest/raw/historical_cases.json', 'r') as f:
        all_cases = json.load(f)

    cases = all_cases[:15]
    shifts = [0, 7, 10, 14, 21]
    results = {}

    for shift in shifts:
        global CURRENT_SHIFT
        CURRENT_SHIFT = shift
        errors = []
        hits_3, hits_7, hits_15 = 0, 0, 0
        total_events = 0

        for case in cases:
            try:
                birth_dt = datetime.strptime(case["dob"] + " " + case["tob"], "%Y-%m-%d %H:%M")
                chart = calculate_chart_data(birth_dt, case["lat"], case["lon"], case["tz"])

                for event in case["events"]:
                    if event["status"] != "OCCURRED": continue

                    domain_str = event["domain"]
                    engine_func = None
                    for k, v in DOMAIN_MAP.items():
                        if k.lower() in domain_str.lower():
                            engine_func = v
                            break

                    if not engine_func: continue

                    total_events += 1
                    event_date = datetime.strptime(event["date"], "%Y-%m-%d")

                    # Run engine 30 days before the event to let it find the trigger
                    prediction = engine_func(chart, event_date - timedelta(days=30))
                    pred_peak_str = prediction.timing_window.get("peak")

                    if pred_peak_str:
                        pred_peak = datetime.strptime(pred_peak_str, "%Y-%m-%d")
                        abs_error = abs((pred_peak - event_date).days)
                        errors.append(abs_error)
                        if abs_error <= 3: hits_3 += 1
                        if abs_error <= 7: hits_7 += 1
                        if abs_error <= 15: hits_15 += 1
                    else:
                        errors.append(99)
            except:
                pass

        valid_errors = [e for e in errors if e < 99]
        results[shift] = {
            "hit_3": hits_3 / total_events if total_events > 0 else 0,
            "hit_7": hits_7 / total_events if total_events > 0 else 0,
            "hit_15": hits_15 / total_events if total_events > 0 else 0,
            "median_error": median(valid_errors) if valid_errors else 99,
            "total": total_events
        }

    print("# Timing Ablation Study: Manifestation Shift Results")
    print("| Shift | Hit Rate ±3d | Hit Rate ±7d | Hit Rate ±15d | Median Error |")
    print("|-------|--------------|--------------|---------------|--------------|")
    for shift in sorted(results.keys()):
        r = results[shift]
        label = f"{shift} days" + (" (Current)" if shift == 14 else "")
        print(f"| {label} | {r['hit_3']:.1%} | {r['hit_7']:.1%} | {r['hit_15']:.1%} | {r['median_error']:.1f} days |")

if __name__ == "__main__":
    run_ablation()
