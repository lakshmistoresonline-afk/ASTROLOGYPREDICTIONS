from .planets import NAKSHATRA_LORDS, NAK_SPAN
from typing import Tuple

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
