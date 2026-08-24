from datetime import date
from typing import Dict

def get_celtic_tree_astrology(m: int, d: int) -> Dict[str, str]:
    """Celtic Tree Astrology (13 Lunar Months)."""
    # Simplified dates
    trees = [
        ((12, 24), (1, 20), "Birch"),
        ((1, 21), (2, 17), "Rowan"),
        ((2, 18), (3, 17), "Ash"),
        ((3, 18), (4, 14), "Alder"),
        ((4, 15), (5, 12), "Willow"),
        ((5, 13), (6, 9), "Hawthorn"),
        ((6, 10), (7, 7), "Oak"),
        ((7, 8), (8, 4), "Holly"),
        ((8, 5), (9, 1), "Hazel"),
        ((9, 2), (9, 29), "Vine"),
        ((9, 30), (10, 27), "Ivy"),
        ((10, 28), (11, 24), "Reed"),
        ((11, 25), (12, 23), "Elder")
    ]

    birth = (m, d)
    for (s_m, s_d), (e_m, e_d), name in trees:
        # Handle wrap around year end
        if s_m > e_m:
            if birth >= (s_m, s_d) or birth <= (e_m, e_d):
                return {"tree": name, "archetype": _get_tree_archetype(name)}
        else:
            if (s_m, s_d) <= birth <= (e_m, e_d):
                return {"tree": name, "archetype": _get_tree_archetype(name)}

    return {"tree": "Unknown", "archetype": ""}

def _get_tree_archetype(name: str) -> str:
    meanings = {
        "Birch": "The Achiever - High ambition and drive.",
        "Rowan": "The Thinker - Originality and creative vision.",
        "Ash": "The Enchanter - High intuition and artistic nature.",
        "Oak": "The Stabilizer - Strength and protection.",
        # ...
    }
    return meanings.get(name, "A unique nature archetype.")
