from typing import List, Dict, Any
from .detector import _get

def check_nadi_signatures(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Nadi Astrology signatures (Bhrigu Nandi Nadi).
    Focuses on planetary combinations (Yoga) across 1-5-9 and 1-7 signs.
    """
    results = []

    # Sign mapping
    sign_planets = {i: [] for i in range(12)}
    for p_name, p_info in planets.items():
        if p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            r = _get(p_info, "rashi")
            sign_planets[r].append(p_name)

    def get_associated(p_name: str) -> List[str]:
        p_info = planets.get(p_name)
        if not p_info: return []
        r = _get(p_info, "rashi")

        # 1-5-9 (Trine)
        trines = [r, (r + 4) % 12, (r + 8) % 12]
        # 7 (Opposition)
        opp = (r + 6) % 12
        # 2-12 (Adjacent)
        adj = [(r + 1) % 12, (r + 11) % 12]

        assoc = []
        for s in trines + [opp] + adj:
            for other in sign_planets[s]:
                if other != p_name:
                    assoc.append(other)
        return list(set(assoc))

    # 1. Career (Saturn)
    sat_assoc = get_associated("Saturn")
    if "Mercury" in sat_assoc and "Venus" in sat_assoc:
        results.append({"name": "Nadi: Business Excellence", "interpretation": "Saturn-Mercury-Venus combination suggests huge success in commercial ventures or creative administration."})
    elif "Mercury" in sat_assoc:
        results.append({"name": "Nadi: Intellectual Career", "interpretation": "Saturn-Mercury suggests success in writing, teaching, or analytical roles."})

    if "Jupiter" in sat_assoc:
         results.append({"name": "Nadi: Dharma-Karmadhipati", "interpretation": "Saturn-Jupiter combination indicates a highly respected career with leadership and wisdom."})

    # 2. Wealth & Marriage (Venus)
    ven_assoc = get_associated("Venus")
    if "Jupiter" in ven_assoc:
         results.append({"name": "Nadi: Luxury & Abundance", "interpretation": "Venus-Jupiter suggests immense wealth and a happy, virtuous partner."})
    if "Mars" in ven_assoc:
         results.append({"name": "Nadi: Passionate Bond", "interpretation": "Venus-Mars indicates a dynamic, passionate, but sometimes impulsive relationship energy."})

    # 3. Life Purpose (Jupiter)
    jup_assoc = get_associated("Jupiter")
    if "Mars" in jup_assoc and "Ketu" in jup_assoc:
        results.append({"name": "Nadi: Spiritual Warrior", "interpretation": "Jupiter-Mars-Ketu suggests deep spiritual insights combined with disciplined action, often seen in healers or monks."})
    elif "Mars" in jup_assoc:
        results.append({"name": "Nadi: Guru-Mangala", "interpretation": "Jupiter-Mars combination gives land, property, and commanding authority."})

    # 4. Obstacles (Rahu/Ketu)
    if "Moon" in get_associated("Rahu"):
        results.append({"name": "Nadi: Mental Shadow", "interpretation": "Rahu-Moon suggests illusion, deep imagination, or periods of emotional confusion."})

    return results
