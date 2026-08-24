from typing import Dict, List, Any

# Popular Uranian Formulas (A+B-C)
FORMULAS = {
    "Marriage": ("Venus", "Jupiter", "Sun"), # Venus + Jupiter - Sun
    "Fame": ("Jupiter", "Apollon", "Sun"),
    "Success": ("Jupiter", "Sun", "Saturn"),
    "Money": ("Jupiter", "Venus", "Mercury")
}

def calculate_uranian_formulas(planets: Dict[str, Any], tnps: Dict[str, Any]) -> Dict[str, float]:
    """Calculate sensitive points based on planetary algebra."""
    all_p = {**planets, **tnps}
    results = {}

    for name, (a, b, c) in FORMULAS.items():
        if a in all_p and b in all_p and c in all_p:
            lon_a = getattr(all_p[a], "longitude", all_p[a].get("longitude", 0))
            lon_b = getattr(all_p[b], "longitude", all_p[b].get("longitude", 0))
            lon_c = getattr(all_p[c], "longitude", all_p[c].get("longitude", 0))

            results[name] = (lon_a + lon_b - lon_c + 360) % 360

    return results
