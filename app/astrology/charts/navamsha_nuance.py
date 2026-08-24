from typing import Dict, List, Any

# Pushkar Navamsha degrees in each Rashi
PUSHKAR_NAVAMSHA = {
    # Fire signs (0, 4, 8): 21° to 23° 20' (7th Navamsha - Libra) and 26° 40' to 30° (9th - Sag)
    "Fire": [(20.0, 23.333), (26.666, 30.0)],
    # Earth signs (1, 5, 9): 3° 20' to 6° 40' (2nd - Taurus) and 13° 20' to 16° 40' (5th - Virgo)
    "Earth": [(3.333, 6.666), (13.333, 16.666)],
    # Air signs (2, 6, 10): 16° 40' to 20° (6th - Pisces) and 23° 20' to 26° 40' (8th - Taurus)
    "Air": [(16.666, 20.0), (23.333, 26.666)],
    # Water signs (3, 7, 11): 0° to 3° 20' (1st - Cancer) and 6° 40' to 10° (3rd - Virgo)
    "Water": [(0.0, 3.333), (6.666, 10.0)]
}

def is_pushkar_navamsha(rashi: int, degree: float) -> bool:
    """Check if a planet's position is in Pushkar Navamsha."""
    group = "Fire" if rashi in [0, 4, 8] else \
            "Earth" if rashi in [1, 5, 9] else \
            "Air" if rashi in [2, 6, 10] else "Water"

    ranges = PUSHKAR_NAVAMSHA[group]
    for start, end in ranges:
        if start <= degree < end:
            return True
    return False

def calculate_navamsha_nuances(planets: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Identify Vargottama, Pushkar Navamsha, Ashtamamsha (8th from D1), Nidhanamsha (64th from D1).
    """
    nuances = {p: [] for p in planets}

    for name, p in planets.items():
        # 1. Pushkar Navamsha
        if is_pushkar_navamsha(p.rashi, p.degree):
            nuances[name].append("Pushkar Navamsha (Extremely Auspicious)")

        # 2. Vargottama (handled in PlanetInfo, but can verify here)
        if p.is_vargottama:
            nuances[name].append("Vargottama (Strength)")

        # 3. Ashtamamsha (Planet in 8th house in D9 relative to D1 sign)
        # (Usually means Navamsha Rashi is 8 signs away from D1 Rashi)
        if p.navamsa_rashi is not None:
            dist = (p.navamsa_rashi - p.rashi + 12) % 12
            if dist == 7: # 8th sign
                nuances[name].append("Ashtamamsha (Instability)")

    return nuances
