from typing import Dict, List, Any
import swisseph as swe

def get_weather_indicators(jd_ut: float) -> Dict[str, Any]:
    """
    Meteorological Astrology (Astrometeorology).
    Predicting weather patterns based on planetary configurations.
    """
    results = {}

    # 1. Elements of Signs occupied by major planets
    # Fire: Heat/Dry, Earth: Cold/Dry, Air: Warm/Moist, Water: Cold/Moist
    elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}

    planet_pids = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
                   "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN}

    for name, pid in planet_pids.items():
        res = swe.calc_ut(jd_ut, pid)
        lon = res[0][0]
        rashi = int(lon // 30)

        # Mapping
        if rashi in [0, 4, 8]: elements["Fire"] += 1
        elif rashi in [1, 5, 9]: elements["Earth"] += 1
        elif rashi in [2, 6, 10]: elements["Air"] += 1
        elif rashi in [3, 7, 11]: elements["Water"] += 1

    dominant = max(elements, key=elements.get)

    # 2. Specific Configurations
    weather_notes = []
    # Sun-Mars: Heat waves, dryness.
    # Sun-Saturn: Cold, storms.
    # Jupiter-Venus: Pleasant, moisture.
    # Mercury-Uranus: High winds, sudden changes.

    results["dominant_element"] = dominant
    results["planetary_weather_notes"] = weather_notes
    results["forecast_type"] = _get_forecast_type(dominant)

    return results

def _get_forecast_type(element: str) -> str:
    types = {
        "Fire": "Hot and Dry - Potential for heatwaves or droughts.",
        "Earth": "Cool and Dry - Grounded, stable, but potentially chilly.",
        "Air": "Warm and Windy - Changeable weather, high pressure shifts.",
        "Water": "Cool and Moist - High probability of precipitation or humidity."
    }
    return types.get(element, "Variable")
