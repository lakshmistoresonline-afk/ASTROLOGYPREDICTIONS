from typing import Callable

def find_event(start_jd: float, end_jd: float, func: Callable[[float], float], target: float, tolerance: float = 1e-6) -> float:
    # ... (existing implementation)
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
