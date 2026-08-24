from typing import Dict, List, Any

# Western Aspects (Major & Minor)
ASPECTS = {
    "Conjunction": {"deg": 0, "orb": 8},
    "Opposition": {"deg": 180, "orb": 8},
    "Trine": {"deg": 120, "orb": 8},
    "Square": {"deg": 90, "orb": 8},
    "Sextile": {"deg": 60, "orb": 6},
    "Quincunx": {"deg": 150, "orb": 2},
    "Semi-Square": {"deg": 45, "orb": 2},
    "Sesquiquadrate": {"deg": 135, "orb": 2}
}

def calculate_natal_western_aspects(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Calculate all aspects between natal planets using Western orbs."""
    results = []
    p_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]

    # Check if outer planets are in the dict, if not ignore
    available = [p for p in p_names if p in planets]

    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            p1_name = available[i]
            p2_name = available[j]
            p1_lon = planets[p1_name].longitude
            p2_lon = planets[p2_name].longitude

            diff = abs(p1_lon - p2_lon) % 360
            if diff > 180: diff = 360 - diff

            for asp_name, data in ASPECTS.items():
                target = data["deg"]
                orb = data["orb"]

                if abs(diff - target) < orb:
                    results.append({
                        "p1": p1_name,
                        "p2": p2_name,
                        "aspect": asp_name,
                        "orb": round(abs(diff - target), 2),
                        "interpretation": _get_aspect_text(p1_name, p2_name, asp_name)
                    })
    return results

def _get_aspect_text(p1: str, p2: str, aspect: str) -> str:
    # Logic for interpreting Western aspects
    if aspect == "Trine":
        return f"{p1} Trine {p2}: Harmonious flow of energy between {p1} and {p2}, suggesting natural talent and ease."
    if aspect == "Square":
        return f"{p1} Square {p2}: Dynamic tension between {p1} and {p2}, indicating internal conflict that leads to growth and action."
    return f"{p1} {aspect} {p2}: Significant energy exchange between these two planetary forces."
