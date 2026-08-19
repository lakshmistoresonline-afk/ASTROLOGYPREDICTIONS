from typing import List, Dict, Optional

# Vedha mapping: { TransitHouse: VedhaHouse }
# If a planet is in TransitHouse, a planet in VedhaHouse blocks it.
# Note: House 11-3 means Transit in 11 is blocked by planet in 3.
VEDHA_MAP = {
    "Sun": {3: 9, 6: 12, 10: 4, 11: 5, 4: 10, 5: 11, 9: 3, 12: 6},
    "Moon": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8, 2: 7, 4: 10, 5: 1, 8: 11, 9: 3, 12: 6},
    "Mars": {3: 12, 6: 9, 11: 5, 5: 11, 9: 6, 12: 3},
    "Mercury": {2: 5, 4: 3, 6: 9, 8: 1, 10: 7, 11: 12, 1: 8, 3: 4, 5: 2, 7: 10, 9: 6, 12: 11},
    "Jupiter": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8, 3: 7, 4: 5, 8: 11, 10: 9, 12: 2},
    "Venus": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 11, 9: 5, 10: 4, 11: 3, 12: 6, 6: 12, 7: 2},
    "Saturn": {3: 12, 6: 9, 11: 5, 5: 11, 9: 6, 12: 3}
}

def check_vedha(transit_planets: Dict, natal_houses: Dict) -> List[Dict]:
    """
    Check for Vedha (obstructions) in current transits.
    transit_planets: { name: { house_from_moon: int } }
    natal_houses: { house_num: [planet_names] } - Houses from natal moon
    """
    results = []

    # 1. Identify all planets present in houses from natal moon
    occupied_houses = {h for h, occupants in natal_houses.items() if occupants}

    for p_name, p_data in transit_planets.items():
        if p_name not in VEDHA_MAP: continue

        t_house = p_data.get("house_from_moon")
        if not t_house: continue

        v_house = VEDHA_MAP[p_name].get(t_house)
        if v_house and v_house in occupied_houses:
            # Special case exceptions
            # Moon & Mercury: No Vedha between them
            # Sun & Saturn: No Vedha between them (Father & Son)
            obstruction = False
            for occ in natal_houses[v_house]:
                if p_name == "Sun" and occ == "Saturn": continue
                if p_name == "Saturn" and occ == "Sun": continue
                if p_name == "Moon" and occ == "Mercury": continue
                if p_name == "Mercury" and occ == "Moon": continue
                obstruction = True
                break

            if obstruction:
                results.append({
                    "planet": p_name,
                    "transit_house": t_house,
                    "vedha_house": v_house,
                    "obstructed_by": natal_houses[v_house]
                })

    return results
