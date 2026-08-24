from typing import Dict, Any, List

def calculate_bcp_activation(natal_asc_rashi: int, birth_year: int, target_year: int) -> Dict[str, Any]:
    """
    Bhrigu Chakra Paddhati (BCP):
    Each house is activated for one year.
    Cycle 1: 0-12 years, Cycle 2: 12-24, etc.
    """
    age = target_year - birth_year
    if age < 0: age = 0

    # Active house (1-indexed)
    active_house = (age % 12) + 1

    # Active rashi
    active_rashi = (natal_asc_rashi + active_house - 1) % 12

    return {
        "age": age,
        "active_house": active_house,
        "active_rashi": active_rashi,
        "cycle": (age // 12) + 1
    }
