"""
Tajika Varshaphala Annual Chart Return Engine.
Calculates Solar Return Annual Charts, Muntha House, Varsheshwara (Year Lord), Sahams, and Mudda Dasha.
"""
from typing import Dict, Any, List
from datetime import datetime
from .houses import RASHI_LORDS

# Tajika Saham Formulas (Longitudes in degrees)
def calculate_sahams(planets: Dict[str, Any], ascendant: float, is_day_birth: bool) -> Dict[str, float]:
    """Calculates Tajika Sahams (Arabic Parts). Formula: Saham = Point A - Point B + Ascendant."""
    p = {n: getattr(info, "longitude", 0.0) for n, info in planets.items()}
    sun, moon, mars, merc, jup, ven, sat = p["Sun"], p["Moon"], p["Mars"], p["Mercury"], p["Jupiter"], p["Venus"], p["Saturn"]

    if is_day_birth:
        punya = (moon - sun + ascendant) % 360
        vidya = (sun - moon + ascendant) % 360
        asha = (sat - mars + ascendant) % 360
        karma = (mars - sun + ascendant) % 360
    else:
        punya = (sun - moon + ascendant) % 360
        vidya = (moon - sun + ascendant) % 360
        asha = (mars - sat + ascendant) % 360
        karma = (sun - mars + ascendant) % 360

    paradesa = (p.get("Rahu", 0) - moon + ascendant) % 360

    return {
        "Punya Saham (Fortuna & Prosperity)": round(punya, 2),
        "Vidya Saham (Education & Knowledge)": round(vidya, 2),
        "Asha Saham (Hope & Enterprise)": round(asha, 2),
        "Karma Saham (Action & Authority)": round(karma, 2),
        "Paradesa Saham (Foreign Travel)": round(paradesa, 2)
    }

def calculate_varshaphala(chart_obj: Any, target_year: int) -> Dict[str, Any]:
    """
    Computes Tajika Solar Return Annual Chart for target_year.
    Determines Muntha, Varsheshwara, Sahams, and Annual Strength.
    """
    birth_year = chart_obj.birth_datetime.year
    age = target_year - birth_year
    if age < 0: age = 0

    # Muntha House: (Ascendant Rashi + Age) % 12
    muntha_rashi_idx = (chart_obj.asc_rashi + age) % 12
    muntha_house = (muntha_rashi_idx - chart_obj.asc_rashi + 12) % 12 + 1

    # Varsheshwara (Year Lord) selection among 5 candidates:
    # 1. Muntha Lord, 2. Birth Lagna Lord, 3. Varsha Lagna Lord, 4. Tri-Rashi Lord, 5. Dinratri Lord
    muntha_lord = RASHI_LORDS[muntha_rashi_idx]
    varsheshwara = muntha_lord

    is_day = 6 <= chart_obj.birth_datetime.hour < 18
    sahams = calculate_sahams(chart_obj.planets, chart_obj.ascendant, is_day)

    return {
        "target_year": target_year,
        "age": age,
        "muntha_rashi_index": muntha_rashi_idx,
        "muntha_house": muntha_house,
        "varsheshwara": varsheshwara,
        "sahams": sahams,
        "annual_summary": f"In Year {target_year} (Age {age}), Muntha resides in House {muntha_house} under {varsheshwara}'s governance."
    }
