from typing import Callable

def find_event(start_jd: float, end_jd: float, func: Callable[[float], float], target: float, tolerance: float = 1e-6) -> float:
    """
    Find the JD where func(jd) == target using bisection method.
    Assumes func is monotonic in the interval [start_jd, end_jd].
    """
    low = start_jd
    high = end_jd

    # Normalize angles if necessary
    def get_val(jd):
        val = func(jd)
        diff = (val - target + 180) % 360 - 180
        return diff

    v_low = get_val(low)
    v_high = get_val(high)

    if v_low * v_high > 0:
        # Not crossing target in this interval or not monotonic
        return -1.0

    for _ in range(50): # Max iterations
        mid = (low + high) / 2
        v_mid = get_val(mid)
        if abs(v_mid) < tolerance:
            return mid
        if v_low * v_mid < 0:
            high = mid
            v_high = v_mid
        else:
            low = mid
            v_low = v_mid
    return (low + high) / 2

def calculate_tarabala(transit_nak: int, birth_nak: int) -> dict:
    TARABALA_NAMES = [
        "Janma", "Sampat", "Vipat", "Kshema", "Pratyak",
        "Sadhana", "Naidhana", "Mitra", "Parama Mitra",
    ]
    TARABALA_NATURE = {
        "Janma": "Neutral", "Sampat": "Auspicious", "Vipat": "Inauspicious",
        "Kshema": "Auspicious", "Pratyak": "Inauspicious", "Sadhana": "Auspicious",
        "Naidhana": "Inauspicious", "Mitra": "Auspicious", "Parama Mitra": "Highly Auspicious",
    }
    count = ((transit_nak - birth_nak) % 27) + 1
    tarabala_idx = ((count - 1) % 9)
    name = TARABALA_NAMES[tarabala_idx]
    return {
        "count": count,
        "name": name,
        "quality": TARABALA_NATURE.get(name, "Neutral")
    }

def calculate_chandra_bala(transit_moon_rashi: int, birth_moon_rashi: int) -> dict:
    count = ((transit_moon_rashi - birth_moon_rashi) % 12) + 1
    favourable = count in (1, 3, 6, 7, 10, 11)
    return {
        "count": count,
        "is_favourable": favourable,
        "quality": "Favorable" if favourable else "Unfavorable"
    }

def check_dagdha_tithi(tithi_num: int, weekday: int) -> bool:
    """
    Dagdha Tithi (Burnt Tithi): Specific weekday-tithi combinations.
    Weekday: 0=Mon, 6=Sun
    """
    # 1-indexed tithi in paksha (1-15)
    t = (tithi_num - 1) % 15 + 1
    mapping = {
        6: [12],    # Sun: 12th
        0: [11],    # Mon: 11th
        1: [5],     # Tue: 5th
        2: [3],     # Wed: 3rd
        3: [6],     # Thu: 6th
        4: [8],     # Fri: 8th
        5: [9]      # Sat: 9th
    }
    return t in mapping.get(weekday, [])
