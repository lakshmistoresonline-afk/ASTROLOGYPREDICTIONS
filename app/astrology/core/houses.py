import swisseph as swe
from typing import Dict, Any

def get_houses(jd_ut: float, lat: float, lon: float, hsys: bytes = b'W') -> Dict[str, Any]:
    """
    Calculate house cusps. Default is 'W' for Whole Sign.
    Returns cusps (1-12) and ascmc (Asc, MC, etc).
    """
    # Sidereal flag is required for Vedic houses
    flags = swe.FLG_SIDEREAL
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys, flags)
    return {
        "cusps": list(cusps[1:]),  # cusps[0] is unused in swe
        "ascendant": ascmc[0],
        "mc": ascmc[1],
        "armc": ascmc[2],
        "vertex": ascmc[3]
    }

def get_house_from_longitude(longitude: float, ascendant: float) -> int:
    """Determine house number for a given longitude using Whole Sign system."""
    asc_rashi = int(ascendant // 30)
    obj_rashi = int(longitude // 30)
    house = (obj_rashi - asc_rashi + 12) % 12 + 1
    return house

# Sign-to-Lord mapping (Standard Parashari)
RASHI_LORDS = {
    0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon",
    4: "Sun", 5: "Mercury", 6: "Venus", 7: "Mars",
    8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

def get_house_lord(house_num: int, ascendant_rashi: int) -> str:
    """Return the lord of a given house number."""
    rashi = (ascendant_rashi + house_num - 1) % 12
    return RASHI_LORDS[rashi]
