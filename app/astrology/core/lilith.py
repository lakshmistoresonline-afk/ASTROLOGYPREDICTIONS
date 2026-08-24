import swisseph as swe
from typing import Dict, Any

def get_lilith_positions(jd_ut: float) -> Dict[str, Dict[str, Any]]:
    """Calculate Mean and True Lilith positions."""
    results = {}

    # 1. Mean Lilith (Apogee)
    res_m = swe.calc_ut(jd_ut, 12) # 12 is Mean Lilith
    lon_m = res_m[0]
    results["Mean Lilith"] = {
        "longitude": lon_m,
        "rashi": int(lon_m // 30),
        "interpretation": "Represents the primal, untamed feminine and hidden desires."
    }

    # 2. True Lilith (Osculating)
    res_t = swe.calc_ut(jd_ut, 13) # 13 is True Lilith
    lon_t = res_t[0]
    results["True Lilith"] = {
        "longitude": lon_t,
        "rashi": int(lon_t // 30),
        "interpretation": "Represents the exact, intense manifestation of the Lilith archetype."
    }

    return results
