from typing import Dict, List, Any

def check_gaja_kesari(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter in Kendra from Moon."""
    jupiter = planets["Jupiter"]
    moon = planets["Moon"]

    # Handle both PlanetInfo objects and dicts
    j_house = jupiter.house if hasattr(jupiter, "house") else jupiter["house"]
    m_house = moon.house if hasattr(moon, "house") else moon["house"]
    j_dignity = jupiter.dignity if hasattr(jupiter, "dignity") else jupiter["dignity"]

    rel_house = (j_house - m_house + 12) % 12 + 1
    if rel_house in [1, 4, 7, 10]:
        return {
            "name": "Gaja Kesari Yoga",
            "present": True,
            "strength": "STRONG" if "Exalted" in j_dignity or "Own Sign" in j_dignity else "MODERATE",
            "interpretation": "Brings wealth, intelligence, and high status. Overcomes enemies and obstacles."
        }
    return {"present": False}

def check_budha_aditya(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Sun and Mercury in same sign."""
    sun = planets["Sun"]
    mercury = planets["Mercury"]

    s_rashi = sun.rashi if hasattr(sun, "rashi") else sun["rashi"]
    m_rashi = mercury.rashi if hasattr(mercury, "rashi") else mercury["rashi"]
    s_lon = sun.longitude if hasattr(sun, "longitude") else sun["longitude"]
    m_lon = mercury.longitude if hasattr(mercury, "longitude") else mercury["longitude"]

    if s_rashi == m_rashi:
        dist = abs(s_lon - m_lon)
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
        p_house = data.house if hasattr(data, "house") else data["house"]
        p_dignity = data.dignity if hasattr(data, "dignity") else data["dignity"]

        if p_house in [1, 4, 7, 10]:
            if "Exalted" in p_dignity or "Own Sign" in p_dignity or "Moolatrikona" in p_dignity:
                yogas.append({
                    "name": name,
                    "present": True,
                    "strength": "STRONG" if "Exalted" in p_dignity else "MODERATE",
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
