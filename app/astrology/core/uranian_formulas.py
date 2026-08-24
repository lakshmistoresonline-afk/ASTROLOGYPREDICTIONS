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

    def get_lon(obj):
        if hasattr(obj, 'longitude'): return obj.longitude
        if isinstance(obj, dict): return obj.get('longitude', 0.0)
        return 0.0

    for name, (a, b, c) in FORMULAS.items():
        if a in all_p and b in all_p and c in all_p:
            lon_a = get_lon(all_p[a])
            lon_b = get_lon(all_p[b])
            lon_c = get_lon(all_p[c])

            results[name] = (lon_a + lon_b - lon_c + 360) % 360

    return results
