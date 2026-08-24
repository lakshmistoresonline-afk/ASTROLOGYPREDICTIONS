from typing import Dict, List, Any
from ..core.models import CanonicalChart

ASPECT_TYPES = {
    0: "Conjunction",
    60: "Sextile",
    90: "Square",
    120: "Trine",
    180: "Opposition"
}

def calculate_transit_to_natal_aspects(natal_chart: CanonicalChart, transit_chart: CanonicalChart) -> List[Dict[str, Any]]:
    """
    Find all aspects between transiting planets and natal planets.
    Orb: 2 degrees.
    """
    results = []
    n_planets = natal_chart.planets
    t_planets = transit_chart.planets

    for t_name, t_info in t_planets.items():
        if t_name not in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            continue

        t_lon = t_info.longitude

        for n_name, n_info in n_planets.items():
            if n_name not in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
                continue

            n_lon = n_info.longitude

            diff = abs(t_lon - n_lon) % 360
            if diff > 180: diff = 360 - diff

            for deg, name in ASPECT_TYPES.items():
                if abs(diff - deg) < 2.0:
                    results.append({
                        "transit_planet": t_name,
                        "natal_planet": n_name,
                        "aspect": name,
                        "exact_diff": round(diff - deg, 2),
                        "interpretation": _get_aspect_meaning(t_name, n_name, name)
                    })

    return results

def _get_aspect_meaning(t: str, n: str, aspect: str) -> str:
    # Generic meanings for professional analysis
    if t == "Saturn" and aspect == "Conjunction":
        return f"Transit Saturn conjunct Natal {n}: A time of reckoning, structure, and potentially heavy responsibility."
    if t == "Jupiter" and aspect in ["Trine", "Sextile"]:
        return f"Transit Jupiter {aspect} Natal {n}: Expansion, opportunity, and favorable growth in areas related to {n}."
    return f"Transit {t} {aspect} Natal {n}: Activation of {n}'s energy through {t}'s current transit."
