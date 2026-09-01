import os
import sys
import json
from datetime import datetime, timedelta
from collections import defaultdict
import copy
from functools import lru_cache

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.framework import CorroborationEngine
from app.astrology.timing.precision import TimingWindowEngine, timing_engine

# Engines for domain mapping
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

# Caching for performance
_chart_cache = {}
def get_cached_chart(dt, lat, lon, tz):
    key = (dt, lat, lon, tz)
    if key not in _chart_cache:
        _chart_cache[key] = calculate_chart_data(dt, lat, lon, tz)
    return _chart_cache[key]

# Cache for transit data
import app.astrology.core.calc_client
_original_get_transit_range = app.astrology.core.calc_client.calc_client.get_transit_range
_transit_cache = {}

def cached_get_transit_range(start, end, lat, lon):
    key = (start, end, lat, lon)
    if key not in _transit_cache:
        _transit_cache[key] = _original_get_transit_range(start, end, lat, lon)
    return _transit_cache[key]

app.astrology.core.calc_client.calc_client.get_transit_range = cached_get_transit_range

# Save original methods and weights
ORIGINAL_WEIGHTS = copy.deepcopy(CorroborationEngine.WEIGHTS)
ORIGINAL_CALC_WINDOW = TimingWindowEngine.calculate_window

def run_experiment(name, cases):
    results = []

    for case in cases:
        birth_dt = datetime.strptime(f"{case['dob']} {case['tob']}", "%Y-%m-%d %H:%M")
        chart = get_cached_chart(birth_dt, case['lat'], case['lon'], case['tz'])

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
            results.append({
                "strength": pred.prediction_strength,
                "status": event['status']
            })

    # Calculate metrics
    tp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])
    fp = len([r for r in results if r['strength'] in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])
    tn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] != "OCCURRED"])
    fn = len([r for r in results if r['strength'] not in ["ACTIVE", "PEAK"] and r['status'] == "OCCURRED"])

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0

    peak_total = len([r for r in results if r['strength'] == "PEAK"])
    peak_hit = len([r for r in results if r['strength'] == "PEAK" and r['status'] == "OCCURRED"])
    peak_rate = peak_hit / peak_total if peak_total > 0 else 0

    active_total = len([r for r in results if r['strength'] == "ACTIVE"])
    active_hit = len([r for r in results if r['strength'] == "ACTIVE" and r['status'] == "OCCURRED"])
    active_rate = active_hit / active_total if active_total > 0 else 0

    return {
        "Config": name,
        "Precision": prec,
        "Recall": rec,
        "PEAK Rate": peak_rate,
        "ACTIVE Rate": active_rate
    }

