import swisseph as swe
from ..core.ephemeris import get_planet_position
from .utils import find_event
from typing import Dict, Any

NAK_SPAN = 360 / 27

def get_nakshatra_info(jd_ut: float) -> Dict[str, Any]:
    """Calculate Nakshatra number and fraction elapsed at given JD."""
    moon_pos = get_planet_position(jd_ut, swe.MOON)
    lon = moon_pos["longitude"]

    nak_num = int(lon / NAK_SPAN) + 1
    fraction = (lon % NAK_SPAN) / NAK_SPAN
    pada = int((lon % NAK_SPAN) / (NAK_SPAN / 4)) + 1

    return {
        "number": nak_num,
        "fraction": fraction,
        "pada": pada,
        "longitude": lon
    }

def get_nakshatra_end_time(jd_ut: float) -> float:
    """Find the JD when the current Nakshatra ends."""
    current_info = get_nakshatra_info(jd_ut)
    target_lon = (current_info["number"] * NAK_SPAN) % 360

    def moon_lon_func(jd):
        return get_planet_position(jd, swe.MOON)["longitude"]

    # Search within the next 2 days
    return find_event(jd_ut, jd_ut + 2.0, moon_lon_func, target_lon)
