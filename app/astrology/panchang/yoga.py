import swisseph as swe
from ..core.ephemeris import get_planet_position
from .utils import find_event
from typing import Dict, Any

YOGA_SPAN = 360 / 27

def get_yoga_info(jd_ut: float) -> Dict[str, Any]:
    """Calculate Yoga number and fraction elapsed at given JD."""
    sun_pos = get_planet_position(jd_ut, swe.SUN)
    moon_pos = get_planet_position(jd_ut, swe.MOON)

    total = (sun_pos["longitude"] + moon_pos["longitude"]) % 360
    yoga_num = int(total / YOGA_SPAN) + 1
    fraction = (total % YOGA_SPAN) / YOGA_SPAN

    return {
        "number": yoga_num,
        "fraction": fraction,
        "total_deg": total
    }

def get_yoga_end_time(jd_ut: float) -> float:
    """Find the JD when the current Yoga ends."""
    current_info = get_yoga_info(jd_ut)
    target_sum = (current_info["number"] * YOGA_SPAN) % 360

    def yoga_sum_func(jd):
        sun = get_planet_position(jd, swe.SUN)["longitude"]
        moon = get_planet_position(jd, swe.MOON)["longitude"]
        return (sun + moon) % 360

    # Search within next 2 days
    return find_event(jd_ut, jd_ut + 2.0, yoga_sum_func, target_sum)
