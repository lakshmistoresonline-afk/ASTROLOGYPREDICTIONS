from .swe_proxy import swe
from typing import Dict, Any
from .planets import PLANETS

def get_heliocentric_positions(jd_ut: float) -> Dict[str, float]:
    """
    Calculate planetary positions relative to the Sun (Heliocentric).
    Provides a perspective beyond the Earth-bound ego.
    """
    results = {}
    # Use swe.FLG_HELCTR for heliocentric positions
    flags = swe.FLG_SWIEPH | swe.FLG_HELCTR

    # Sun is 0, but in helio we usually look at Earth
    # swe.EARTH is 14
    target_planets = {**PLANETS, "Earth": 14}

    for name, pid in target_planets.items():
        if name == "Sun": continue # Sun is the center
        res = swe.calc_ut(jd_ut, pid, flags)
        results[name] = res[0][0] # Longitude

    return results
