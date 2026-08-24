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

def get_visha_amrit_ghatis(nak_idx: int, nak_start_jd: float, nak_end_jd: float) -> Dict[str, Tuple[float, float]]:
    """
    Visha Ghati (Toxic window) and Amrit Ghati (Nectar window).
    Each lasts 4 ghatikas (96 mins).
    """
    # Visha Ghati start ghatikas for 27 nakshatras
    VISHA_START = {
        0: 50, 1: 24, 2: 30, 3: 40, 4: 14, 5: 21, 6: 30, 7: 20, 8: 32,
        9: 30, 10: 36, 11: 24, 12: 20, 13: 18, 14: 16, 15: 14, 16: 10, 17: 14,
        18: 56, 19: 24, 20: 20, 21: 10, 22: 10, 23: 18, 24: 16, 25: 24, 26: 30
    }

    duration = nak_end_jd - nak_start_jd
    ghatika = duration / 60.0

    results = {}

    v_start_ghatika = VISHA_START.get(nak_idx, 30)
    v_start = nak_start_jd + v_start_ghatika * ghatika
    v_end = v_start + 4 * ghatika
    results["Visha Ghati"] = (v_start, v_end)

    # Amrit Ghati is usually 21 ghatikas after Visha Ghati start (classic rule vary)
    a_start = v_start + 21 * ghatika
    a_end = a_start + 4 * ghatika
    results["Amrit Ghati"] = (a_start, a_end)

    return results

# Event-specific Muhurta Rules
EVENT_MUHURTA_RULES = {
    "Marriage": {
        "nakshatras": [4, 8, 13, 15, 17, 21, 22, 26, 27], # Rohini, Pushya, Hasta, Swati, Anuradha, etc.
        "tithis": [2, 3, 5, 7, 10, 11, 13, 15],
        "weekdays": ["Monday", "Wednesday", "Thursday", "Friday"]
    },
    "Business Opening": {
        "nakshatras": [1, 5, 8, 13, 15, 22, 27], # Ashwini, Mrigashira, Pushya, Hasta, Swati, Shravana, Revati
        "tithis": [1, 2, 3, 5, 10, 11, 13],
        "weekdays": ["Monday", "Wednesday", "Thursday"]
    },
    "Property Purchase": {
        "nakshatras": [4, 9, 11, 13, 15, 18, 26],
        "tithis": [1, 2, 5, 10, 11],
        "weekdays": ["Thursday", "Friday"]
    },
    "Vehicle Purchase": {
        "nakshatras": [1, 4, 5, 8, 13, 15, 22, 27],
        "tithis": [1, 2, 5, 10, 11, 13],
        "weekdays": ["Monday", "Wednesday", "Thursday", "Friday"]
    },
    "Travel": {
        "nakshatras": [1, 4, 5, 7, 8, 13, 15, 17, 21, 22, 27],
        "tithis": [2, 3, 5, 7, 10, 11, 13],
        "weekdays": ["Monday", "Wednesday", "Thursday", "Friday"]
    },
    "Education Start": {
        "nakshatras": [1, 4, 5, 8, 13, 15, 22, 27],
        "tithis": [1, 2, 3, 5, 10, 11],
        "weekdays": ["Wednesday", "Thursday", "Friday"]
    },
    "House Warming (Griha Pravesh)": {
        "nakshatras": [4, 12, 13, 17, 21, 22, 26, 27],
        "tithis": [2, 3, 5, 7, 10, 11, 13],
        "weekdays": ["Monday", "Wednesday", "Thursday", "Friday"]
    },
    "Medical Surgery": {
        "nakshatras": [3, 9, 10, 11, 14, 16, 18, 19, 20, 24, 25], # Hard/Sharp naks for cutting
        "tithis": [4, 9, 14, 8, 12], # Avoiding Rikta if possible, but surgeons often prefer sharp days
        "weekdays": ["Tuesday", "Saturday"] # Mars/Saturn days traditionally used for surgery
    },
    "Legal/Court Case": {
        "nakshatras": [1, 5, 8, 13, 15, 17, 22, 27],
        "tithis": [1, 2, 3, 5, 7, 10, 11],
        "weekdays": ["Tuesday", "Thursday"]
    },
    "Financial Investment": {
        "nakshatras": [4, 5, 8, 13, 15, 22, 27],
        "tithis": [2, 5, 10, 11, 13],
        "weekdays": ["Wednesday", "Thursday", "Friday"]
    },
    "New Job Joining": {
        "nakshatras": [1, 4, 8, 13, 15, 17, 22, 27],
        "tithis": [2, 3, 5, 10, 11, 13],
        "weekdays": ["Monday", "Wednesday", "Thursday"]
    },
    "Travel (International)": {
        "nakshatras": [1, 4, 5, 7, 8, 13, 15, 22, 27],
        "tithis": [2, 3, 5, 7, 10, 11, 13],
        "weekdays": ["Monday", "Thursday", "Friday"]
    }
}

def check_muhurta_suitability(event_type: str, panchang: Dict) -> Dict:
    """Check if the current panchang is suitable for a specific event."""
    rules = EVENT_MUHURTA_RULES.get(event_type)
    if not rules:
        return {"status": "Neutral", "score": 50, "reasons": ["No specific rules for this event."]}

    reasons = []
    score = 50

    # 1. Nakshatra check
    if panchang["nakshatra"]["number"] in rules["nakshatras"]:
        score += 20
        reasons.append(f"Favorable Nakshatra ({panchang['nakshatra']['name']})")
    else:
        score -= 10
        reasons.append("Nakshatra is not ideal.")

    # 2. Tithi check
    if panchang["tithi"]["number"] in rules["tithis"]:
        score += 15
        reasons.append(f"Favorable Tithi ({panchang['tithi']['name']})")
    else:
        score -= 10
        reasons.append("Tithi is not ideal.")

    # 3. Weekday check
    if panchang["vara"]["name"] in rules["weekdays"]:
        score += 15
        reasons.append(f"Favorable Weekday ({panchang['vara']['name']})")

    status = "Auspicious" if score >= 70 else "Moderate" if score >= 50 else "Inauspicious"

    return {
        "status": status,
        "score": score,
        "reasons": reasons
    }
