from typing import Dict, Any

def get_draconic_chart(natal_planets: Dict[str, Any], rahu_longitude: float) -> Dict[str, float]:
    """
    Draconic Chart: Shift the entire chart so that the North Node (Rahu) is at 0° Aries.
    Represents the soul's intent.
    """
    # Offset = 360 - Rahu Longitude
    # So Rahu + Offset = 360 (or 0)
    offset = (360 - rahu_longitude) % 360

    results = {}
    for name, p_info in natal_planets.items():
        if hasattr(p_info, "longitude"):
            results[name] = (p_info.longitude + offset) % 360

    return results
