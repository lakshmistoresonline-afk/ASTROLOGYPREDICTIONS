from typing import Dict, List, Any
from ..charts.ashtakavarga import BINDU_TABLES

# Kakshya order: Sat, Jup, Mars, Sun, Ven, Merc, Moon, Lagna
KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"]

def is_kakshya_active(planet: str, rashi: int, degree: float, b_rashis: Dict[str, int]) -> bool:
    """
    Check if a transit planet is in an 'active' Kakshya.
    Active means the lord of the 3°45' segment contributes a bindu in the planet's BAV.
    """
    # 1. Determine which Kakshya (0-7)
    k_idx = int(degree / 3.75)
    if k_idx > 7: k_idx = 7

    k_lord = KAKSHYA_LORDS[k_idx]

    # 2. Check if k_lord contributes a bindu for 'planet' in 'rashi'
    # b_rashis: natal positions {planet_name: rashi_index}

    # Get relative house of k_lord from natal position
    natal_rashi = b_rashis.get(k_lord)
    if natal_rashi is None: return False

    # Sign index being transited is 'rashi'
    # Relative house from natal
    rel_house = (rashi - natal_rashi + 12) % 12 + 1

    # Bindu table for 'planet' showing contributions from 'k_lord'
    table = BINDU_TABLES.get(planet, {})
    houses = table.get(k_lord, [])

    return rel_house in houses

def get_planet_kakshya_status(planet: str, rashi: int, degree: float, b_rashis: Dict[str, int]) -> Dict[str, Any]:
    k_idx = int(degree / 3.75)
    k_lord = KAKSHYA_LORDS[k_idx]
    active = is_kakshya_active(planet, rashi, degree, b_rashis)

    return {
        "kakshya_lord": k_lord,
        "is_active": active,
        "degree_in_kakshya": round(degree % 3.75, 2)
    }
