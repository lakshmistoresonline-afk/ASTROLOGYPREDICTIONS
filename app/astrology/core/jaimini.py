from typing import Dict, List, Tuple, Any
from ..predictions.framework import are_associated

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

def get_jaimini_drishti(sign: int) -> List[int]:
    """
    Jaimini Rashi Drishti:
    Movable signs (1,4,7,10) aspect Fixed signs (2,5,8,11) except the adjacent one.
    Fixed signs (2,5,8,11) aspect Movable signs (1,4,7,10) except the adjacent one.
    Dual signs (3,6,9,12) aspect each other.
    Input: sign (0-11)
    """
    # Signs are 0-indexed: 0=Aries...
    # Types: 0=Movable, 1=Fixed, 2=Dual
    sign_type = sign % 3 # This is not correct for 0-indexed rashi
    # Correct mapping:
    # Movable: 0, 3, 6, 9
    # Fixed: 1, 4, 7, 10
    # Dual: 2, 5, 8, 11

    if sign in [0, 3, 6, 9]: # Movable
        # Aspects Fixed except adjacent
        fixed = [1, 4, 7, 10]
        adjacent = [(sign + 1) % 12, (sign - 1 + 12) % 12]
        return [s for s in fixed if s not in adjacent]
    elif sign in [1, 4, 7, 10]: # Fixed
        # Aspects Movable except adjacent
        movable = [0, 3, 6, 9]
        adjacent = [(sign + 1) % 12, (sign - 1 + 12) % 12]
        return [s for s in movable if s not in adjacent]
    else: # Dual
        dual = [2, 5, 8, 11]
        return [s for s in dual if s != sign]

def check_jaimini_rajayoga_advanced(chart: Any) -> List[Dict[str, Any]]:
    yogas = []
    karakas = calculate_charakarakas({p: info.longitude for p, info in chart.planets.items()})
    ak_name = karakas.get("Atmakaraka (AK) - Soul")
    amk_name = karakas.get("Amatyakaraka (AmK) - Career/Mind")
    pk_name = karakas.get("Putrakaraka (PK) - Children")
    dk_name = karakas.get("Darakaraka (DK) - Spouse")

    # 1. AK & AmK association
    if are_associated(ak_name, amk_name, chart.planets):
        yogas.append({"name": "Jaimini Rajayoga (AK-AmK)", "strength": "HIGH"})

    # 2. AK & PK association
    if are_associated(ak_name, pk_name, chart.planets):
        yogas.append({"name": "Jaimini Rajayoga (AK-PK)", "strength": "MEDIUM"})

    # 3. AmK & PK association
    if are_associated(amk_name, pk_name, chart.planets):
        yogas.append({"name": "Jaimini Rajayoga (AmK-PK)", "strength": "MEDIUM"})

    return yogas