def no_filter_calculate_window(chart, supporting_planets, houses, calculation_date=None):
    from app.astrology.timing.precision import HighPrecisionTransitEngine
    if calculation_date is None:
        start_date = datetime.now()
    else:
        start_date = calculation_date

    transit_events = HighPrecisionTransitEngine.get_transit_events(chart, start_date, start_date + timedelta(days=60))

    triggers = []
    for e in transit_events:
        if e.planet in supporting_planets:
            triggers.append(e)

    unique_planets = {e.planet for e in triggers}
    trigger_count = len(unique_planets)
    triggers.sort(key=lambda x: x.peak_date)

    valid_peak_event = None
    for t in triggers:
        t_dt = datetime.strptime(t.peak_date, "%Y-%m-%d")
        dist = abs((t_dt - start_date).days)
        if dist <= 30:
            valid_peak_event = t
            break

    if valid_peak_event:
        peak_dt = datetime.strptime(valid_peak_event.peak_date, "%Y-%m-%d")
        days_to_peak = (peak_dt - start_date).days
        PLANET_IMPORTANCE = {
            "Moon": 0.1, "Mercury": 0.3, "Venus": 0.4, "Sun": 0.4,
            "Mars": 0.7, "Jupiter": 1.0, "Saturn": 1.0, "Rahu": 1.0, "Ketu": 1.0
        }
        p_imp = PLANET_IMPORTANCE.get(valid_peak_event.planet, 0.5)
        abs_dist = abs(days_to_peak)
        if abs_dist <= 7:
            phase = "PEAK_MANIFESTATION"
            temporal_weight = 1.0
        elif abs_dist <= 21:
            phase = "NEAR_TERM_ACTIVE"
            temporal_weight = 0.35
        else:
            phase = "BUILD_UP"
            temporal_weight = 0.05
        convergence_bonus = 1.4 if trigger_count >= 2 else 0.7
        proximity_weight = temporal_weight * p_imp * convergence_bonus
        return {
            "phase": phase,
            "activation": (peak_dt - timedelta(days=20)).strftime("%Y-%m-%d"),
            "build": (peak_dt - timedelta(days=7)).strftime("%Y-%m-%d"),
            "peak": peak_dt.strftime("%Y-%m-%d"),
            "manifestation": (peak_dt + timedelta(days=3)).strftime("%Y-%m-%d"),
            "decline": (peak_dt + timedelta(days=15)).strftime("%Y-%m-%d"),
            "description": f"{valid_peak_event.planet} {valid_peak_event.event_type} trigger.",
            "timing_confidence": f"{phase} ({int(proximity_weight*100)}%)",
            "proximity_weight": proximity_weight,
            "days_to_peak": days_to_peak,
            "trigger_count": trigger_count
        }
    else:
        return {
            "phase": "STABLE_BACKGROUND",
            "activation": start_date.strftime("%Y-%m-%d"),
            "build": (start_date + timedelta(days=30)).strftime("%Y-%m-%d"),
            "peak": (start_date + timedelta(days=60)).strftime("%Y-%m-%d"),
            "manifestation": (start_date + timedelta(days=65)).strftime("%Y-%m-%d"),
            "decline": (start_date + timedelta(days=90)).strftime("%Y-%m-%d"),
            "description": "General life-period support (No immediate trigger).",
            "timing_confidence": "LOW (Dasha Only)",
            "proximity_weight": 0.0,
            "days_to_peak": 999,
            "trigger_count": 0
        }

def main():
    os.environ["FLASK_SECRET_KEY"] = "ablation-key"
    app = create_app()

    with open("data/backtest/raw/historical_cases.json", "r") as f:
        cases = json.load(f)[:15]

    ablation_results = []

    with app.app_context():
        # 1. BASELINE
        CorroborationEngine.WEIGHTS = copy.deepcopy(ORIGINAL_WEIGHTS)
        ablation_results.append(run_experiment("BASELINE", cases))

        # 2. NO_DASHA
        CorroborationEngine.WEIGHTS = copy.deepcopy(ORIGINAL_WEIGHTS)
        CorroborationEngine.WEIGHTS["DASHA_ACTIVATION"] = 0.0
        ablation_results.append(run_experiment("NO_DASHA", cases))

        # 3. NO_TRANSIT
        CorroborationEngine.WEIGHTS = copy.deepcopy(ORIGINAL_WEIGHTS)
        CorroborationEngine.WEIGHTS["TRANSIT_TRIGGER"] = 0.0
        ablation_results.append(run_experiment("NO_TRANSIT", cases))

        # 4. NO_VARGA
        CorroborationEngine.WEIGHTS = copy.deepcopy(ORIGINAL_WEIGHTS)
        CorroborationEngine.WEIGHTS["DIVISIONAL_CONFIRM"] = 0.0
        ablation_results.append(run_experiment("NO_VARGA", cases))

        # 5. NO_FILTER
        # Clear transit cache just in case, though the logic change is in timing_engine
        # Actually NO_FILTER still uses the same raw transits, so cache is fine.
        CorroborationEngine.WEIGHTS = copy.deepcopy(ORIGINAL_WEIGHTS)
        import app.astrology.timing.precision
        app.astrology.timing.precision.timing_engine.calculate_window = no_filter_calculate_window
        ablation_results.append(run_experiment("NO_FILTER", cases))
        app.astrology.timing.precision.timing_engine.calculate_window = ORIGINAL_CALC_WINDOW

    # Print Table
    print("\n| Configuration | Precision | Recall | PEAK Rate | ACTIVE Rate |")
    print("|---------------|-----------|--------|-----------|-------------|")
    for r in ablation_results:
        print(f"| {r['Config']:13} | {r['Precision']:9.1%} | {r['Recall']:6.1%} | {r['PEAK Rate']:9.1%} | {r['ACTIVE Rate']:11.1%} |")

if __name__ == "__main__":
    main()
