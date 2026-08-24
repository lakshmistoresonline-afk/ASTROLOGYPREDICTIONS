from typing import Dict, Any

TARA_BALA_MAP = {
    1: ("Janma", "Birth/Self", "Neutral"),
    2: ("Sampat", "Wealth/Prosperity", "Auspicious"),
    3: ("Vipat", "Danger/Obstacles", "Inauspicious"),
    4: ("Kshema", "Well-being/Security", "Auspicious"),
    5: ("Pratyari", "Opposition/Enemies", "Inauspicious"),
    6: ("Sadhaka", "Achievement/Success", "Auspicious"),
    7: ("Vadha", "Danger/Destruction", "Inauspicious"),
    8: ("Mitra", "Friendship/Help", "Auspicious"),
    9: ("Ati-Mitra", "Great Friendship", "Auspicious")
}

def calculate_tarabala(natal_nak_idx: int, transit_nak_idx: int) -> Dict[str, Any]:
    """
    Count from Janma Nakshatra to target Nakshatra.
    Divide by 9, remainder is the Tara.
    """
    # 0-indexed nakshatras (Ashwini=0)
    # Count: Ashwini(0) to Ashwini(0) is 1.
    count = (transit_nak_idx - natal_nak_idx + 27) % 27 + 1
    tara_num = count % 9
    if tara_num == 0: tara_num = 9

    name, meaning, quality = TARA_BALA_MAP[tara_num]

    return {
        "number": tara_num,
        "name": name,
        "meaning": meaning,
        "quality": quality
    }

def calculate_chandrabala(natal_rashi_idx: int, transit_rashi_idx: int) -> Dict[str, Any]:
    """
    Moon's position from natal Moon.
    Favorable: 1, 3, 6, 7, 10, 11
    Wait: Classics differ. Standard: 1, 3, 6, 7, 10, 11 are good.
    Actually: 2, 5, 9 are neutral/moderate. 4, 8, 12 are bad.
    """
    rel_house = (transit_rashi_idx - natal_rashi_idx + 12) % 12 + 1

    good = [1, 3, 6, 7, 10, 11]
    neutral = [2, 5, 9]

    if rel_house in good: quality = "Auspicious"
    elif rel_house in neutral: quality = "Moderate"
    else: quality = "Inauspicious"

    return {
        "house": rel_house,
        "quality": quality
    }
