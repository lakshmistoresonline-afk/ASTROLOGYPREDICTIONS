from typing import Dict, List, Any
from ..core.houses import RASHI_LORDS

def check_gaja_kesari(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter in Kendra from Moon."""
    jupiter = planets["Jupiter"]
    moon = planets["Moon"]

    # Houses are 1-12
    # Relative house
    rel_house = (jupiter["house"] - moon["house"] + 12) % 12 + 1
    if rel_house in [1, 4, 7, 10]:
        return {
            "name": "Gaja Kesari Yoga",
            "present": True,
            "strength": "STRONG" if "Exalted" in jupiter["dignity"] or "Own Sign" in jupiter["dignity"] else "MODERATE",
            "interpretation": "Brings wealth, intelligence, and high status. Overcomes enemies and obstacles."
        }
    return {"present": False}

def check_budha_aditya(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Sun and Mercury in same sign."""
    sun = planets["Sun"]
    mercury = planets["Mercury"]
    if sun["rashi"] == mercury["rashi"]:
        # Should not be combust? Standard often allows it.
        # But if too close, it might be weak.
        dist = abs(sun["longitude"] - mercury["longitude"])
        if dist > 1.0 and dist < 14.0:
            return {
                "name": "Budha Aditya Yoga",
                "present": True,
                "strength": "MODERATE",
                "interpretation": "High intelligence, administrative ability, and oratorical skills."
            }
    return {"present": False}

def check_pancha_mahapurusha(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Non-luminary planets in own/exalt sign and in Kendra."""
    yogas = []
    candidates = {
        "Mars": ("Ruchaka Yoga", "Strength, courage, leadership, and land ownership."),
        "Mercury": ("Bhadra Yoga", "Intelligence, eloquence, longevity, and administrative success."),
        "Jupiter": ("Hamsa Yoga", "Wisdom, morality, prosperity, and respect."),
        "Venus": ("Malavya Yoga", "Luxury, beauty, marital happiness, and artistic talents."),
        "Saturn": ("Shasha Yoga", "Persistence, authority, loyalty of subordinates, and property."),
    }

    for p, (name, interp) in candidates.items():
        data = planets[p]
        if data["house"] in [1, 4, 7, 10]:
            if "Exalted" in data["dignity"] or "Own Sign" in data["dignity"] or "Moolatrikona" in data["dignity"]:
                yogas.append({
                    "name": name,
                    "present": True,
                    "strength": "STRONG" if "Exalted" in data["dignity"] else "MODERATE",
                    "interpretation": interp
                })
    return yogas

def detect_yogas(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    results = []

    gk = check_gaja_kesari(planets)
    if gk["present"]: results.append(gk)

    ba = check_budha_aditya(planets)
    if ba["present"]: results.append(ba)

    pm = check_pancha_mahapurusha(planets)
    results.extend(pm)

    return results
