from typing import Dict, List, Any

# Major Galactic Points (Sidereal Longitudes for Lahiri approx)
# Tropical values for 2026:
# Galactic Center: ~27 Sag
# Great Attractor: ~14 Sag
# Super Galactic Center: ~2 Lib
GALACTIC_POINTS = {
    "Galactic Center": 267.0, # ~27 deg Sidereal Sag
    "Great Attractor": 254.0, # ~14 deg Sidereal Sag
    "Super Galactic Center": 182.0, # ~2 deg Sidereal Libra
    "Andromeda Galaxy": 27.0, # ~27 deg Sidereal Aries
}

def analyze_galactic_aspects(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check for conjunctions with major galactic points (Orb 2 deg)."""
    results = []
    for p_name, p_info in planets.items():
        p_lon = getattr(p_info, "longitude", 0)
        for g_name, g_lon in GALACTIC_POINTS.items():
            diff = abs(p_lon - g_lon) % 360
            if diff > 180: diff = 360 - diff

            if diff < 2.0:
                results.append({
                    "planet": p_name,
                    "point": g_name,
                    "interpretation": f"{p_name} is aligned with the {g_name}, suggesting a high-frequency or 'galactic' influence on {p_name}'s expression."
                })
    return results
