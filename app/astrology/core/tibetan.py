from typing import Dict, Any

def calculate_tibetan_mewa(year: int) -> Dict[str, Any]:
    """
    Tibetan Mewa (Magic Square number).
    Cycle of 9 years.
    """
    # 2000 was 9 Purple
    mewa = 9 - ((year - 2000) % 9)
    if mewa <= 0: mewa += 9

    MEWA_DATA = {
        1: ("White", "Iron", "Source of life, clear and cold."),
        2: ("Black", "Water", "Depth, hidden power, potential."),
        3: ("Blue", "Water", "Communication and flow."),
        4: ("Green", "Wood", "Growth and flexibility."),
        5: ("Yellow", "Earth", "Stability and center."),
        6: ("White", "Metal", "Strength and precision."),
        7: ("Red", "Fire", "Passion and illumination."),
        8: ("White", "Metal", "Refinement and clarity."),
        9: ("Purple", "Fire", "Transformation and spirit.")
    }

    color, element, desc = MEWA_DATA[mewa]

    return {
        "mewa_number": mewa,
        "color": color,
        "element": element,
        "description": desc
    }

def get_tibetan_parkha(year: int) -> str:
    """Tibetan Parkha (8 Trigrams)."""
    # Cycle of 8
    idx = (year - 2000) % 8
    TRIGRAMS = ["Li", "Kun", "Dwa", "Khen", "Kham", "Gin", "Zin", "Zon"]
    return TRIGRAMS[idx]
