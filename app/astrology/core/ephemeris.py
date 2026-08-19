import swisseph as swe
import os
from typing import Dict, Any

# Ensure ephemeris files are found
EPHE_PATH = os.getenv("SE_EPHE_PATH", os.path.join(os.getcwd(), "ephe"))
if os.path.exists(EPHE_PATH):
    swe.set_ephe_path(EPHE_PATH)

# Default to Lahiri ayanamsa
swe.set_sid_mode(swe.SIDM_LAHIRI)

def get_julian_day(year: int, month: int, day: int, hour_utc: float) -> float:
    """Return the Julian Day in UT."""
    return swe.julday(year, month, day, hour_utc)

def get_planet_position(jd_ut: float, planet_id: int, flags: int = swe.FLG_SIDEREAL | swe.FLG_SPEED) -> Dict[str, Any]:
    """
    Get sidereal longitude, speed, and other data for a planet.
    Returns a dict with longitude, latitude, distance, and speeds.
    """
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
