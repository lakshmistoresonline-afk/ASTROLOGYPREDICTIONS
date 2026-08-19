from datetime import datetime, time, timedelta
from typing import List, Dict, Optional, Tuple

CHOGHADIYA_ORDER_DAY = [
    "Udveg", "Chara", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"
]
CHOGHADIYA_ORDER_NIGHT = [
    "Shubh", "Amrit", "Chara", "Rog", "Kaal", "Labh", "Udveg", "Shubh"
]

# Sunday=0, Monday=1, ...
DAY_START_MAP = {
    0: 0, # Sun starts with Udveg
    1: 3, # Mon starts with Amrit
    2: 7, # Tue starts with Udveg
    3: 1, # Wed starts with Chara
    4: 5, # Thu starts with Shubh
    5: 2, # Fri starts with Labh
    6: 4, # Sat starts with Kaal
}

# Amrit Kaal starting ghatikas for each Nakshatra (1-27)
AMRIT_KAAL_START = {
    1: 42, 2: 48, 3: 54, 4: 52, 5: 38, 6: 35, 7: 54, 8: 42, 9: 56,
    10: 54, 11: 44, 12: 48, 13: 45, 14: 45, 15: 43, 16: 48, 17: 54, 18: 52,
    19: 52, 20: 50, 21: 46, 22: 54, 23: 52, 24: 54, 25: 42, 26: 48, 27: 48
}

def get_choghadiya(sunrise_jd: float, sunset_jd: float, next_sunrise_jd: float, weekday: int) -> List[Dict]:
    """Calculate day and night Choghadiyas."""
    # 1. Day Choghadiya
    day_span = (sunset_jd - sunrise_jd) / 8.0
    start_idx = DAY_START_MAP[weekday]

    day_periods = []
    for i in range(8):
        name = CHOGHADIYA_ORDER_DAY[(start_idx + i) % 7]
        day_periods.append({
            "name": name,
            "start_jd": sunrise_jd + i * day_span,
            "end_jd": sunrise_jd + (i+1) * day_span,
            "type": "Day"
        })

    # 2. Night Choghadiya
    night_span = (next_sunrise_jd - sunset_jd) / 8.0
    night_start_idx = (start_idx + 5) % 7

    night_periods = []
    for i in range(8):
        name = CHOGHADIYA_ORDER_NIGHT[(night_start_idx + i) % 7]
        night_periods.append({
            "name": name,
            "start_jd": sunset_jd + i * night_span,
            "end_jd": sunset_jd + (i+1) * night_span,
            "type": "Night"
        })

    return day_periods + night_periods

def get_abhijit_muhurta(sunrise_jd: float, sunset_jd: float) -> Tuple[float, float]:
    """Calculate Abhijit Muhurta (Solar Noon +/- 24 mins approx)."""
    # Duration of day divided by 15 muhurtas (each ~48 mins)
    # Abhijit is the 8th muhurta
    muhurta_duration = (sunset_jd - sunrise_jd) / 15.0
    start = sunrise_jd + 7 * muhurta_duration
    end = sunrise_jd + 8 * muhurta_duration
    return start, end

def get_brahma_muhurta(sunrise_jd: float, sunset_jd: float) -> Tuple[float, float]:
    """Calculate Brahma Muhurta (Starts 96 mins before sunrise)."""
    # Usually calculated based on the previous night's duration
    # Simplified: 2 muhurtas (96 mins) before sunrise
    muhurta_duration = 48.0 / 1440.0 # Standard 48 mins in JD
    start = sunrise_jd - 2 * muhurta_duration
    end = sunrise_jd - muhurta_duration
    return start, end

def get_amrit_kaal(nak_num: int, start_jd: float, end_jd: float) -> Optional[Tuple[float, float]]:
    """Calculate Amrit Kaal window for a given nakshatra."""
    if nak_num not in AMRIT_KAAL_START:
        return None

    duration = end_jd - start_jd
    # 60 ghatikas in a nakshatra duration
    ghatika = duration / 60.0

    start = start_jd + AMRIT_KAAL_START[nak_num] * ghatika
    # Amrit Kaal duration is 4 ghatikas
    end = start + 4 * ghatika

    return start, end
