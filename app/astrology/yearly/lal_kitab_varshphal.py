from typing import Dict, List, Any

# Lal Kitab Year Lord (Not same as Varshaphala)
# Based on the house occupied by a planet in the natal chart and the current year.

def get_lal_kitab_year_lord(natal_planets: Dict[str, Any], current_year: int, birth_year: int) -> str:
    age = current_year - birth_year + 1
    # Circular order of planets for years:
    # 1-Jupiter, 2-Sun, 3-Moon, 4-Venus, 5-Mars, 6-Mercury, 7-Saturn, 8-Rahu, 9-Ketu
    ORDER = ["Jupiter", "Sun", "Moon", "Venus", "Mars", "Mercury", "Saturn", "Rahu", "Ketu"]
    return ORDER[(age - 1) % 9]

def analyze_lal_kitab_yearly_houses(natal_planets: Dict[str, Any], age: int) -> Dict[str, int]:
    """
    In Lal Kitab, planets shift houses every year in a specific cycle.
    Placeholder for complex house-rotation logic.
    """
    results = {}
    for p_name, p_info in natal_planets.items():
        natal_h = getattr(p_info, "house", 1)
        # Shift formula: (Natal House + Age - 1) % 12 + 1
        curr_h = (natal_h + age - 1) % 12
        if curr_h == 0: curr_h = 12
        results[p_name] = curr_h
    return results
