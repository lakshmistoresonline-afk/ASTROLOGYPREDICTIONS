from typing import Dict, List, Any

# Planetary mapping to the Tree of Life
SEPHIRA_MAP = {
    "Pluto": "Kether (Crown)",
    "Neptune": "Chokmah (Wisdom)",
    "Uranus": "Binah (Understanding)",
    "Jupiter": "Chesed (Mercy)",
    "Mars": "Geburah (Severity)",
    "Sun": "Tiphareth (Beauty)",
    "Venus": "Netzach (Victory)",
    "Mercury": "Hod (Splendour)",
    "Moon": "Yesod (Foundation)",
    "Saturn": "Da'at (The Abyss/Knowledge) or Binah",
    "Earth": "Malkuth (Kingdom)"
}

def get_kabbalistic_profile(planets: Dict[str, Any]) -> List[str]:
    """Map planetary strengths/positions to Sephirothic pathworking."""
    profile = []
    for p_name, p_info in planets.items():
        if p_name in SEPHIRA_MAP:
            sephira = SEPHIRA_MAP[p_name]
            h = getattr(p_info, "house", 0)
            profile.append(f"{p_name} is currently pathworking through {sephira}, focused on life area H{h}.")
    return profile
