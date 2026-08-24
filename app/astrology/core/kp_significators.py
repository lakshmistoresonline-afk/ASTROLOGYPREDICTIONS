from typing import Dict, List, Any

def calculate_kp_significators(planets: Dict[str, Any], cusps: List[float]) -> Dict[int, Dict[str, List[str]]]:
    """
    KP Significators for Houses 1-12.
    Levels:
    A: Planets in the star of occupants of the house.
    B: Planets in the house.
    C: Planets in the star of house lord.
    D: House Lord.
    """
    significators = {h: {"A": [], "B": [], "C": [], "D": []} for h in range(1, 13)}

    # 1. Map planets to their Star Lords
    # (KPInfo already contains star_lord)

    # 2. Level D: House Lords
    # (House lords from cusps)
    from .houses import get_house_lord_kp
    for h in range(1, 13):
        lord = get_house_lord_kp(h, cusps)
        significators[h]["D"].append(lord)

    # 3. Level B: Occupants
    # (We need KP house positions from cusps)
    from .houses import get_house_from_cusps
    occupants = {h: [] for h in range(1, 13)}
    for p_name, p_info in planets.items():
        h = get_house_from_cusps(p_info.longitude, cusps)
        occupants[h].append(p_name)
        significators[h]["B"].append(p_name)

    # 4. Level A: Planets in star of occupants
    for p_name, p_info in planets.items():
        star_lord = p_info.kp_details.star_lord
        # Which house does star_lord occupy?
        for h, occs in occupants.items():
            if star_lord in occs:
                significators[h]["A"].append(p_name)

    # 5. Level C: Planets in star of house lord
    for p_name, p_info in planets.items():
        star_lord = p_info.kp_details.star_lord
        for h, lord_list in significators.items():
            if star_lord in lord_list["D"]:
                significators[h]["C"].append(p_name)

    return significators
