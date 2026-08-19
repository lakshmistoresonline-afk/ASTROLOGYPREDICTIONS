import swisseph as swe
from ..core.ephemeris import get_planet_position
from .utils import find_event
from typing import Dict, Any

def get_karana_info(jd_ut: float) -> Dict[str, Any]:
    """Calculate Karana number and fraction elapsed at given JD."""
    sun_pos = get_planet_position(jd_ut, swe.SUN)
    moon_pos = get_planet_position(jd_ut, swe.MOON)

    diff = (moon_pos["longitude"] - sun_pos["longitude"]) % 360
    karana_num = int(diff / 6) + 1
    fraction = (diff % 6) / 6

    return {
        "number": karana_num,
        "fraction": fraction,
        "diff_deg": diff
    }

def get_karana_end_time(jd_ut: float) -> float:
    """Find the JD when the current Karana ends."""
    current_info = get_karana_info(jd_ut)
    target_angle = (current_info["number"] * 6) % 360

    def diff_func(jd):
        sun = get_planet_position(jd, swe.SUN)["longitude"]
        moon = get_planet_position(jd, swe.MOON)["longitude"]
        return (moon - sun) % 360

    # Search within next 1 day (Karana is ~12-13h)
    return find_event(jd_ut, jd_ut + 1.0, diff_func, target_angle)
