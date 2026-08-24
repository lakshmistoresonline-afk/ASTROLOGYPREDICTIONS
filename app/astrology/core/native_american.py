from typing import Dict

def get_native_american_totem(m: int, d: int) -> Dict[str, str]:
    """Native American Animal Totems based on birth date (Northern Hemisphere)."""
    totems = [
        ((1, 20), (2, 18), "Otter"),
        ((2, 19), (3, 20), "Wolf"),
        ((3, 21), (4, 19), "Falcon"),
        ((4, 20), (5, 20), "Beaver"),
        ((5, 21), (6, 20), "Deer"),
        ((6, 21), (7, 21), "Woodpecker"),
        ((7, 22), (8, 21), "Salmon"),
        ((8, 22), (9, 21), "Bear"),
        ((9, 22), (10, 22), "Raven"),
        ((10, 23), (11, 22), "Snake"),
        ((11, 23), (12, 21), "Owl"),
        ((12, 22), (1, 19), "Goose")
    ]

    birth = (m, d)
    for (s_m, s_d), (e_m, e_d), name in totems:
        if s_m > e_m: # Goose
            if birth >= (s_m, s_d) or birth <= (e_m, e_d):
                return {"totem": name, "meaning": _get_totem_meaning(name)}
        else:
            if (s_m, s_d) <= birth <= (e_m, e_d):
                return {"totem": name, "meaning": _get_totem_meaning(name)}

    return {"totem": "Unknown", "meaning": ""}

def _get_totem_meaning(name: str) -> str:
    meanings = {
        "Wolf": "Deep emotion, intuition, and fierce loyalty.",
        "Falcon": "Vision, swiftness, and leadership.",
        "Snake": "Transformation, healing, and mystery.",
        "Bear": "Strength, grounding, and introspective power."
    }
    return meanings.get(name, "A connection to the natural world.")
