import swisseph as swe
import os
from typing import Dict, Any
from functools import lru_cache

# Ensure ephemeris files are found
EPHE_PATH = os.getenv("SE_EPHE_PATH", os.path.join(os.getcwd(), "ephe"))
if os.path.exists(EPHE_PATH):
    swe.set_ephe_path(EPHE_PATH)

# Default to Lahiri ayanamsa
_sid_mode = swe.SIDM_LAHIRI
swe.set_sid_mode(_sid_mode)

def set_ayanamsa_mode(mode: int):
    """Set the global sidereal mode (Lahiri, Raman, etc)."""
    global _sid_mode
    _sid_mode = mode
    swe.set_sid_mode(mode)

# Global flag to enable/disable topocentric precision
_USE_TOPO = False

def set_topocentric(lat: float, lon: float, alt: float = 0.0):
    """Set the topocentric location for precision calculations."""
    global _USE_TOPO
    swe.set_topo(lon, lat, alt)
    _USE_TOPO = True

def get_julian_day(year: int, month: int, day: int, hour_utc: float) -> float:
    """Return the Julian Day in UT."""
    return swe.julday(year, month, day, hour_utc)

@lru_cache(maxsize=1024)
def get_planet_position(jd_ut: float, planet_id: int, flags: int = None) -> Dict[str, Any]:
    """
    Get sidereal longitude, speed, and other data for a planet.
    Uses LRU cache for performance.
    """
    if flags is None:
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Try with topocentric if requested, but fallback if not set
    try:
        res, ret_flag = swe.calc_ut(jd_ut, planet_id, flags | (swe.FLG_TOPOCTR if _USE_TOPO else 0))
    except swe.Error:
        # Fallback to geocentric if topocentric fails (e.g. position not set in this thread)
        res, ret_flag = swe.calc_ut(jd_ut, planet_id, flags)

    return {
        "longitude": res[0],
        "latitude": res[1],
        "distance": res[2],
        "speed_long": res[3],
        "speed_lat": res[4],
        "speed_dist": res[5],
        "is_retrograde": res[3] < 0
    }

def get_ayanamsa(jd_ut: float) -> float:
    """Return the ayanamsa for the given Julian Day."""
    return swe.get_ayanamsa_ut(jd_ut)
