from typing import Dict, List, Any

# Vedha Positions: For each planet's auspicious transit house from Moon,
# there is a corresponding 'Vedha' house that blocks it.
# Auspicious: (House, Vedha House)
VEDHA_MAP = {
    "Sun": {3: 9, 6: 12, 10: 4, 11: 5},
    "Moon": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
    "Mars": {3: 12, 6: 9, 11: 5},
    "Mercury": {2: 5, 4: 3, 6: 9, 8: 1, 10: 7, 11: 12},
    "Jupiter": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
    "Venus": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 3, 12: 6},
    "Saturn": {3: 12, 6: 9, 11: 5}
}

def calculate_transit_vedha(natal_moon_rashi: int, transit_planets: Dict[str, float]) -> Dict[str, List[str]]:
    """
    Check if an auspicious transit is blocked by Vedha.
    Note: Sun and Saturn don't obstruct each other. Moon has no Vedha.
    """
    results = {}

    # Rashi of transit planets
    transit_rashis = {p: int(lon // 30) for p, lon in transit_planets.items()}

    for p_name, auspicious_houses in VEDHA_MAP.items():
        if p_name not in transit_rashis: continue

        t_rashi = transit_rashis[p_name]
        # Transit house from Moon
        t_house = (t_rashi - natal_moon_rashi + 12) % 12 + 1

        if t_house in auspicious_houses:
            v_house = auspicious_houses[t_house]
            # Sign corresponding to v_house from Moon
            v_rashi = (natal_moon_rashi + v_house - 1) % 12

            # Is any planet in the Vedha rashi?
            obstructors = []
            for other_p, other_r in transit_rashis.items():
                if other_p == p_name: continue

                # Exceptions
                if p_name == "Sun" and other_p == "Saturn": continue
                if p_name == "Saturn" and other_p == "Sun": continue

                if other_r == v_rashi:
                    obstructors.append(other_p)

            if obstructors:
                results[p_name] = obstructors

    return results
