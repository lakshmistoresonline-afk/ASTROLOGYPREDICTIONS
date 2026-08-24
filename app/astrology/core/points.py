from typing import Dict, Any, List
import math

def calculate_bhrigu_bindu(rahu_lon: float, moon_lon: float) -> float:
    """
    Bhrigu Bindu (Destiny Point): Midpoint between Rahu and Moon.
    Calculated via the shorter arc.
    """
    diff = (moon_lon - rahu_lon + 360) % 360
    if diff > 180:
        # Shorter arc is the other way
        mid = (rahu_lon + (diff - 360) / 2) % 360
    else:
        mid = (rahu_lon + diff / 2) % 360
    return mid

def calculate_sensitive_points(chart: Any) -> Dict[str, Any]:
    """
    64th Navamsha (Khara): 210 degrees from Moon/Lagna.
    22nd Drekkana: 8th house lord in D3.
    """
    planets = chart.planets
    asc_lon = chart.ascendant
    moon_lon = planets["Moon"].longitude

    points = {}

    # 1. 64th Navamsha from Lagna (approx 210 deg or 8th house Navamsha)
    points["64th Navamsha (Lagna)"] = (asc_lon + 210) % 360
    points["64th Navamsha (Moon)"] = (moon_lon + 210) % 360

    # 2. 22nd Drekkana
    # House 8 in D3
    d3 = chart.divisional_charts.get("D3", {})
    l8_name = chart.house_lords[8]
    points["22nd Drekkana Lord"] = d3.get(l8_name, "N/A")

    # 3. Bhrigu Bindu
    points["Bhrigu Bindu"] = calculate_bhrigu_bindu(planets["Rahu"].longitude, moon_lon)

    return points

def calculate_ashtakavarga_precincts(sav: List[int]) -> Dict[str, List[int]]:
    """
    Khandas (Sections):
    1st (H1-H4): Self/Effort
    2nd (H5-H8): Interaction/Karma
    3rd (H9-H12): Luck/Results
    """
    # sav is sign-indexed (0-11)
    # We need house-indexed for Khandas
    # (Simplified: using 0-3, 4-7, 8-11 as approximations)
    return {
        "Antar Khanda": sav[0:4],
        "Madhya Khanda": sav[4:8],
        "Bahir Khanda": sav[8:12]
    }
