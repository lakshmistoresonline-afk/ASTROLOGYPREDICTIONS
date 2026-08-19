from datetime import datetime, timedelta
from typing import List, Dict, Any

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
    """Generate the full list of Mahadashas with Antardashas and Pratyantardashas."""
    balance = calculate_dasha_balance(moon_longitude)
    start_lord_idx = balance["lord_idx"]

    mahadashas = []
    current_start = birth_dt

    for i in range(9):
        lord = DASHA_SEQUENCE[(start_lord_idx + i) % 9]
        years = balance["balance_years"] if i == 0 else DASHA_YEARS[lord]

        duration_days = years * DAYS_PER_YEAR
        current_end = current_start + timedelta(days=duration_days)

        # Calculate Antardashas
        antardashas = _get_antardashas(lord, current_start, years)

        mahadashas.append({
            "lord": lord,
            "start": current_start,
            "end": current_end,
            "years": years,
            "antardashas": antardashas
        })
        current_start = current_end

    return mahadashas

def _get_antardashas(maha_lord: str, maha_start: datetime, maha_years: float) -> List[Dict[str, Any]]:
    antars = []
    lord_idx = DASHA_SEQUENCE.index(maha_lord)
    current_start = maha_start

    for i in range(9):
        lord = DASHA_SEQUENCE[(lord_idx + i) % 9]
        # Duration is proportional: (Maha Years * Antar Years) / 120
        years = (maha_years * DASHA_YEARS[lord]) / TOTAL_YEARS
        duration_days = years * DAYS_PER_YEAR
        current_end = current_start + timedelta(days=duration_days)

        # Calculate Pratyantardashas
        pratyantars = _get_pratyantardashas(lord, current_start, years)

        antars.append({
            "lord": lord,
            "start": current_start,
            "end": current_end,
            "years": years,
            "months": years * 12,
            "pratyantardashas": pratyantars
        })
        current_start = current_end

    return antars

def _get_pratyantardashas(antar_lord: str, antar_start: datetime, antar_years: float) -> List[Dict[str, Any]]:
    pratys = []
    lord_idx = DASHA_SEQUENCE.index(antar_lord)
    current_start = antar_start

    for i in range(9):
        lord = DASHA_SEQUENCE[(lord_idx + i) % 9]
        years = (antar_years * DASHA_YEARS[lord]) / TOTAL_YEARS
        duration_days = years * DAYS_PER_YEAR
        current_end = current_start + timedelta(days=duration_days)

        pratys.append({
            "lord": lord,
            "start": current_start,
            "end": current_end,
            "years": years,
            "days": int(duration_days)
        })
        current_start = current_end

    return pratys
