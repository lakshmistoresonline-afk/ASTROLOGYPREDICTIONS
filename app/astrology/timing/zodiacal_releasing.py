from datetime import datetime, timedelta
from typing import List, Dict, Any

# Rashi Period Years (Zodiacal Releasing)
RASHI_PERIODS = {
    0: 15, # Aries (Mars) - Actually 15
    1: 8,  # Taurus (Venus)
    2: 20, # Gemini (Mercury)
    3: 25, # Cancer (Moon)
    4: 19, # Leo (Sun)
    5: 20, # Virgo (Mercury)
    6: 8,  # Libra (Venus)
    7: 15, # Scorpio (Mars)
    8: 12, # Sagittarius (Jupiter)
    9: 27, # Capricorn (Saturn)
    10: 30, # Aquarius (Saturn)
    11: 12  # Pisces (Jupiter)
}

def calculate_zodiacal_releasing(start_rashi: int, birth_dt: datetime, level: int = 1) -> List[Dict[str, Any]]:
    """
    Zodiacal Releasing for Fortune/Spirit.
    Level 1: Years.
    """
    periods = []
    curr_start = birth_dt
    curr_rashi = start_rashi

    for _ in range(12): # One full cycle of signs
        years = RASHI_PERIODS[curr_rashi]
        curr_end = curr_start + timedelta(days=years * 365.2425)

        periods.append({
            "rashi": curr_rashi,
            "years": years,
            "start": curr_start,
            "end": curr_end
        })

        curr_start = curr_end
        curr_rashi = (curr_rashi + 1) % 12

    return periods
