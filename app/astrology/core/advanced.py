from typing import Dict, List, Any, Tuple
from .houses import RASHI_LORDS
import math

def calculate_arudha_padas(asc_rashi: int, house_lords: Dict[int, str], planets: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculate Arudha Padas for all 12 houses.
    """
    arudhas = {}
    house_to_rashi = {h: (asc_rashi + h - 1) % 12 for h in range(1, 13)}

    for h in range(1, 13):
        h_rashi = house_to_rashi[h]
        lord_name = house_lords[h]
        lord_rashi = planets[lord_name].rashi
        dist = (lord_rashi - h_rashi + 12) % 12
        arudha = (lord_rashi + dist) % 12
        if arudha == h_rashi or arudha == (h_rashi + 6) % 12:
            arudha = (arudha + 9) % 12
        name = "AL" if h == 1 else f"A{h}"
        arudhas[name] = arudha
    return arudhas

def get_jaimini_aspects(rashi: int) -> List[int]:
    movable, fixed, dual = [0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8, 11]
    if rashi in movable:
        return [r for r in fixed if r != (rashi + 1) % 12]
    elif rashi in fixed:
        return [r for r in movable if r != (rashi - 1 + 12) % 12]
    else: return [r for r in dual if r != rashi]

def calculate_yogi_avayogi(sun_lon: float, moon_lon: float) -> Dict[str, str]:
    yogi_point = (sun_lon + moon_lon + 93.333333) % 360
    from .planets import NAKSHATRA_LORDS, NAK_SPAN
    idx = int(yogi_point / NAK_SPAN)
    yogi_lord = NAKSHATRA_LORDS[idx]
    avayogi_lord = NAKSHATRA_LORDS[(idx + 6) % 27]
    saha_yogi = RASHI_LORDS[int(yogi_point // 30)]
    return {
        "Yogi": yogi_lord, "Avayogi": avayogi_lord, "Saha Yogi": saha_yogi,
        "Yogi Point": f"{round(yogi_point, 2)}°"
    }

def calculate_indu_lagna(planets: Dict[str, Any], house_lords: Dict[int, str]) -> float:
    UNIT_POINTS = {"Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8, "Jupiter": 10, "Venus": 12, "Saturn": 1}
    pts1 = UNIT_POINTS.get(house_lords[9], 0)
    moon_rashi = planets["Moon"].rashi
    m9_lord = RASHI_LORDS[(moon_rashi + 8) % 12]
    pts2 = UNIT_POINTS.get(m9_lord, 0)
    rem = (pts1 + pts2) % 12
    if rem == 0: rem = 12
    return float(((moon_rashi + rem - 1) % 12) * 30)

def calculate_special_lagnas(birth_jd: float, sunrise_jd: float, sun_lon: float) -> Dict[str, float]:
    if sunrise_jd is None:
        raise ValueError("Sunrise data required for Special Lagna calculation.")
    diff_hours = (birth_jd - sunrise_jd) * 24.0
    return {
        "Hora Lagna": (sun_lon + diff_hours * 30.0) % 360,
        "Ghati Lagna": (sun_lon + (diff_hours / 0.4) * 30.0) % 360,
        "Bhava Lagna": (sun_lon + (diff_hours / 2.0) * 30.0) % 360,
        "Pranapada Lagna": (sun_lon + (diff_hours / 0.25) * 30.0) % 360
    }

def calculate_varnada_lagna(asc_rashi: int, hora_lagna_rashi: int) -> Dict[int, int]:
    def get_v(r1, r2):
        if (r1 % 2 == 0) == (r2 % 2 == 0): return (r1 + r2) % 12
        else: return (r1 - r2 + 12) % 12
    v1 = get_v(asc_rashi, hora_lagna_rashi)
    res = {1: v1}
    for h in range(2, 13): res[h] = (v1 + h - 1) % 12
    return res

def calculate_shree_lagna(moon_lon: float, asc_lon: float) -> float:
    """Project the fractional degree of Moon within its Nakshatra from the Lagna."""
    from .planets import NAK_SPAN
    return (asc_lon + (moon_lon % NAK_SPAN) / NAK_SPAN * 360) % 360
