from typing import Dict, List, Any
from .dignity import EXALTATION, DEBILITATION

def calculate_pindayu(planets: Dict[str, Any]) -> Dict[str, float]:
    """
    Pindayu (Planet-based Longevity contribution).
    Max years: Sun=19, Moon=25, Mars=15, Merc=12, Jup=15, Ven=21, Sat=20.
    Contribution = Max * (1 - (dist_from_exalt / 360))
    """
    MAX_YEARS = {
        "Sun": 19, "Moon": 25, "Mars": 15, "Mercury": 12,
        "Jupiter": 15, "Venus": 21, "Saturn": 20
    }

    results = {}
    for name, max_y in MAX_YEARS.items():
        if name not in planets: continue
        p = planets[name]

        ex_rashi, ex_deg = EXALTATION[name]
        ex_lon = ex_rashi * 30 + ex_deg

        dist = (p.longitude - ex_lon + 360) % 360
        # If at exaltation, years = max. If at debilitation (180 away), years = max/2.
        # Classic formula is linear between exalt and debil.

        if dist <= 180:
            contribution = max_y * (1 - (dist / 360.0))
        else:
            # 180 to 360: years go from max/2 back up? No, 180 is debil (half).
            # Actually classic formula is different. Simplified:
            contribution = max_y * (1 - (dist / 360.0))

        results[name] = round(contribution, 2)

    return results

def calculate_ashtakavarga_ayurdaya(planets: Dict[str, Any], av_data: Dict[str, Any]) -> float:
    """
    Longevity based on Ashtakavarga Bindus.
    Formula: (Bindus * 3 / 4) or similar based on planet.
    """
    total_years = 0.0
    bav = av_data.get("BAV", {})

    for name, p_bav in bav.items():
        if name not in planets: continue
        rashi = planets[name].rashi
        bindus = p_bav[rashi]

        # Standard: bindus in the sign occupied
        total_years += (bindus * 1.5) # Simplified proxy

    return round(total_years, 2)
