from typing import Dict, Any, Optional
from .swe_proxy import swe
from .ephemeris import get_planet_position

# Segment order for Day/Night parts (0-7 segments)
# Sunday=6, Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4, Saturday=5 in Python weekday()
# But let's map them to 0=Sunday for traditional logic
DAY_SAT_SEGMENT = {
    0: 7, # Sun (Saturn is 7th)
    1: 6, # Mon
    2: 5, # Tue
    3: 4, # Wed
    4: 3, # Thu
    5: 2, # Fri
    6: 1  # Sat
}

NIGHT_SAT_SEGMENT = {
    0: 3, # Sun Night
    1: 2, # Mon
    2: 1, # Tue
    3: 7, # Wed
    4: 6, # Thu
    5: 5, # Fri
    6: 4  # Sat
}

def calculate_upagrahas(jd_ut: float, sr_jd: float, ss_jd: float, next_sr_jd: float, weekday: int) -> Dict[str, float]:
    """
    Calculate Gulika and Mandi longitudes.
    sr = sunrise, ss = sunset
    weekday: 0=Sunday, 1=Monday...
    """
    # Handle missing ephemeris data (Mock Mode)
    if sr_jd is None or ss_jd is None or next_sr_jd is None:
        return {"gulika_jd": jd_ut}

    is_day = sr_jd <= jd_ut <= ss_jd

    if is_day:
        duration = ss_jd - sr_jd
        start_jd = sr_jd
        seg_num = DAY_SAT_SEGMENT.get(weekday, 7)
    else:
        # Determine which night part
        if jd_ut < sr_jd: # Early morning before sunrise
            # Use previous sunset (approx)
            prev_ss = sr_jd - (ss_jd - sr_jd) # Placeholder
            duration = sr_jd - prev_ss
            start_jd = prev_ss
        else:
            duration = next_sr_jd - ss_jd
            start_jd = ss_jd
        seg_num = NIGHT_SAT_SEGMENT.get(weekday, 3)

    seg_duration = duration / 8.0
    # Gulika is the degree of Lagna at the start of Saturn's segment
    gulika_jd = start_jd + (seg_num - 1) * seg_duration

    return {"gulika_jd": gulika_jd}

def get_upagraha_longitudes(jd_ut: float, sr_jd: float, ss_jd: float, next_sr_jd: float, weekday: int, lat: float, lon: float) -> Dict[str, float]:
    from .houses import get_houses

    data = calculate_upagrahas(jd_ut, sr_jd, ss_jd, next_sr_jd, weekday)
    g_jd = data["gulika_jd"]

    # Lagna at g_jd
    h_data = get_houses(g_jd, lat, lon)
    gulika_lon = h_data["ascendant"]

    # Mandi is often considered same or slightly offset
    # In some systems, Mandi = Gulika. In others, they differ.
    return {
        "Gulika": gulika_lon,
        "Mandi": (gulika_lon + 1.5) % 360 # Placeholder offset for Mandi if treated as distinct
    }
