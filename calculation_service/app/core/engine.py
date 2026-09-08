import swisseph as swe
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

# Initialize Ephemeris Path
EPHE_PATH = os.getenv("SE_EPHE_PATH", "/app/ephe")
if os.path.exists(EPHE_PATH):
    swe.set_ephe_path(EPHE_PATH)

AYANAMSA_MAP = {
    "LAHIRI": swe.SIDM_LAHIRI,
    "RAMAN": swe.SIDM_RAMAN,
    "KP": swe.SIDM_KRISHNAMURTI
}

PLANET_IDS = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
    "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE
}

def calculate_natal_chart(year: int, month: int, day: int, hour: float, lat: float, lon: float, ayanamsa_name: str = "LAHIRI"):
    swe.set_sid_mode(AYANAMSA_MAP.get(ayanamsa_name, swe.SIDM_LAHIRI))
    jd_ut = swe.julday(year, month, day, hour)
    swe.set_topo(lon, lat, 0.0)
    # Handle potential 3rd return value (error message) in some swisseph forks
    h_res = swe.houses_ex(jd_ut, lat, lon, b'P', swe.FLG_SIDEREAL)
    cusps, ascmc = h_res[0], h_res[1]
    ascendant = ascmc[0]

    planets = {}
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_TOPOCTR

    for name, pid in PLANET_IDS.items():
        c_res = swe.calc_ut(jd_ut, pid, flags)
        res, ret_flag = c_res[0], c_res[1]
        planets[name] = {
            "longitude": res[0], "latitude": res[1],
            "speed": res[3], "is_retrograde": res[3] < 0
        }
    planets["Ketu"] = {
        "longitude": (planets["Rahu"]["longitude"] + 180) % 360,
        "latitude": -planets["Rahu"]["latitude"],
        "speed": planets["Rahu"]["speed"], "is_retrograde": planets["Rahu"]["is_retrograde"]
    }
    return {
        "jd_ut": jd_ut, "ayanamsa": swe.get_ayanamsa_ut(jd_ut),
        "ascendant": ascendant, "planets": planets, "houses": list(cusps[1:13])
    }

def calculate_transits_for_range(start_date: str, end_date: str, lat: float, lon: float):
    """
    High-Precision Range Scanning (Phase 3).
    Returns daily positions for major planets.
    """
    dt_start = datetime.strptime(start_date, "%Y-%m-%d")
    dt_end = datetime.strptime(end_date, "%Y-%m-%d")

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    swe.set_topo(lon, lat, 0.0)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED | swe.FLG_TOPOCTR

    results = []
    curr = dt_start
    while curr <= dt_end:
        jd = swe.julday(curr.year, curr.month, curr.day, 12.0) # Noon UT
        day_data = {"date": curr.strftime("%Y-%m-%d"), "planets": {}}
        for name, pid in PLANET_IDS.items():
            c_res = swe.calc_ut(jd, pid, flags)
            res = c_res[0]
            day_data["planets"][name] = {"lon": res[0], "is_retrograde": res[3] < 0}
        results.append(day_data)
        curr += timedelta(days=1)

    return results

def calculate_dasha(moon_lon: float, birth_year: int, birth_month: int, birth_day: int, birth_hour: float):
    NAK_SPAN = 360/27
    nak_idx = int(moon_lon / NAK_SPAN)
    rem_deg = NAK_SPAN - (moon_lon % NAK_SPAN)
    return {"moon_nakshatra_index": nak_idx, "remaining_degrees": rem_deg, "nak_span": NAK_SPAN}

def calculate_sky_events(jd_ut: float, lat: float, lon: float):
    """
    Calculate Sunrise and Sunset for a given JD and location.
    Using standard astronomical definitions (pyswisseph).
    """
    atpress = 1013.25
    attemp = 15.0

    # Rise = 1, Set = 2
    res_rise = swe.rise_trans(jd_ut, swe.SUN, 1, (lon, lat, 0.0), atpress, attemp, 0)
    res_set = swe.rise_trans(jd_ut, swe.SUN, 2, (lon, lat, 0.0), atpress, attemp, 0)

    sr_jd = res_rise[1][0] if res_rise[0] == 0 else None
    ss_jd = res_set[1][0] if res_set[0] == 0 else None

    return {"sunrise_jd": sr_jd, "sunset_jd": ss_jd}
