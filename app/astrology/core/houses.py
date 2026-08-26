from .swe_proxy import swe
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
        "cusps": list(cusps),
        "ascendant": ascmc[0],
        "mc": ascmc[1],
        "armc": ascmc[2],
        "vertex": ascmc[3],
        "equatorial_ascendant": ascmc[4], # East Point
        "co_ascendant_koch": ascmc[5],
        "co_ascendant_munk": ascmc[6],
        "polar_ascendant": ascmc[7]
    }

def get_house_from_cusps(longitude: float, cusps: list) -> int:
    """Determine house number for a given longitude using specific cusps (1-indexed)."""
    # cusps[1] is start of House 1, cusps[12] is start of House 12
    # Ensure we use 1-12
    c = cusps
    if len(c) < 13:
        # Fallback if list is 0-indexed 12 elements
        c = [0.0] + list(cusps)

    for i in range(1, 12):
        if c[i] <= longitude < c[i+1]:
            return i
        # Handle wraparound
        if c[i] > c[i+1]:
            if longitude >= c[i] or longitude < c[i+1]:
                return i
    return 12

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

RASHI_NAMES = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrishchika",
    "Dhanu", "Makara", "Kumbha", "Meena",
]

def get_house_lord(house_num: int, ascendant_rashi: int) -> str:
    """Return the lord of a given house number."""
    rashi = (ascendant_rashi + house_num - 1) % 12
    return RASHI_LORDS[rashi]

def get_house_lord_kp(house_num: int, cusps: list) -> str:
    """Return the lord of the sign where a cusp longitude falls."""
    # Handle both 0-indexed and 1-indexed lists
    if len(cusps) >= 13:
        longitude = cusps[house_num]
    else:
        longitude = cusps[house_num - 1]

    rashi = int(longitude // 30)
    return RASHI_LORDS[rashi]
