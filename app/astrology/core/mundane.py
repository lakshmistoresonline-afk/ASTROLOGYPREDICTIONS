from typing import Dict, List, Any
from .swe_proxy import swe

def get_mundane_indicators(jd_ut: float) -> Dict[str, Any]:
    """ indicators for global cycles."""
    results = {}

    # 1. Precession (Ayanamsa)
    results["Ayanamsa"] = swe.get_ayanamsa_ut(jd_ut)

    # 2. Great Mutation (Jupiter-Saturn cycle)
    # The last 2020 mutation was in Capricorn/Aquarius (Earth to Air transition)
    results["Jupiter-Saturn_Cycle"] = "Transitioning to Air Element Era (2020-2219)"

    # 3. Outer Planet Transits (Global Shifts)
    # Pluto in Capricorn (Deconstruction), Neptune in Pisces (Spiritual/Illusion), Uranus in Taurus (Financial Tech)
    outer_pid = {"Pluto": swe.PLUTO, "Neptune": swe.NEPTUNE, "Uranus": swe.URANUS}
    outers = {}
    for name, pid in outer_pid.items():
        res = swe.calc_ut(jd_ut, pid)
        lon = res[0]
        outers[name] = {"longitude": lon, "rashi": int(lon // 30)}

    results["outer_planet_status"] = outers

    return results
