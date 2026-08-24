from typing import Dict, Any, List
from .data import (
    NAKSHATRA_GANA, NAKSHATRA_YONI, NAKSHATRA_NADI,
    YONI_SCORE_TABLE, RASHI_VARNA, RASHI_VASHYA,
    PLANET_FRIENDSHIP, RASHI_LORDS
)
from ..core.models import CanonicalChart

def calculate_varna(boy_rashi: int, girl_rashi: int) -> float:
    b_v = RASHI_VARNA[boy_rashi]
    g_v = RASHI_VARNA[girl_rashi]
    if b_v <= g_v: return 1.0
    return 0.0

def calculate_vashya(boy_rashi: int, girl_rashi: int) -> float:
    b_v = RASHI_VASHYA[boy_rashi]
    g_v = RASHI_VASHYA[girl_rashi]
    if b_v == g_v: return 2.0
    vashya_map = {"Chatushpad": ["Manav", "Jalchar"], "Manav": ["Chatushpad", "Keet"], "Jalchar": ["Chatushpad", "Manav"], "Keet": ["Manav"]}
    if g_v in vashya_map.get(b_v, []): return 1.0
    return 0.0

def calculate_tara(boy_nak: int, girl_nak: int) -> float:
    diff1 = (boy_nak - girl_nak + 27) % 9
    diff2 = (girl_nak - boy_nak + 27) % 9
    bad_tara = [3, 5, 7]
    score = 0.0
    if (diff1 % 9) not in bad_tara: score += 1.5
    if (diff2 % 9) not in bad_tara: score += 1.5
    return score

def calculate_yoni(boy_nak: int, girl_nak: int) -> float:
    b_y = NAKSHATRA_YONI[boy_nak]
    g_y = NAKSHATRA_YONI[girl_nak]
    return float(YONI_SCORE_TABLE.get(b_y, {}).get(g_y, 0))

def calculate_grahamaitri(boy_rashi: int, girl_rashi: int) -> float:
    b_l = RASHI_LORDS[boy_rashi]
    g_l = RASHI_LORDS[girl_rashi]
    if b_l == g_l: return 5.0
    return float(PLANET_FRIENDSHIP[b_l][g_l])

def calculate_gana(boy_nak: int, girl_nak: int) -> float:
    b_g = NAKSHATRA_GANA[boy_nak]
    g_g = NAKSHATRA_GANA[girl_nak]
    if b_g == g_g: return 6.0
    if (b_g == "Deva" and g_g == "Manushya") or (b_g == "Manushya" and g_g == "Deva"): return 5.0
    return 0.0

def calculate_bhakut(boy_rashi: int, girl_rashi: int) -> float:
    diff = (boy_rashi - girl_rashi + 12) % 12 + 1
    if diff in [2, 12, 5, 9, 6, 8]: return 0.0
    return 7.0

def calculate_nadi(boy_nak: int, girl_nak: int) -> float:
    if NAKSHATRA_NADI[boy_nak] == NAKSHATRA_NADI[girl_nak]: return 0.0
    return 8.0

def is_manglik(chart: CanonicalChart) -> Dict[str, Any]:
    """Check if a native is Manglik (Mars in 1, 2, 4, 7, 8, 12)."""
    mars = chart.planets.get("Mars")
    if not mars: return {"is_manglik": False, "house": 0}

    m_house = mars.house
    if m_house in [1, 2, 4, 7, 8, 12]:
        # Check for cancellation
        # Rule: Mars in own sign or exaltation
        if mars.dignity in ["Own Sign", "Exalted"]:
             return {"is_manglik": False, "house": m_house, "cancelled": True, "reason": "Mars in Own Sign/Exalted"}
        return {"is_manglik": True, "house": m_house}
    return {"is_manglik": False, "house": m_house}

