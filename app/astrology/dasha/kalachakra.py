from typing import Dict, List, Any
from datetime import datetime

# Rashi Years in Kala Chakra
RASHI_YEARS = {
    0: 7,  # Aries
    1: 16, # Taurus
    2: 9,  # Gemini
    3: 21, # Cancer
    4: 5,  # Leo
    5: 9,  # Virgo
    6: 16, # Libra
    7: 7,  # Scorpio
    8: 10, # Sag
    9: 5,  # Capricorn
    10: 11, # Aqua
    11: 10  # Pisces
}

# Sequences for the 9 quarters (Padas) - Simplified Savya
SEQUENCES = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8], # Pada 1
    [9, 10, 11, 7, 6, 5, 4, 3, 2], # Pada 2
    # ... In reality there are 12 signs * 4 padas = 48 variations.
    # We will implement a representative sequence logic.
]

def calculate_kalachakra_dasha(moon_lon: float, birth_dt: datetime) -> Dict[str, Any]:
    """
    Kala Chakra Dasha (Simplified Foundation).
    Based on Moon's Navamsha position.
    """
    # 1. Determine Pada (1-108)
    from ..core.planets import NAK_SPAN
    pada_idx = int(moon_lon / (NAK_SPAN / 4))

    # 2. Determine if Savya or Apasavya
    # Simplified: First 3 naks are Savya, next 3 Apasavya
    is_savya = (pada_idx // 36) % 2 == 0

    # 3. Determine starting Rashi of cycle
    # (Highly complex rashi jump logic needed for full accuracy)
    # We'll provide the 'Deha' and 'Jiva' indicators.

    deha_rashi = 0 # Aries (Start of body)
    jiva_rashi = 11 # Pisces (Soul)

    mahadashas = []
    current_start = birth_dt

    # Representative 9-rashi cycle
    cycle = [0, 1, 2, 3, 4, 5, 6, 7, 8] if is_savya else [11, 10, 9, 8, 7, 6, 5, 4, 3]

    for r in cycle:
        dur = RASHI_YEARS[r]
        end = current_start.replace(year=current_start.year + dur)
        mahadashas.append({
            "rashi_idx": r,
            "duration": dur,
            "start": current_start,
            "end": end
        })
        current_start = end

    return {
        "is_savya": is_savya,
        "mahadashas": mahadashas,
        "deha_rashi_idx": deha_rashi,
        "jiva_rashi_idx": jiva_rashi
    }
