from typing import Dict, Any, List
from .data import (
    NAKSHATRA_GANA, NAKSHATRA_YONI, NAKSHATRA_NADI,
    YONI_SCORE_TABLE, RASHI_VARNA, RASHI_VASHYA,
    PLANET_FRIENDSHIP, RASHI_LORDS
)

def calculate_varna(boy_rashi: int, girl_rashi: int) -> float:
    b_v = RASHI_VARNA[boy_rashi]
    g_v = RASHI_VARNA[girl_rashi]
    # Hierarchy: 0 (Brahmin) > 1 (Kshatriya) > 2 (Vaishya) > 3 (Shudra)
    # Higher rank has lower index
    if b_v <= g_v:
        return 1.0
    return 0.0

def calculate_vashya(boy_rashi: int, girl_rashi: int) -> float:
    b_v = RASHI_VASHYA[boy_rashi]
    g_v = RASHI_VASHYA[girl_rashi]

    if b_v == g_v: return 2.0

    # Specific rules for Vashya compatibility
    # This is a simplified version
    vashya_map = {
        "Chatushpad": ["Manav", "Jalchar"],
        "Manav": ["Chatushpad", "Keet"],
        "Jalchar": ["Chatushpad", "Manav"],
        "Keet": ["Manav"],
        "Vananchar": [] # Not in my basic rashi mapping
    }

    if g_v in vashya_map.get(b_v, []):
        return 1.0
    return 0.0

def calculate_tara(boy_nak: int, girl_nak: int) -> float:
    # Tara is calculated both ways
    # 1. Girl to Boy
    diff1 = (boy_nak - girl_nak + 27) % 9
    # 2. Boy to Girl
    diff2 = (girl_nak - boy_nak + 27) % 9

    bad_tara = [3, 5, 7] # Vipat, Pratyari, Vadha

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

    score = PLANET_FRIENDSHIP[b_l][g_l]
    return float(score)

def calculate_gana(boy_nak: int, girl_nak: int) -> float:
    b_g = NAKSHATRA_GANA[boy_nak]
    g_g = NAKSHATRA_GANA[girl_nak]

    if b_g == g_g: return 6.0
    if b_g == "Deva" and g_g == "Manushya": return 6.0
    if b_g == "Manushya" and g_g == "Deva": return 5.0
    if b_g == "Rakshasa" or g_g == "Rakshasa":
        if (b_g == "Deva" and g_g == "Rakshasa") or (b_g == "Rakshasa" and g_g == "Deva"):
            return 0.0
        return 1.0 # One is Rakshasa, other is Manushya
    return 0.0

def calculate_bhakut(boy_rashi: int, girl_rashi: int) -> float:
    diff = (boy_rashi - girl_rashi + 12) % 12 + 1
    # 2-12, 5-9, 6-8 are considered Bhakut Dosha
    bad_diffs = [2, 12, 5, 9, 6, 8]
    if diff in bad_diffs:
        return 0.0
    return 7.0

def calculate_nadi(boy_nak: int, girl_nak: int) -> float:
    b_n = NAKSHATRA_NADI[boy_nak]
    g_n = NAKSHATRA_NADI[girl_nak]

    if b_n == g_n:
        return 0.0
    return 8.0

def get_matchmaking_score(boy_data: Dict[str, Any], girl_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    boy_data/girl_data: { "rashi": int, "nakshatra_idx": int }
    """
    b_r = boy_data["rashi"]
    b_n = boy_data["nakshatra_idx"]
    g_r = girl_data["rashi"]
    g_n = girl_data["nakshatra_idx"]

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

    results = []
    for name, score, max_score in kutas:
        results.append({
            "name": name,
            "score": score,
            "max": max_score,
            "status": "PASS" if score > (max_score / 2) else "FAIL"
        })

    verdict = "Excellent" if total_score >= 25 else \
              "Good" if total_score >= 18 else \
              "Average" if total_score >= 12 else "Poor"

    # Flag Doshas
    doshas = []
    if calculate_nadi(b_n, g_n) == 0:
        doshas.append("Nadi Dosha")
    if calculate_bhakut(b_r, g_r) == 0:
        doshas.append("Bhakut Dosha")

    return {
        "total_score": total_score,
        "max_score": 36.0,
        "verdict": verdict,
        "kutas": results,
        "doshas": doshas
    }
