from .planets import NAKSHATRA_LORDS, NAK_SPAN
from typing import Tuple, Dict

# Vimshottari years
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
    "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19,
    "Mercury": 17
}

LORDS_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

def get_kp_lords(longitude: float) -> Tuple[str, str]:
    """Calculate Star Lord and Sub-Lord for a given longitude."""
    # 1. Star Lord
    nak_idx = int(longitude / NAK_SPAN)
    star_lord = NAKSHATRA_LORDS[nak_idx]

    # 2. Sub-Lord
    # Degree within the nakshatra (0 to 13.333...)
    deg_in_nak = longitude % NAK_SPAN

    # Each nakshatra is divided into 9 parts proportional to dasha years
    # The order of sub-lords starts from the Star Lord itself
    start_lord_idx = LORDS_ORDER.index(star_lord)

    # One nakshatra (800') divided by 120 years = 6.666' per year
    minutes_per_year = 800.0 / 120.0

    current_minutes = deg_in_nak * 60.0
    accumulated = 0.0

    for i in range(9):
        lord = LORDS_ORDER[(start_lord_idx + i) % 9]
        span = DASHA_YEARS[lord] * minutes_per_year
        if accumulated <= current_minutes < (accumulated + span):
            return star_lord, lord
        accumulated += span

    return star_lord, LORDS_ORDER[start_lord_idx] # Fallback

def get_kp_sub_sub_lord(longitude: float) -> Tuple[str, str, str]:
    """Star, Sub, and Sub-Sub Lord."""
    # ... logic for SSL (division of Sub-Lord into 9 proportional parts)
    star, sub = get_kp_lords(longitude)

    # 3. Sub-Sub Lord
    deg_in_nak = longitude % NAK_SPAN
    minutes_per_year = 800.0 / 120.0

    start_lord_idx_star = LORDS_ORDER.index(star)
    accumulated_sub = 0.0
    sub_start_minutes = 0.0
    sub_span = 0.0

    for i in range(9):
        lord = LORDS_ORDER[(start_lord_idx_star + i) % 9]
        span = DASHA_YEARS[lord] * minutes_per_year
        if lord == sub:
            sub_start_minutes = accumulated_sub
            sub_span = span
            break
        accumulated_sub += span

    current_minutes = deg_in_nak * 60.0
    deg_in_sub_min = current_minutes - sub_start_minutes

    # Sub-lord (span) is divided into 9 SSL parts proportional to dasha years
    # 120 years = sub_span
    # 1 year = sub_span / 120
    ssl_min_per_year = sub_span / 120.0

    start_lord_idx_sub = LORDS_ORDER.index(sub)
    accumulated_ssl = 0.0
    for i in range(9):
        ssl_lord = LORDS_ORDER[(start_lord_idx_sub + i) % 9]
        span = DASHA_YEARS[ssl_lord] * ssl_min_per_year
        if accumulated_ssl <= deg_in_sub_min < (accumulated_ssl + span):
            return star, sub, ssl_lord
        accumulated_ssl += span

    return star, sub, sub # Fallback

def get_ruling_planets(jd_ut: float, lat: float, lon: float) -> Dict[str, str]:
    """RPs at the moment of calculation."""
    from .ephemeris import get_planet_position
    from .houses import get_houses
    from .swe_proxy import swe

    # 1. Moon Rashi and Star Lord
    moon_pos = get_planet_position(jd_ut, swe.MOON)
    m_star, m_sub = get_kp_lords(moon_pos["longitude"])
    from .houses import RASHI_LORDS
    m_rashi_lord = RASHI_LORDS[int(moon_pos["longitude"] // 30)]

    # 2. Lagna Rashi and Star Lord
    h_data = get_houses(jd_ut, lat, lon)
    asc_lon = h_data["ascendant"]
    l_star, l_sub = get_kp_lords(asc_lon)
    l_rashi_lord = RASHI_LORDS[int(asc_lon // 30)]

    # 3. Day Lord
    y, m, d, h = swe.revjul(jd_ut)
    from datetime import date
    wd = date(y, m, d).weekday() # 0=Mon, 6=Sun
    # Map to Lord
    DAY_LORDS = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
    day_lord = DAY_LORDS[wd]

    return {
        "Lagna Star Lord": l_star,
        "Lagna Rashi Lord": l_rashi_lord,
        "Moon Star Lord": m_star,
        "Moon Rashi Lord": m_rashi_lord,
        "Day Lord": day_lord
    }
