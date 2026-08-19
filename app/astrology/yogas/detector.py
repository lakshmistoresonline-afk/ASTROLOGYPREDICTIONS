from typing import Dict, List, Any

def _get(obj, attr, default=None):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    return obj.get(attr, default)

def check_gaja_kesari(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter in Kendra from Moon."""
    jupiter = planets.get("Jupiter")
    moon = planets.get("Moon")
    if not jupiter or not moon: return {"present": False}

    j_house = _get(jupiter, "house")
    m_house = _get(moon, "house")
    j_dignity = _get(jupiter, "dignity", "")

    # Jupiter in 1, 4, 7, 10 from Moon
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
    sun = planets.get("Sun")
    mercury = planets.get("Mercury")
    if not sun or not mercury: return {"present": False}

    s_rashi = _get(sun, "rashi")
    m_rashi = _get(mercury, "rashi")
    s_lon = _get(sun, "longitude")
    m_lon = _get(mercury, "longitude")

    if s_rashi == m_rashi:
        dist = abs(s_lon - m_lon)
        # Not combust but close enough to be a yoga
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
        data = planets.get(p)
        if not data: continue
        p_house = _get(data, "house")
        p_dignity = _get(data, "dignity", "")

        if p_house in [1, 4, 7, 10]:
            if "Exalted" in p_dignity or "Own Sign" in p_dignity or "Moolatrikona" in p_dignity:
                yogas.append({
                    "name": name,
                    "present": True,
                    "strength": "STRONG" if "Exalted" in p_dignity else "MODERATE",
                    "interpretation": interp
                })
    return yogas

def check_lakshmi_yoga(planets: Dict[str, Any], house_lords: Dict[int, str]) -> Dict[str, Any]:
    """9th Lord in Kendra and Lagna Lord strong."""
    l9_name = house_lords.get(9)
    l1_name = house_lords.get(1)
    if not l9_name or not l1_name: return {"present": False}

    l9 = planets.get(l9_name)
    l1 = planets.get(l1_name)
    if not l9 or not l1: return {"present": False}

    if _get(l9, "house") in [1, 4, 7, 10]:
        l1_dignity = _get(l1, "dignity", "")
        if "Exalted" in l1_dignity or "Own Sign" in l1_dignity:
            return {
                "name": "Lakshmi Yoga",
                "present": True,
                "strength": "STRONG",
                "interpretation": "Wealth, prosperity, noble character, and grace of goddess Lakshmi."
            }
    return {"present": False}

def check_saraswati_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter, Venus, and Mercury in Kendra/Trikona and Jupiter strong."""
    jup = planets.get("Jupiter")
    ven = planets.get("Venus")
    merc = planets.get("Mercury")
    if not jup or not ven or not merc: return {"present": False}

    houses = [_get(jup, "house"), _get(ven, "house"), _get(merc, "house")]
    kendra_trikona = [1, 4, 7, 10, 5, 9]

    if all(h in kendra_trikona for h in houses):
        j_dignity = _get(jup, "dignity", "")
        if any(d in j_dignity for d in ["Exalted", "Own Sign", "Friendly"]):
            return {
                "name": "Saraswati Yoga",
                "present": True,
                "strength": "MODERATE",
                "interpretation": "Exceptional wisdom, learning, eloquence, and fame in arts/sciences."
            }
    return {"present": False}

def check_adhi_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Benefics in 6, 7, 8 from Moon."""
    moon = planets.get("Moon")
    if not moon: return {"present": False}
    m_house = _get(moon, "house")

    benefics = ["Jupiter", "Venus", "Mercury"]
    count = 0
    for b in benefics:
        b_data = planets.get(b)
        if not b_data: continue
        b_house = _get(b_data, "house")
        rel_house = (b_house - m_house + 12) % 12 + 1
        if rel_house in [6, 7, 8]:
            count += 1

    if count >= 2:
        return {
            "name": "Chandra Adhi Yoga",
            "present": True,
            "strength": "STRONG" if count == 3 else "MODERATE",
            "interpretation": "Leadership, high status, victory over enemies, and long life."
        }
    return {"present": False}

def check_lunar_yogas(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Sunapha, Anapha, Dhurdhura."""
    moon = planets.get("Moon")
    if not moon: return []
    m_rashi = _get(moon, "rashi")

    prev_rashi = (m_rashi - 1 + 12) % 12
    next_rashi = (m_rashi + 1) % 12

    planets_around = {
        "prev": [],
        "next": []
    }

    for p, data in planets.items():
        if p in ["Sun", "Moon", "Rahu", "Ketu"]: continue
        p_rashi = _get(data, "rashi")
        if p_rashi == prev_rashi: planets_around["prev"].append(p)
        if p_rashi == next_rashi: planets_around["next"].append(p)

    yogas = []
    if planets_around["next"] and not planets_around["prev"]:
        yogas.append({
            "name": "Sunapha Yoga",
            "present": True,
            "strength": "MODERATE",
            "interpretation": "Wealth, self-acquired property, and sharp intelligence."
        })
    elif planets_around["prev"] and not planets_around["next"]:
        yogas.append({
            "name": "Anapha Yoga",
            "present": True,
            "strength": "MODERATE",
            "interpretation": "Good health, polite manners, and fame."
        })
    elif planets_around["prev"] and planets_around["next"]:
        yogas.append({
            "name": "Dhurdhura Yoga",
            "present": True,
            "strength": "STRONG",
            "interpretation": "Abundant wealth, comfort, and administrative power."
        })

    return yogas

def check_raja_yogas(planets: Dict[str, Any], house_lords: Dict[int, str]) -> List[Dict[str, Any]]:
    """Kendra and Trikona lord associations."""
    kendras = [1, 4, 7, 10]
    trikonas = [1, 5, 9]
    yogas = []

    k_lords = [house_lords[k] for k in kendras]
    t_lords = [house_lords[t] for t in trikonas]

    # Dharma Karma Adhipati Yoga (9th and 10th)
    l9_name = house_lords[9]
    l10_name = house_lords[10]
    l9 = planets[l9_name]
    l10 = planets[l10_name]

    if _get(l9, "rashi") == _get(l10, "rashi"):
        yogas.append({
            "name": "Dharma Karma Adhipati Yoga",
            "present": True,
            "strength": "STRONG",
            "interpretation": "A major Raja Yoga indicating high status, power, and ethical leadership."
        })

    return yogas

def detect_yogas(planets: Dict[str, Any], house_lords: Dict[int, str] = None) -> List[Dict[str, Any]]:
    results = []

    # 1. Standard Yogas
    gk = check_gaja_kesari(planets)
    if gk["present"]: results.append(gk)

    ba = check_budha_aditya(planets)
    if ba["present"]: results.append(ba)

    pm = check_pancha_mahapurusha(planets)
    results.extend(pm)

    # 2. Wealth & Wisdom
    if house_lords:
        ly = check_lakshmi_yoga(planets, house_lords)
        if ly["present"]: results.append(ly)

        # Raja Yogas
        results.extend(check_raja_yogas(planets, house_lords))

    sy = check_saraswati_yoga(planets)
    if sy["present"]: results.append(sy)

    # 3. Strength & Influence
    ay = check_adhi_yoga(planets)
    if ay["present"]: results.append(ay)

    # 4. Lunar Configs
    results.extend(check_lunar_yogas(planets))

    return results