def get_matchmaking_score(boy_chart: CanonicalChart, girl_chart: CanonicalChart) -> Dict[str, Any]:
    b_moon = boy_chart.planets["Moon"]
    g_moon = girl_chart.planets["Moon"]

    b_r, b_n = b_moon.rashi, b_moon.nakshatra.index
    g_r, g_n = g_moon.rashi, g_moon.nakshatra.index

    kutas = [
        ("Varna", calculate_varna(b_r, g_r), 1.0),
        ("Vashya", calculate_vashya(b_r, g_r), 2.0),
        ("Tara", calculate_tara(b_n, g_n), 3.0),
        ("Yoni", calculate_yoni(b_n, g_n), 4.0),
        ("Graha Maitri", calculate_grahamaitri(b_r, g_r), 5.0),
        ("Gana", calculate_gana(b_n, g_n), 6.0),
        ("Bhakut", calculate_bhakut(b_r, g_r), 7.0),
        ("Nadi", calculate_nadi(b_n, g_n), 8.0),
    ]

    total_score = sum(k[1] for k in kutas)

    # --- DOSHA CANCELLATIONS (Refined Accuracy) ---
    cancellations = []

    # 1. Bhakut Dosha Cancellation
    if calculate_bhakut(b_r, g_r) == 0:
        # Rule: Same Rashi lord or mutual friendship cancels Bhakoot Dosha
        b_lord = RASHI_LORDS[b_r]
        g_lord = RASHI_LORDS[g_r]
        if b_lord == g_lord or PLANET_FRIENDSHIP[b_lord][g_lord] >= 4.0:
            cancellations.append("Bhakoot Dosha cancelled due to Rashi Lord friendship.")
            total_score += 7.0

    # 2. Gana Dosha Cancellation
    if calculate_gana(b_n, g_n) == 0:
        # Rule: Same rashi lord or friendship cancels Gana Dosha
        b_lord = RASHI_LORDS[b_r]
        g_lord = RASHI_LORDS[g_r]
        if b_lord == g_lord or PLANET_FRIENDSHIP[b_lord][g_lord] >= 4.0:
            cancellations.append("Gana Dosha cancelled due to Rashi Lord friendship.")
            total_score += 6.0

    # 3. Nadi Dosha Cancellation
    if calculate_nadi(b_n, g_n) == 0:
        # Rule: Different Rashi but same Nakshatra lord (sometimes used)
        # Standard: If Rashi lord is same and Rashi is different
        if b_r != g_r and RASHI_LORDS[b_r] == RASHI_LORDS[g_r]:
            cancellations.append("Nadi Dosha cancelled due to common Rashi Lord.")
            total_score += 8.0

    total_score = min(36.0, total_score)

    # Manglik Check
    b_manglik = is_manglik(boy_chart)
    g_manglik = is_manglik(girl_chart)
    manglik_match = (b_manglik["is_manglik"] == g_manglik["is_manglik"])

    # Deep Comparison: Navamsha & 7th House
    b_d9_lagna = boy_chart.divisional_charts.get("D9", {}).get("Lagna")
    g_d9_lagna = girl_chart.divisional_charts.get("D9", {}).get("Lagna")
    d9_lagna_match = (b_d9_lagna == g_d9_lagna)

    b_7th_lord_name = boy_chart.house_lords[7]
    g_7th_lord_name = girl_chart.house_lords[7]

    b_7th_lord = boy_chart.planets[b_7th_lord_name]
    g_7th_lord = girl_chart.planets[g_7th_lord_name]

    # Compare 7th lord dignities
    lord_harmony = (b_7th_lord.dignity == g_7th_lord.dignity)

    # Mars-Venus association (Pasya/Yoga)
    b_mars = boy_chart.planets["Mars"]
    g_venus = girl_chart.planets["Venus"]
    g_mars = girl_chart.planets["Mars"]
    b_venus = boy_chart.planets["Venus"]

    mars_venus_match = (b_mars.rashi == g_venus.rashi) or (g_mars.rashi == b_venus.rashi)

    results = [{"name": k[0], "score": k[1], "max": k[2], "status": "PASS" if k[1] > (k[2]/2) else "FAIL"} for k in kutas]

    return {
        "total_score": total_score,
        "max_score": 36.0,
        "verdict": "Excellent" if total_score >= 25 else "Good" if total_score >= 18 else "Average" if total_score >= 12 else "Poor",
        "kutas": results,
        "manglik_analysis": {
            "boy": b_manglik,
            "girl": g_manglik,
            "match": manglik_match
        },
        "deep_comparison": {
            "navamsha_lagna_match": d9_lagna_match,
            "seventh_lord_harmony": lord_harmony,
            "boy_7th_lord_dignity": b_7th_lord.dignity,
            "girl_7th_lord_dignity": g_7th_lord.dignity,
            "mars_venus_conjunction": mars_venus_match
        }
    }
