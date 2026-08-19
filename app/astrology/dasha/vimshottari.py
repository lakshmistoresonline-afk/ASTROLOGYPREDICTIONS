from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

DASHA_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars",
    "Rahu", "Jupiter", "Saturn", "Mercury",
]

DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
    "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}

TOTAL_YEARS = 120
DAYS_PER_YEAR = 365.2425 # More precise Gregorian year

def calculate_dasha_balance(moon_longitude: float) -> Dict[str, Any]:
    """Calculate the starting dasha and balance years at birth."""
    nak_span = 360 / 27
    nak_idx = int(moon_longitude / nak_span)

    # Dasha sequence repeats every 9 nakshatras
    lord_idx = nak_idx % 9
    # The sequence starts from Ketu for Ashwini (idx 0)
    # Ashwini (0), Bharani (1), Krittika (2)...
    # Sequence: Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury
    # Matches NAKSHATRA_LORDS logic in legacy code

    lord = DASHA_SEQUENCE[lord_idx]

    nak_start = nak_idx * nak_span
    elapsed_in_nak = moon_longitude - nak_start
    fraction_remaining = 1 - (elapsed_in_nak / nak_span)

    balance_years = DASHA_YEARS[lord] * fraction_remaining

    return {
        "lord": lord,
        "balance_years": balance_years,
        "lord_idx": lord_idx
    }

def get_vimshottari_periods(moon_longitude: float, birth_dt: datetime) -> List[Dict[str, Any]]:
    """Generate the full list of Mahadashas."""
    balance = calculate_dasha_balance(moon_longitude)

    periods = []
    current_start = birth_dt

    start_lord_idx = balance["lord_idx"]

    for i in range(9):
        lord = DASHA_SEQUENCE[(start_lord_idx + i) % 9]
        years = balance["balance_years"] if i == 0 else DASHA_YEARS[lord]

        duration_days = years * DAYS_PER_YEAR
        current_end = current_start + timedelta(days=duration_days)

        periods.append({
            "lord": lord,
            "start": current_start,
            "end": current_end,
            "years": years
        })
        current_start = current_end

    return periods
