from typing import Dict, List, Any, Tuple
from .houses import RASHI_LORDS
import math

def calculate_arudha_padas(asc_rashi: int, house_lords: Dict[int, str], planets: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculate Arudha Padas for all 12 houses.
    Rule: Lord of House is X signs away from House. Arudha is X signs away from Lord.
    Exception: If Arudha falls in House itself, move 10 signs. If in 7th from house, move 10 signs.
    """
    arudhas = {}

    # Sign index where each house starts (Whole Sign)
    house_to_rashi = {h: (asc_rashi + h - 1) % 12 for h in range(1, 13)}

    for h in range(1, 13):
        h_rashi = house_to_rashi[h]
        lord_name = house_lords[h]
        lord_rashi = planets[lord_name].rashi

        # Distance from House to Lord
        dist = (lord_rashi - h_rashi + 12) % 12

        # Arudha is 'dist' signs away from Lord
        arudha = (lord_rashi + dist) % 12

        # Apply exceptions (Standard Parashari/Jaimini)
        if arudha == h_rashi:
            arudha = (arudha + 9) % 12 # Move 10 signs (index + 9)
        elif arudha == (h_rashi + 6) % 12:
            arudha = (arudha + 9) % 12

        name = "AL" if h == 1 else f"A{h}"
        arudhas[name] = arudha

    return arudhas

def get_jaimini_aspects(rashi: int) -> List[int]:
    """
    Movable (0,3,6,9) aspect Fixed (1,4,7,10) except adjacent.
    Fixed (1,4,7,10) aspect Movable (0,3,6,9) except adjacent.
    Dual (2,5,8,11) aspect each other.
    """
    movable = [0, 3, 6, 9]
    fixed = [1, 4, 7, 10]
    dual = [2, 5, 8, 11]

    if rashi in movable:
        # Aspect all fixed signs except the adjacent one
        # Adjacent are rashi+1
        targets = [r for r in fixed if r != (rashi + 1) % 12]
        return targets
    elif rashi in fixed:
        # Aspect all movable signs except the adjacent one
        # Adjacent are rashi-1
        targets = [r for r in movable if r != (rashi - 1 + 12) % 12]
        return targets
    else: # Dual
        return [r for r in dual if r != rashi]

def calculate_yogi_avayogi(sun_lon: float, moon_lon: float) -> Dict[str, str]:
    """
    Yogi Point = Sun + Moon + 93° 20' (Pushya Nakshatra constant)
    Yogi Planet = Lord of Nakshatra where Yogi Point falls.
    Avayogi Planet = 6th Nakshatra from Yogi Nakshatra.
    """
    yogi_point = (sun_lon + moon_lon + 93.333333) % 360

    from .planets import NAKSHATRA_LORDS, NAK_SPAN
    idx = int(yogi_point / NAK_SPAN)
    yogi_lord = NAKSHATRA_LORDS[idx]

    avayogi_idx = (idx + 6) % 27
    avayogi_lord = NAKSHATRA_LORDS[avayogi_idx]

    # Saha Yogi: Lord of Sign where Yogi Point falls
    rashi_idx = int(yogi_point // 30)
    saha_yogi = RASHI_LORDS[rashi_idx]

    return {
        "Yogi": yogi_lord,
        "Avayogi": avayogi_lord,
        "Saha Yogi": saha_yogi,
        "Yogi Point": f"{round(yogi_point, 2)}°"
    }

def analyze_argala(house: int, planets_house_map: Dict[str, int]) -> Dict[str, List[int]]:
    """
    Primary Argala: 2, 4, 11 from house.
    Obstructing (Virodh): 12, 10, 3.
    Secondary Argala: 5. Obstructing: 9.
    Returns sign indices.
    """
    # house here is 1-indexed house number from Lagna
    # we convert to relative house numbers
    def get_rel(h_num, dist):
        return (h_num + dist - 2) % 12 + 1

    argala = {
        "primary": [get_rel(house, 2), get_rel(house, 4), get_rel(house, 11)],
        "secondary": [get_rel(house, 5)],
        "obstructing": [get_rel(house, 12), get_rel(house, 10), get_rel(house, 3), get_rel(house, 9)]
    }
    return argala

def calculate_indu_lagna(planets: Dict[str, Any], house_lords: Dict[int, str]) -> float:
    """
    Indu Lagna (Wealth Point):
    Points: Sun=30, Moon=16, Mars=6, Merc=8, Jup=10, Ven=12, Sat=1.
    Sum points of 9th lord from Lagna and 9th lord from Moon.
    Divide by 12, remainder is signs from Moon.
    """
    UNIT_POINTS = {"Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8, "Jupiter": 10, "Venus": 12, "Saturn": 1}

    # 9th lord from Lagna
    l9_name = house_lords[9]
    pts1 = UNIT_POINTS.get(l9_name, 0)

    # 9th lord from Moon
    moon_rashi = planets["Moon"].rashi
    # 9th from Moon
    m9_rashi = (moon_rashi + 8) % 12
    m9_lord = RASHI_LORDS[m9_rashi]
    pts2 = UNIT_POINTS.get(m9_lord, 0)

    total = pts1 + pts2
    rem = total % 12
    if rem == 0: rem = 12

    # Indu Lagna is 'rem' signs from Moon
    il_rashi = (moon_rashi + rem - 1) % 12
    return float(il_rashi * 30) # Return start of rashi

def calculate_dagtha_rashis(tithi_num: int) -> List[int]:
    """Signs that are 'burnt' or 'dead' based on the Tithi."""
    # Tithi is 1-30 (1-15 Shukla, 16-30 Krishna)
    # Mapping for Shukla/Krishna same numbers
    t = (tithi_num - 1) % 15 + 1

    dagtha = {
        1: [8, 11], # Dhanu, Meena
        2: [11, 0], # Meena, Mesha (Wait, classics differ slightly, using standard)
        3: [1, 10], # Vrishabha, Kumbha
        4: [2, 5],  # Mithuna, Kanya
        5: [3, 9],  # Karka, Makara
        6: [4, 8],  # Simha, Dhanu
        7: [5, 11], # Kanya, Meena
        8: [2, 5],  # Mithuna, Kanya
        9: [4, 7],  # Simha, Vrishchika
        10: [7, 10], # Vrishchika, Kumbha
        11: [8, 11], # Dhanu, Meena
        12: [1, 10], # Vrishabha, Kumbha
        13: [7, 0],  # Vrishchika, Mesha
        14: [2, 5, 8, 11], # Dual signs
        15: [] # Full moon/New moon none
    }
    return dagtha.get(t, [])

def calculate_special_lagnas(birth_jd: float, sunrise_jd: float, sun_lon: float) -> Dict[str, float]:
    """HL = Hora Lagna, GL = Ghati Lagna, PL = Pranapada Lagna, BL = Bhava Lagna."""
    # Handle missing ephemeris data (Mock Mode)
    if sunrise_jd is None:
        return {"Hora Lagna": sun_lon, "Ghati Lagna": sun_lon, "Bhava Lagna": sun_lon, "Pranapada Lagna": sun_lon}

    # Time elapsed in decimal days
    diff = birth_jd - sunrise_jd
    # Convert to hours (1 day = 24 hours)
    diff_hours = diff * 24.0

    # Hora Lagna: 1 sign per hour
    hl = (sun_lon + diff_hours * 30.0) % 360

    # Ghati Lagna: 1 sign per ghati (24 mins = 0.4 hours)
    gl = (sun_lon + (diff_hours / 0.4) * 30.0) % 360

    # Bhava Lagna: 1 sign per 2 hours (approx)
    bl = (sun_lon + (diff_hours / 2.0) * 30.0) % 360

    # Pranapada Lagna:
    # Calculate Sun position at sunrise (simplified: natal sun)
    # (birth time - sunrise) in seconds * 15 / 15 ... complex formula
    # PL = (Sun + time_diff * constant) % 360
    # Rule: 1 sign per 15 mins (roughly)
    pl = (sun_lon + (diff_hours / 0.25) * 30.0) % 360

    return {
        "Hora Lagna": hl,
        "Ghati Lagna": gl,
        "Bhava Lagna": bl,
        "Pranapada Lagna": pl
    }

def calculate_shree_lagna(moon_lon: float, asc_lon: float) -> float:
    """
    Shree Lagna: Project the fractional degree of Moon within its Nakshatra from the Lagna.
    Used specifically for Wealth and Prosperity.
    """
    from .planets import NAK_SPAN
    deg_in_nak = moon_lon % NAK_SPAN
    # fractional position (0 to 1)
    frac = deg_in_nak / NAK_SPAN

    # Project 360 degrees * frac from Lagna
    sl = (asc_lon + frac * 360) % 360
    return sl

def calculate_varnada_lagna(asc_rashi: int, hora_lagna_rashi: int) -> Dict[int, int]:
    """
    Varnada Lagna (V1-V12):
    Used for professional status and social standing.
    Standard Parashari rule involving Lagna and Hora Lagna.
    """
    results = {}
    # Rule for V1 (Lagna): If both are odd or both are even,
    # calculate distance directly. Else, subtract from 12.
    def get_v(r1, r2):
        if (r1 % 2 == 0) == (r2 % 2 == 0):
            return (r1 + r2) % 12
        else:
            return (r1 - r2 + 12) % 12

    v1 = get_v(asc_rashi, hora_lagna_rashi)
    results[1] = v1
    # Others follow in sequence
    for h in range(2, 13):
        results[h] = (v1 + h - 1) % 12

    return results
