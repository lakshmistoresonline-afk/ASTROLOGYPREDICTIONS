from datetime import date
from typing import Dict, Any

# Maya Tzolkin Calendar
MAYA_NAMES = [
    "Imix", "Ik", "Akbal", "Kan", "Chicchan", "Cimi", "Manik", "Lamat", "Muluc", "Oc",
    "Chuen", "Eb", "Ben", "Ix", "Men", "Cib", "Caban", "Etznab", "Cauac", "Ahau"
]

def calculate_maya_tzolkin(y: int, m: int, d: int) -> Dict[str, Any]:
    """Calculate the Tzolkin Day (Maya Sacred Calendar)."""
    # Reference: 2000-01-01 was 8 Manik
    d1 = date(2000, 1, 1)
    d2 = date(y, m, d)
    diff = (d2 - d1).days

    # 260 day cycle (13 numbers * 20 names)
    tzolkin_day = (diff + (8 - 1) * 20 + 6) % 260 # 6 is Manik index

    number = (diff + 8 - 1) % 13 + 1
    name_idx = (diff + 6) % 20

    return {
        "number": number,
        "name": MAYA_NAMES[name_idx],
        "karmic_theme": _get_tzolkin_meaning(MAYA_NAMES[name_idx])
    }

def _get_tzolkin_meaning(name: str) -> str:
    meanings = {
        "Manik": "Healing, completion, and the energy of the hand.",
        "Ahau": "Enlightenment, solar consciousness, and wholeness.",
        # ...
    }
    return meanings.get(name, "Spiritual archetypal energy.")
