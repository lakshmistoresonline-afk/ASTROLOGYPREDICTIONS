from datetime import datetime, date, timedelta
from typing import List, Dict
import swisseph as swe
from ..core.ephemeris import get_planet_position, get_julian_day

def calculate_sade_sati(natal_moon_rashi: int) -> List[Dict]:
    """
    Calculate Sade Sati phases for the next 30 years.
    Sade Sati occurs when Saturn is in the sign before, same as, or after the Natal Moon.
    """
    results = []
    today = date.today()

    # Signs of interest
    s_before = (natal_moon_rashi - 1 + 12) % 12
    s_during = natal_moon_rashi
    s_after  = (natal_moon_rashi + 1) % 12

    ss_signs = {s_before: "Phase 1: Rising", s_during: "Phase 2: Peak", s_after: "Phase 3: Setting"}

    # Scan next 30 years month by month
    current_phase = None
    phase_start = None

    for month_offset in range(30 * 12):
        check_date = today + timedelta(days=month_offset * 30)
        jd = get_julian_day(check_date.year, check_date.month, check_date.day, 12.0)

        saturn_pos = get_planet_position(jd, swe.SATURN)
        sat_rashi = int(saturn_pos["longitude"] / 30)

        detected_phase = ss_signs.get(sat_rashi)

        if detected_phase != current_phase:
            if current_phase:
                results.append({
                    "phase": current_phase,
                    "start": phase_start.strftime("%b %Y"),
                    "end": check_date.strftime("%b %Y")
                })
            current_phase = detected_phase
            phase_start = check_date

    return results

def get_shani_status(natal_moon_rashi: int, natal_asc_rashi: int) -> Dict:
    """Check current Saturn status: Sade Sati, Dhaiya, Ashtama Shani."""
    jd_now = swe.julday(datetime.now().year, datetime.now().month, datetime.now().day, 12.0)
    sat_pos = get_planet_position(jd_now, swe.SATURN)
    sat_rashi = int(sat_pos["longitude"] / 30)

    # 1. Sade Sati
    diff_moon = (sat_rashi - natal_moon_rashi + 12) % 12
    ss_status = None
    if diff_moon == 11: ss_status = "Phase 1: Rising"
    elif diff_moon == 0: ss_status = "Phase 2: Peak"
    elif diff_moon == 1: ss_status = "Phase 3: Setting"

    # 2. Dhaiya (4th or 8th from Moon)
    dhaiya = None
    if diff_moon == 3: dhaiya = "Artha-Ashtama Shani (4th from Moon)"
    elif diff_moon == 7: dhaiya = "Ashtama Shani (8th from Moon)"

    # 3. Kantaka Shani (1st, 4th, 8th, 10th from Lagna)
    diff_lagna = (sat_rashi - natal_asc_rashi + 12) % 12
    kantaka = None
    if diff_lagna == 0: kantaka = "Kantaka Shani (Over Lagna)"
    elif diff_lagna == 3: kantaka = "Kantaka Shani (4th house)"
    elif diff_lagna == 7: kantaka = "Kantaka Shani (8th house)"
    elif diff_lagna == 9: kantaka = "Kantaka Shani (10th house)"

    return {
        "saturn_rashi": sat_rashi,
        "sade_sati": ss_status,
        "dhaiya": dhaiya,
        "kantaka": kantaka,
        "is_heavy": any([ss_status, dhaiya, kantaka])
    }
