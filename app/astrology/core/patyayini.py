from typing import Dict, List, Any

def calculate_patyayini_bala(planets: Dict[str, Any], asc_deg: float) -> Dict[str, float]:
    """
    Patyayini Bala:
    Strength based on degrees within a sign.
    """
    eligible = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]

    # 1. Get degrees within sign
    degs = []
    for name in eligible:
        if name == "Lagna":
            degs.append(("Lagna", asc_deg % 30))
        elif name in planets:
            degs.append((name, planets[name].degree))

    # 2. Sort by degree
    sorted_degs = sorted(degs, key=lambda x: x[1])

    # 3. Calculate increments
    # 1st planet gets its full degree.
    # 2nd gets (degree2 - degree1), etc.
    results = {}
    prev_deg = 0.0
    for name, deg in sorted_degs:
        diff = deg - prev_deg
        results[name] = round(diff, 2)
        prev_deg = deg

    return results
