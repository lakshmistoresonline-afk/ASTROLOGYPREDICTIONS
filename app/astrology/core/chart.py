from typing import Dict, Any
from .ephemeris import get_planet_position, get_ayanamsa
from .datetime import datetime_to_jd
from .houses import get_houses, get_house_from_longitude
from .planets import PLANETS
from ..strength.dignity import get_dignity
from ..strength.functional import get_functional_status
from ..strength.aspects import get_graha_drishti
from ..charts.divisional import get_varga_chart
from datetime import datetime

def calculate_chart_data(birth_dt: datetime, lat: float, lon: float, tz_str: str) -> Dict[str, Any]:
    """Calculate all raw astrological data for a birth moment."""
    jd_ut = datetime_to_jd(birth_dt, tz_str)

    # 1. Houses and Lagna
    house_data = get_houses(jd_ut, lat, lon)
    ascendant = house_data["ascendant"]
    asc_rashi = int(ascendant // 30)

    # 2. Planets
    planets = {}
    planets_lon = {}
    for name, pid in PLANETS.items():
        pos = get_planet_position(jd_ut, pid)
        lon = pos["longitude"]
        planets_lon[name] = lon
        rashi = int(lon // 30)
        deg = lon % 30

        planets[name] = {
            "longitude": lon,
            "rashi": rashi,
            "degree": deg,
            "house": get_house_from_longitude(lon, ascendant),
            "is_retrograde": pos["is_retrograde"],
            "dignity": get_dignity(name, rashi, deg),
            "drishti": get_graha_drishti(name, rashi)
        }

    # Ketu logic
    rahu_lon = planets["Rahu"]["longitude"]
    ketu_lon = (rahu_lon + 180) % 360
    ketu_rashi = int(ketu_lon // 30)
    planets["Ketu"] = {
        "longitude": ketu_lon,
        "rashi": ketu_rashi,
        "degree": ketu_lon % 30,
        "house": get_house_from_longitude(ketu_lon, ascendant),
        "is_retrograde": True,
        "dignity": get_dignity("Ketu", ketu_rashi, ketu_lon % 30),
        "drishti": get_graha_drishti("Ketu", ketu_rashi)
    }
    planets_lon["Ketu"] = ketu_lon

    # 3. Functional Status
    functional_status = get_functional_status(asc_rashi)
    for p, status in functional_status.items():
        if p in planets:
            planets[p]["functional_status"] = status

    # 4. Divisional Charts (D9, D10)
    d9 = get_varga_chart(planets_lon, ascendant, 9)
    d10 = get_varga_chart(planets_lon, ascendant, 10)

    return {
        "jd_ut": jd_ut,
        "ascendant": ascendant,
        "asc_rashi": asc_rashi,
        "houses": house_data["cusps"],
        "planets": planets,
        "ayanamsa": get_ayanamsa(jd_ut),
        "divisional": {
            "D9": d9,
            "D10": d10
        }
    }
