from typing import Dict, Any, Optional
from .swe_proxy import swe
from .ephemeris import get_planet_position

# Segment order for Day/Night parts (0-7 segments)
DAY_SAT_SEGMENT = { 0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1 }
NIGHT_SAT_SEGMENT = { 0: 3, 1: 2, 2: 1, 3: 7, 4: 6, 5: 5, 6: 4 }

def calculate_upagrahas(jd_ut: float, sr_jd: float, ss_jd: float, next_sr_jd: float, weekday: int) -> Dict[str, float]:
    """
    Calculate Gulika and Mandi longitudes.
    """
    if sr_jd is None or ss_jd is None or next_sr_jd is None:
        raise ValueError("Sunrise/Sunset data required for Upagraha calculation.")

    is_day = sr_jd <= jd_ut <= ss_jd

    if is_day:
        duration = ss_jd - sr_jd
        start_jd = sr_jd
        seg_num = DAY_SAT_SEGMENT.get(weekday, 7)
    else:
        if jd_ut < sr_jd:
            # Approx using previous cycle
            prev_ss = sr_jd - (ss_jd - sr_jd)
            duration = sr_jd - prev_ss
            start_jd = prev_ss
        else:
            duration = next_sr_jd - ss_jd
            start_jd = ss_jd
        seg_num = NIGHT_SAT_SEGMENT.get(weekday, 3)

    seg_duration = duration / 8.0
    gulika_jd = start_jd + (seg_num - 1) * seg_duration
    return {"gulika_jd": gulika_jd}

def get_upagraha_longitudes(jd_ut: float, sr_jd: float, ss_jd: float, next_sr_jd: float, weekday: int, lat: float, lon: float) -> Dict[str, float]:
    from .houses import get_houses
    data = calculate_upagrahas(jd_ut, sr_jd, ss_jd, next_sr_jd, weekday)
    g_jd = data["gulika_jd"]
    h_data = get_houses(g_jd, lat, lon)
    gulika_lon = h_data["ascendant"]
    return {
        "Gulika": gulika_lon,
        "Mandi": (gulika_lon + 0.5) % 360 # Systematic offset per Parashara
    }
