from typing import Dict, List, Any
from ..strength.aspects import get_graha_drishti
from ..predictions.framework import are_associated

def _get(obj, attr, default=None):
    if hasattr(obj, attr):
        val = getattr(obj, attr)
        return val() if callable(val) else val
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return default

def check_gaja_kesari(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter in Kendra from Moon."""
    jupiter = planets.get("Jupiter")
    moon = planets.get("Moon")
    if not jupiter or not moon: return {"present": False}

    j_house = _get(jupiter, "house")
    m_house = _get(moon, "house")
    j_dignity = _get(jupiter, "dignity", "")

    rel_house = (j_house - m_house + 12) % 12 + 1
    if rel_house in [1, 4, 7, 10]:
        # Additional condition for full strength: Jupiter should not be combust or debilitated
        is_combust = _get(jupiter, "is_combust", False)
        if "Debilitated" in j_dignity or is_combust:
            return {
                "name": "Gaja Kesari Yoga (Weakened)",
                "present": True,
                "strength": "LOW",
                "interpretation": "Brings intelligence and status, but results may be delayed or obstructed due to Jupiter's weakness."
            }
        return {
            "name": "Gaja Kesari Yoga",
            "present": True,
            "strength": "STRONG" if "Exalted" in j_dignity or "Own Sign" in j_dignity else "MODERATE",
            "interpretation": "Brings wealth, intelligence, and high status. Overcomes enemies and gives a lion-like courage."
        }
    return {"present": False}

def check_budha_aditya(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Sun and Mercury in same sign."""
    sun = planets.get("Sun")
    mercury = planets.get("Mercury")
    if not sun or not mercury: return {"present": False}

    s_rashi = _get(sun, "rashi")
    m_rashi = _get(mercury, "rashi")
    if s_rashi == m_rashi:
        return {
            "name": "Budha Aditya Yoga",
            "present": True,
            "strength": "MODERATE",
            "interpretation": "High intelligence and administrative ability."
        }
    return {"present": False}

def check_chandra_mangala(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Moon and Mars in same sign or house."""
    moon = planets.get("Moon")
    mars = planets.get("Mars")
    if not moon or not mars: return {"present": False}
    if _get(moon, "rashi") == _get(mars, "rashi"):
        return {
            "name": "Chandra-Mangala Yoga",
            "present": True,
            "strength": "MODERATE",
            "interpretation": "Financial success through active effort and courageous mindset."
        }
    return {"present": False}

def check_kemadruma(planets: Dict[str, Any]) -> Dict[str, Any]:
    """No planets in signs adjacent to Moon."""
    moon = planets.get("Moon")
    if not moon: return {"present": False}
    m_rashi = _get(moon, "rashi")
    prev_rashi = (m_rashi - 1 + 12) % 12
    next_rashi = (m_rashi + 1) % 12
    others = [p for p in planets if p not in ["Moon", "Sun", "Rahu", "Ketu"]]
    for p in others:
        p_rashi = _get(planets[p], "rashi")
        if p_rashi == prev_rashi or p_rashi == next_rashi:
            return {"present": False}
    return {
        "name": "Kemadruma Yoga",
        "present": True,
        "strength": "CAUTION",
        "interpretation": "May indicate periods of isolation or financial fluctuations."
    }

def check_pancha_mahapurusha(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    yogas = []
    candidates = {
        "Mars": ("Ruchaka Yoga", "Strength, courage, and leadership."),
        "Mercury": ("Bhadra Yoga", "Intelligence and administrative success."),
        "Jupiter": ("Hamsa Yoga", "Wisdom and prosperity."),
        "Venus": ("Malavya Yoga", "Luxury and artistic talents."),
        "Saturn": ("Shasha Yoga", "Persistence and authority."),
    }
    for p, (name, interp) in candidates.items():
        data = planets.get(p)
        if not data: continue
        if _get(data, "house") in [1, 4, 7, 10]:
            p_dignity = _get(data, "dignity", "")
            if "Exalted" in p_dignity or "Own Sign" in p_dignity:
                yogas.append({"name": name, "present": True, "strength": "STRONG", "interpretation": interp})
    return yogas

def check_lakshmi_yoga(planets: Dict[str, Any], house_lords: Dict[int, str]) -> Dict[str, Any]:
    l9_name = house_lords.get(9)
    l1_name = house_lords.get(1)
    if l9_name and l1_name:
        l9 = planets.get(l9_name)
        l1 = planets.get(l1_name)
        if l9 and l1 and _get(l9, "house") in [1, 4, 7, 10] and ("Exalted" in _get(l1, "dignity", "") or "Own Sign" in _get(l1, "dignity", "")):
            return {"name": "Lakshmi Yoga", "present": True, "strength": "STRONG", "interpretation": "Wealth and grace of goddess Lakshmi."}
    return {"present": False}

def check_sakata_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    moon = planets.get("Moon")
    jupiter = planets.get("Jupiter")
    if not moon or not jupiter: return {"present": False}
    rel_h = (_get(moon, "house") - _get(jupiter, "house") + 12) % 12 + 1
    if rel_h in [6, 8, 12]:
        if _get(moon, "house") in [1, 4, 7, 10]:
            return {"name": "Sakata Yoga (Cancelled)", "present": True, "strength": "NEUTRAL", "interpretation": "Negative effects cancelled by Kendra position."}
        return {"name": "Sakata Yoga", "present": True, "strength": "CAUTION", "interpretation": "Potential for financial fluctuations."}
    return {"present": False}

def check_adhi_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    moon = planets.get("Moon")
    if not moon: return {"present": False}
    m_house = _get(moon, "house")
    benefics = ["Jupiter", "Venus", "Mercury"]
    count = 0
    for b in benefics:
        b_data = planets.get(b)
        if b_data and (_get(b_data, "house") - m_house + 12) % 12 + 1 in [6, 7, 8]:
            count += 1
    if count >= 2:
        return {"name": "Adhi Yoga", "present": True, "strength": "STRONG", "interpretation": "Leadership and victory over enemies."}
    return {"present": False}

def check_saraswati_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter, Venus, Mercury in Kendra/Trikona or 2nd house and Jupiter strong."""
    jup = planets.get("Jupiter")
    ven = planets.get("Venus")
    merc = planets.get("Mercury")
    if not jup or not ven or not merc: return {"present": False}

    houses = [_get(jup, "house"), _get(ven, "house"), _get(merc, "house")]
    good_houses = [1, 2, 4, 5, 7, 9, 10]

    if all(h in good_houses for h in houses) and "Exalted" in _get(jup, "dignity", ""):
        return {
            "name": "Saraswati Yoga",
            "present": True,
            "strength": "STRONG",
            "interpretation": "Exceptional wisdom, learning, and fame in arts or sciences."
        }
    return {"present": False}

def check_kalanidhi_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Jupiter in 2nd or 5th house and associated with Mercury or Venus."""
    jup = planets.get("Jupiter")
    if not jup: return {"present": False}
    j_house = _get(jup, "house")
    if j_house in [2, 5]:
        if are_associated("Jupiter", "Mercury", planets) or are_associated("Jupiter", "Venus", planets):
            return {
                "name": "Kalanidhi Yoga",
                "present": True,
                "strength": "MODERATE",
                "interpretation": "Brings wealth, good health, and respect in society."
            }
    return {"present": False}

def check_vipareeta_raja_yoga(planets: Dict[str, Any], house_lords: Dict[int, str]) -> List[Dict[str, Any]]:
    yogas = []
    dusthanas = [6, 8, 12]
    for h in dusthanas:
        lord_name = house_lords.get(h)
        lord_p = planets.get(lord_name)
        if lord_p and _get(lord_p, "house") in dusthanas:
            yogas.append({"name": f"Vipareeta Raja Yoga ({lord_name})", "present": True, "strength": "MODERATE", "interpretation": "Success through sudden changes or downfall of competitors."})
    return yogas

def check_jaimini_rajayogas(chart: Any) -> List[Dict[str, Any]]:
    yogas = []
    karakas = getattr(chart, "jaimini_karakas", {})
    ak = karakas.get("Atmakaraka (AK) - Soul")
    amk = karakas.get("Amatyakaraka (AmK) - Career/Mind")
    if ak and amk and are_associated(ak, amk, chart.planets):
        yogas.append({"name": "Jaimini Raja Yoga (AK & AmK)", "present": True, "strength": "VERY STRONG", "interpretation": "Connection between Soul and Career indicators."})

    # AK and 5th lord from AK association
    # This requires more complex logic to find 5th sign from AK's sign
    return yogas

def check_parivartana_yogas(planets: Dict[str, Any], house_lords: Dict[int, str]) -> List[Dict[str, Any]]:
    """Exchange of signs between two house lords."""
    yogas = []
    if not house_lords: return yogas

    for h1 in range(1, 13):
        for h2 in range(h1 + 1, 13):
            l1_name = house_lords.get(h1)
            l2_name = house_lords.get(h2)
            if not l1_name or not l2_name: continue

            p1 = planets.get(l1_name)
            p2 = planets.get(l2_name)
            if not p1 or not p2: continue

            # l1 is in h2 house sign AND l2 is in h1 house sign
            # This requires knowing which rashi is in which house
            # Simplified: if l1 is in h2 house and l2 is in h1 house
            if _get(p1, "house") == h2 and _get(p2, "house") == h1:
                type_y = "Maha Yoga" if h1 in [1,2,4,5,7,9,10,11] and h2 in [1,2,4,5,7,9,10,11] else "Dainya Yoga"
                if h1 in [6,8,12] or h2 in [6,8,12]: type_y = "Dainya Yoga"
                if h1 == 3 or h2 == 3: type_y = "Khala Yoga"

                yogas.append({
                    "name": f"Parivartana Yoga ({type_y})",
                    "present": True,
                    "strength": "STRONG",
                    "interpretation": f"Exchange between H{h1} and H{h2} lords. {type_y} indicates {'positive' if type_y == 'Maha Yoga' else 'mixed'} results."
                })
    return yogas

def check_vasumathi_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Benefics in Upachaya houses (3, 6, 10, 11) from Lagna or Moon."""
    benefics = ["Jupiter", "Venus", "Mercury"]
    count = 0
    for b in benefics:
        b_data = planets.get(b)
        if b_data and _get(b_data, "house") in [3, 6, 10, 11]:
            count += 1
    if count == 3:
        return {"name": "Vasumathi Yoga", "present": True, "strength": "VERY STRONG", "interpretation": "Brings immense wealth and prosperity independent of other factors."}
    return {"present": False}

def check_parijata_yoga(planets: Dict[str, Any], house_lords: Dict[int, str]) -> Dict[str, Any]:
    """Lord of the sign where Lagna Lord is placed, and the lord of that planet's Navamsha sign, should be in Kendra/Trikona."""
    l1_name = house_lords.get(1)
    l1 = planets.get(l1_name)
    if not l1: return {"present": False}

    # Simplified: Lord of L1's sign is in Kendra/Trikona
    from ..core.houses import RASHI_LORDS
    l1_dispositor_name = RASHI_LORDS[_get(l1, "rashi")]
    dispositor = planets.get(l1_dispositor_name)

    if dispositor and _get(dispositor, "house") in [1, 4, 7, 10, 5, 9]:
        return {"name": "Parijata Yoga", "present": True, "strength": "MODERATE", "interpretation": "Success in the middle and later part of life, happy and respectful."}
    return {"present": False}

def check_kahala_yoga(planets: Dict[str, Any], house_lords: Dict[int, str]) -> Dict[str, Any]:
    """Lords of 4th and 9th houses in mutual Kendra and L1 strong."""
    l4 = house_lords.get(4)
    l9 = house_lords.get(9)
    if not l4 or not l9: return {"present": False}

    p4 = planets.get(l4)
    p9 = planets.get(l9)
    if not p4 or not p9: return {"present": False}

    rel_h = (_get(p4, "house") - _get(p9, "house") + 12) % 12 + 1
    if rel_h in [1, 4, 7, 10]:
        return {"name": "Kahala Yoga", "present": True, "strength": "MODERATE", "interpretation": "Noble, energetic, and successful in administrative roles."}
    return {"present": False}

def check_durudhara_yoga(planets: Dict[str, Any]) -> Dict[str, Any]:
    """Planets (other than Sun) in both 2nd and 12th from Moon."""
    moon = planets.get("Moon")
    if not moon: return {"present": False}
    m_h = _get(moon, "house")
    h2 = (m_h % 12) + 1
    h12 = (m_h - 2 + 12) % 12 + 1

    p2 = [p for p, info in planets.items() if p != "Sun" and _get(info, "house") == h2]
    p12 = [p for p, info in planets.items() if p != "Sun" and _get(info, "house") == h12]

    if p2 and p12:
        return {"name": "Durudhara Yoga", "present": True, "strength": "STRONG", "interpretation": "Wealthy, charitable, and blessed with good family and vehicles."}
    return {"present": False}

def check_sunapha_anapha(planets: Dict[str, Any]) -> List[Dict[str, Any]]:
    yogas = []
    moon = planets.get("Moon")
    if not moon: return yogas
    m_h = _get(moon, "house")
    h2 = (m_h % 12) + 1
    h12 = (m_h - 2 + 12) % 12 + 1

    p2 = [p for p, info in planets.items() if p not in ["Sun", "Moon", "Rahu", "Ketu"] and _get(info, "house") == h2]
    p12 = [p for p, info in planets.items() if p not in ["Sun", "Moon", "Rahu", "Ketu"] and _get(info, "house") == h12]

    if p2 and not p12:
        yogas.append({"name": "Sunapha Yoga", "present": True, "strength": "MODERATE", "interpretation": "Self-earned wealth, fame, and good intelligence."})
    if p12 and not p2:
        yogas.append({"name": "Anapha Yoga", "present": True, "strength": "MODERATE", "interpretation": "Well-formed body, polite, famous, and happy."})
    return yogas

def check_kala_sarpa(planets: Dict[str, Any]) -> Dict[str, Any]:
    """All planets between Rahu and Ketu."""
    rahu = planets.get("Rahu")
    ketu = planets.get("Ketu")
    if not rahu or not ketu: return {"present": False}

    r_rashi = _get(rahu, "rashi")
    k_rashi = _get(ketu, "rashi")

    # Signs between Rahu and Ketu (forward)
    forward_signs = []
    curr = r_rashi
    while curr != k_rashi:
        forward_signs.append(curr)
        curr = (curr + 1) % 12
    forward_signs.append(k_rashi)

    backward_signs = []
    curr = r_rashi
    while curr != k_rashi:
        backward_signs.append(curr)
        curr = (curr - 1 + 12) % 12
    backward_signs.append(k_rashi)

    others = [p for p in planets if p not in ["Rahu", "Ketu"]]
    in_forward = True
    in_backward = True

    for p in others:
        p_r = _get(planets[p], "rashi")
        if p_r not in forward_signs: in_forward = False
        if p_r not in backward_signs: in_backward = False

    if in_forward or in_backward:
        type_ks = "Ananta" if r_rashi == 0 else "Kulika" # Simplified names
        return {
            "name": "Kala Sarpa Yoga",
            "present": True,
            "strength": "CAUTION",
            "interpretation": "All planets hemmed between nodes. May bring intense struggle followed by great success."
        }
    return {"present": False}

def detect_yogas(planets: Dict[str, Any], house_lords: Dict[int, str] = None, chart: Any = None) -> List[Dict[str, Any]]:
    results = []
    results.append(check_gaja_kesari(planets))
    results.append(check_budha_aditya(planets))
    results.append(check_chandra_mangala(planets))
    results.extend(check_pancha_mahapurusha(planets))
    results.append(check_vasumathi_yoga(planets))
    results.extend(check_sunapha_anapha(planets))
    results.append(check_durudhara_yoga(planets))
    if house_lords:
        results.append(check_lakshmi_yoga(planets, house_lords))
        results.extend(check_vipareeta_raja_yoga(planets, house_lords))
        results.extend(check_parivartana_yogas(planets, house_lords))
        results.append(check_parijata_yoga(planets, house_lords))
        results.append(check_kahala_yoga(planets, house_lords))
    results.append(check_sakata_yoga(planets))
    results.append(check_adhi_yoga(planets))
    results.append(check_saraswati_yoga(planets))
    results.append(check_kalanidhi_yoga(planets))
    results.append(check_kemadruma(planets))
    results.append(check_kala_sarpa(planets))
    if chart:
        results.extend(check_jaimini_rajayogas(chart))

    # 8b. Special Combinations (Visha Kanya / etc.)
    # Sunday + Dwitiya + Ashlesha... (Simplified check)
    # (Requires birth weekday and tithi, but we can check chart panchang if available)

    # 9. Kartari Yogas (Hemming)
    # Check each house
    for h in range(1, 13):
        # sign index
        # (Requires Lagna Rashi from chart)
        if chart:
            asc_r = chart.asc_rashi
            h_r = (asc_r + h - 1) % 12
            prev_r = (h_r - 1 + 12) % 12
            next_r = (h_r + 1) % 12

            p_prev = [p for p, info in planets.items() if info.rashi == prev_r]
            p_next = [p for p, info in planets.items() if info.rashi == next_r]

            malefics = ["Saturn", "Mars", "Sun", "Rahu", "Ketu"]
            benefics = ["Jupiter", "Venus", "Moon", "Mercury"]

            if any(p in malefics for p in p_prev) and any(p in malefics for p in p_next):
                results.append({"name": f"Paapa Kartari Yoga (H{h})", "present": True, "strength": "CAUTION", "interpretation": "House hemmed between challenging planets, indicating external pressures on this life area."})
            if any(p in benefics for p in p_prev) and any(p in benefics for p in p_next):
                results.append({"name": f"Subha Kartari Yoga (H{h})", "present": True, "strength": "STRONG", "interpretation": "House hemmed between supportive planets, indicating protection and growth."})

    return [r for r in results if r.get("present")]
