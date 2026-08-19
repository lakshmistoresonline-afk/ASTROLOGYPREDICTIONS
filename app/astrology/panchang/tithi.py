import swisseph as swe
from ..core.ephemeris import get_planet_position
from .utils import find_event
from typing import Dict, Any

def get_tithi_info(jd_ut: float) -> Dict[str, Any]:
    """Calculate Tithi number and fraction elapsed at given JD."""
    sun_pos = get_planet_position(jd_ut, swe.SUN)
    moon_pos = get_planet_position(jd_ut, swe.MOON)

    diff = (moon_pos["longitude"] - sun_pos["longitude"]) % 360
    tithi_num = int(diff / 12) + 1
    fraction = (diff % 12) / 12

    return {
        "number": tithi_num,
        "fraction": fraction,
        "diff_deg": diff
    }

def get_tithi_end_time(jd_ut: float) -> float:
    """Find the JD when the current Tithi ends."""
    current_info = get_tithi_info(jd_ut)
    target_angle = (current_info["number"] * 12) % 360

    def diff_func(jd):
        sun = get_planet_position(jd, swe.SUN)["longitude"]
        moon = get_planet_position(jd, swe.MOON)["longitude"]
        return (moon - sun) % 360

    # Search within the next 2 days (max tithi duration is ~26h)
    return find_event(jd_ut, jd_ut + 2.0, diff_func, target_angle)
