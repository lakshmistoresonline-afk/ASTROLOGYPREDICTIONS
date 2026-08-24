from typing import Dict, List, Any

# 16 Geomantic Figures
FIGURES = [
    "Via", "Cauda Draconis", "Puer", "Fortuna Minor", "Puella", "Amissio", "Albus", "Populus",
    "Fortuna Major", "Conjunctio", "Acquisitio", "Rubeus", "Laetitia", "Tristitia", "Caput Draconis", "Carcer"
]

def calculate_birth_figure(y: int, m: int, d: int, h: int) -> Dict[str, str]:
    """Calculate the primary geomantic figure based on birth time binary reduction."""
    # Simplified calculation using parity of birth elements
    # 1=Odd, 0=Even
    bits = [y % 2, m % 2, d % 2, h % 2]

    # Map 4 bits to 16 figures
    idx = int("".join(map(str, bits)), 2)
    name = FIGURES[idx]

    return {
        "birth_figure": name,
        "element": _get_figure_element(name),
        "interpretation": _get_figure_meaning(name)
    }

def _get_figure_element(name: str) -> str:
    # Standard geomantic elemental mapping
    if name in ["Via", "Populus"]: return "Water"
    if name in ["Fortuna Major", "Fortuna Minor"]: return "Fire"
    # ...
    return "Air"

def _get_figure_meaning(name: str) -> str:
    meanings = {
        "Fortuna Major": "Great Fortune and inner strength.",
        "Amissio": "Loss or letting go of the unnecessary.",
        "Albus": "Wisdom, clarity, and peace.",
        "Rubeus": "Intensity, passion, and potential conflict."
    }
    return meanings.get(name, "A symbolic pattern of destiny.")
