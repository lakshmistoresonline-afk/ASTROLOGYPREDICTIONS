import swisseph as swe
from datetime import datetime, date
from .ephemeris import get_planet_position, get_julian_day
from ..panchang.utils import find_event
from typing import Dict, Any

def get_solar_return_jd(natal_jd: float, target_year: int) -> float:
    """Find the exact JD when Sun returns to natal longitude."""
    # 1. Get natal sun position
    natal_sun = get_planet_position(natal_jd, swe.SUN)
    target_lon = natal_sun["longitude"]

    # 2. Approximate return time
    # Convert natal_jd to y/m/d to find birthday
    y, m, d, h = swe.revjul(natal_jd)
    # Search around the target birthday
    search_start = get_julian_day(target_year, m, d, h) - 2.0
    search_end = search_start + 4.0

    def sun_lon_func(jd):
        return get_planet_position(jd, swe.SUN)["longitude"]

    return find_event(search_start, search_end, sun_lon_func, target_lon)

def calculate_muntha(natal_asc_rashi: int, age_years: int) -> int:
    """Calculate the Muntha (Yearly point) rashi."""
    return (natal_asc_rashi + age_years) % 12

def get_varshaphala_data(birth_dt: datetime, natal_asc_rashi: int, target_year: int) -> Dict[str, Any]:
    # Calculate age
    age = target_year - birth_dt.year
    muntha_rashi = calculate_muntha(natal_asc_rashi, age)

    return {
        "age": age,
        "muntha_rashi": muntha_rashi,
        "muntha_house": (muntha_rashi - natal_asc_rashi + 12) % 12 + 1
    }
