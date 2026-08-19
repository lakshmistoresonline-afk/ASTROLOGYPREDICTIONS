from typing import Dict, List, Tuple

def calculate_charakarakas(planets: Dict[str, float]) -> Dict[str, str]:
    """
    Calculate the 7 Jaimini Charakarakas based on degrees (0-30).
    Input: Dict of {planet_name: longitude}
    """
    # 7 planets used in Jaimini (Rahu/Ketu usually excluded in 7-karaka system)
    eligible = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    # Get degrees within sign
    planet_degrees = []
    for name in eligible:
        if name in planets:
            deg = planets[name] % 30
            planet_degrees.append((name, deg))

    # Sort by descending degree
    sorted_planets = sorted(planet_degrees, key=lambda x: x[1], reverse=True)

    names = [
        "Atmakaraka (AK) - Soul",
        "Amatyakaraka (AmK) - Career/Mind",
        "Bhratrukaraka (BK) - Siblings",
        "Matrukaraka (MK) - Mother",
        "Putrakaraka (PK) - Children",
        "Gnatikaraka (GK) - Challenges",
        "Darakaraka (DK) - Spouse"
    ]

    result = {}
    for i in range(min(len(sorted_planets), len(names))):
        result[names[i]] = sorted_planets[i][0]

    return result
