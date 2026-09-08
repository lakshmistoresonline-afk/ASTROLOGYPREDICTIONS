from datetime import datetime, timedelta
from typing import Dict, Any
from .chart import calculate_chart_data

def evaluate_birth_time_confidence(birth_dt: datetime, lat: float, lon: float, tz_str: str, stated_confidence: str = "HIGH") -> Dict[str, Any]:
    """
    V4 Birth-Time Confidence & Sensitivity Analysis Subsystem.
    Evaluates sensitivity to birth time variations (±1 min, ±5 min, ±15 min).
    """
    base_chart = calculate_chart_data(birth_dt, lat, lon, tz_str)
    base_asc = base_chart.ascendant
    base_asc_rashi = base_chart.asc_rashi

    # Sensitivity checks
    shifts = [1, 5, 15]
    sensitivity_results = {}
    lagna_stable = True

    for minutes in shifts:
        dt_plus = birth_dt + timedelta(minutes=minutes)
        dt_minus = birth_dt - timedelta(minutes=minutes)

        try:
            chart_plus = calculate_chart_data(dt_plus, lat, lon, tz_str)
            chart_minus = calculate_chart_data(dt_minus, lat, lon, tz_str)

            stable = (chart_plus.asc_rashi == base_asc_rashi) and (chart_minus.asc_rashi == base_asc_rashi)
            if not stable:
                lagna_stable = False

            sensitivity_results[f"plus_minus_{minutes}_min"] = {
                "lagna_stable": stable,
                "asc_diff_plus": round(abs(chart_plus.ascendant - base_asc), 3),
                "asc_diff_minus": round(abs(chart_minus.ascendant - base_asc), 3)
            }
        except Exception:
            sensitivity_results[f"plus_minus_{minutes}_min"] = {"error": True}

    confidence_level = stated_confidence
    if not lagna_stable and confidence_level == "HIGH":
        confidence_level = "MEDIUM"

    return {
        "stated_confidence": stated_confidence,
        "evaluated_confidence": confidence_level,
        "lagna_stable_15m": lagna_stable,
        "sensitivity_analysis": sensitivity_results,
        "recommendation": "High stability" if lagna_stable else "Birth time rectification recommended due to Ascendant boundary proximity."
    }
