from typing import Dict, Any

# Decanates (10 degrees each)
DECAN_LORDS = {
    0: ["Mars", "Sun", "Jupiter"],      # Aries
    1: ["Venus", "Mercury", "Saturn"],   # Taurus
    2: ["Mercury", "Venus", "Saturn"],   # Gemini
    3: ["Moon", "Mars", "Jupiter"],      # Cancer
    4: ["Sun", "Jupiter", "Mars"],       # Leo
    5: ["Mercury", "Saturn", "Venus"],   # Virgo
    6: ["Venus", "Saturn", "Mercury"],   # Libra
    7: ["Mars", "Jupiter", "Moon"],      # Scorpio
    8: ["Jupiter", "Mars", "Sun"],       # Sagittarius
    9: ["Saturn", "Venus", "Mercury"],   # Capricorn
    10: ["Saturn", "Mercury", "Venus"],  # Aquarius
    11: ["Jupiter", "Moon", "Mars"]      # Pisces
}

def get_decanate_info(rashi: int, degree: float) -> Dict[str, str]:
    """Get the lord and quality of the decanate."""
    idx = int(degree / 10)
    if idx > 2: idx = 2

    lord = DECAN_LORDS[rashi][idx]

    # Simple quality based on lord
    qualities = {
        "Sun": "Vitality and Leadership",
        "Moon": "Sensitivity and Nurturing",
        "Mars": "Energy and Initiative",
        "Mercury": "Intelligence and Skill",
        "Jupiter": "Wisdom and Growth",
        "Venus": "Harmony and Beauty",
        "Saturn": "Discipline and Structure"
    }

    return {
        "lord": lord,
        "quality": qualities.get(lord, "Mixed Energy"),
        "index": idx + 1
    }

def get_dwadashamsha(rashi: int, degree: float) -> int:
    """Calculate the Dwadashamsha (1/12th of a sign - 2.5 degrees)."""
    # Each dwadashamsha is 2.5 degrees.
    # The first dwadashamsha of a sign is the sign itself.
    dwad_idx = int(degree / 2.5)
    return (rashi + dwad_idx) % 12
