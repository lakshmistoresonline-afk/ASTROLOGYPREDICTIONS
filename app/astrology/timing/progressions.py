from datetime import datetime, timedelta
from typing import Dict, List, Any
from ..core.datetime import datetime_to_jd
from ..core.ephemeris import get_planet_position, get_ayanamsa
import swisseph as swe

def calculate_secondary_progressions(birth_dt: datetime, target_dt: datetime, lat: float, lon: float, tz: str) -> Dict[str, float]:
    """
    Secondary Progressions: A day for a year.
    Calculates planetary positions for the 'progressed' time.
    """
    age_days = (target_dt - birth_dt).days
    # Progressed time = birth time + 1 day for every year (roughly)
    # Exact: 1 day = 1 year of life.
    # So if age is 30 years, we look at 30 days after birth.

    # age in years (float)
    age_years = age_days / 365.2425

    progressed_dt = birth_dt + timedelta(days=age_years)
    jd_prog = datetime_to_jd(progressed_dt, tz)

    results = {}
    for name, pid in [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS), ("Mercury", swe.MERCURY),
                      ("Jupiter", swe.JUPITER), ("Venus", swe.VENUS), ("Saturn", swe.SATURN)]:
        pos = get_planet_position(jd_prog, pid)
        results[name] = pos["longitude"]

    return results

def calculate_solar_arc_directions(natal_planets: Dict[str, Any], birth_dt: datetime, target_dt: datetime, tz: str) -> Dict[str, float]:
    """
    Solar Arc Directions: Every planet moves by the same arc as the Sun.
    """
    age_years = (target_dt - birth_dt).days / 365.2425

    jd_birth = datetime_to_jd(birth_dt, tz)
    jd_target_prog = jd_birth + age_years # 1 day per year

    sun_birth = get_planet_position(jd_birth, swe.SUN)["longitude"]
    sun_prog = get_planet_position(jd_target_prog, swe.SUN)["longitude"]

    solar_arc = (sun_prog - sun_birth + 360) % 360

    results = {}
    for name, p_info in natal_planets.items():
        if hasattr(p_info, "longitude"):
            results[name] = (p_info.longitude + solar_arc) % 360

    return results
