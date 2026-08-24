from typing import Dict, List, Any

# 12 Palaces in Zi Wei Dou Shu
PALACES = [
    "Self", "Siblings", "Marriage", "Children", "Wealth",
    "Health", "Travel", "Friends", "Career", "Property",
    "Happiness", "Parents"
]

def calculate_zi_wei_palaces(lunar_month: int, lunar_day: int, hour_idx: int) -> Dict[str, str]:
    """
    Simplified Zi Wei Dou Shu palace mapping.
    hour_idx: 0 (Zi) to 11 (Hai)
    """
    # Self Palace position
    # Formula: (Month - Hour + 12) % 12
    self_pos = (lunar_month - hour_idx + 12) % 12

    palace_map = {}
    for i in range(12):
        # Palaces go counter-clockwise
        p_idx = (self_pos - i + 12) % 12
        palace_map[PALACES[i]] = f"Position {p_idx + 1}"

    return {
        "self_palace": f"Position {self_pos + 1}",
        "palace_distribution": palace_map,
        "emperor_star": _get_zi_wei_star_pos(lunar_day)
    }

def _get_zi_wei_star_pos(day: int) -> str:
    # Emperor Star (Zi Wei) position based on lunar day and element
    # Simplified placeholder
    return f"Calculated based on day {day}"
