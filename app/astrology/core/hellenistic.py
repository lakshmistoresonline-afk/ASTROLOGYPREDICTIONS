from typing import Dict, List, Any

def get_annual_profection(asc_rashi: int, age: int) -> int:
    """Annual Profection: 1 sign per year."""
    # Age 0 = Lagna sign (asc_rashi)
    # Age 1 = 2nd house sign
    return (asc_rashi + age) % 12

def calculate_greek_lots(planets: Dict[str, Any], asc_lon: float, is_day: bool) -> Dict[str, float]:
    """
    Hellenistic Lots (Arabic Parts).
    Fortune (Tyche): Asc + Moon - Sun (Day), Asc + Sun - Moon (Night)
    Spirit (Daimon): Asc + Sun - Moon (Day), Asc + Moon - Sun (Night)
    """
    sun = planets["Sun"].longitude
    moon = planets["Moon"].longitude

    def calc(a, b, c): return (a - b + c) % 360

    lots = {}
    if is_day:
        lots["Lot of Fortune"] = calc(asc_lon, sun, moon)
        lots["Lot of Spirit"] = calc(asc_lon, moon, sun)
    else:
        lots["Lot of Fortune"] = calc(asc_lon, moon, sun)
        lots["Lot of Spirit"] = calc(asc_lon, sun, moon)

    # Lot of Eros: Asc + Spirit - Fortune (Day), Asc + Fortune - Spirit (Night)
    if is_day:
        lots["Lot of Eros"] = calc(asc_lon, lots["Lot of Fortune"], lots["Lot of Spirit"])
    else:
        lots["Lot of Eros"] = calc(asc_lon, lots["Lot of Spirit"], lots["Lot of Fortune"])

    return lots

# Egyptian Bounds (Terms)
# Different systems exist, using Egyptian as standard
BOUNDS = {
    0: [(6, "Jupiter"), (12, "Venus"), (20, "Mercury"), (25, "Mars"), (30, "Saturn")], # Aries
    1: [(8, "Venus"), (14, "Mercury"), (22, "Jupiter"), (27, "Saturn"), (30, "Mars")], # Taurus
    2: [(6, "Mercury"), (12, "Jupiter"), (17, "Venus"), (24, "Mars"), (30, "Saturn")], # Gemini
    3: [(7, "Mars"), (13, "Venus"), (19, "Mercury"), (26, "Jupiter"), (30, "Saturn")], # Cancer
    4: [(6, "Jupiter"), (11, "Venus"), (18, "Saturn"), (24, "Mercury"), (30, "Mars")], # Leo
    5: [(7, "Mercury"), (17, "Venus"), (21, "Jupiter"), (28, "Saturn"), (30, "Mars")], # Virgo
    6: [(6, "Saturn"), (14, "Venus"), (21, "Jupiter"), (28, "Mercury"), (30, "Mars")], # Libra
    7: [(7, "Mars"), (11, "Venus"), (19, "Mercury"), (24, "Jupiter"), (30, "Saturn")], # Scorpio
    8: [(12, "Jupiter"), (17, "Venus"), (21, "Mercury"), (26, "Saturn"), (30, "Mars")], # Sagittarius
    9: [(7, "Mercury"), (14, "Jupiter"), (22, "Venus"), (26, "Saturn"), (30, "Mars")], # Capricorn
    10: [(7, "Mercury"), (13, "Venus"), (20, "Jupiter"), (25, "Mars"), (30, "Saturn")], # Aquarius
    11: [(12, "Venus"), (16, "Jupiter"), (19, "Mercury"), (28, "Mars"), (30, "Saturn")] # Pisces
}

def get_egyptian_bound(rashi: int, degree: float) -> str:
    for limit, lord in BOUNDS[rashi]:
        if degree < limit:
            return lord
    return "Unknown"
