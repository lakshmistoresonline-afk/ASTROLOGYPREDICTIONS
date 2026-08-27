from typing import Dict, List, Any
from datetime import datetime, timedelta

# Mudda Dasha (1 Year cycle)
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
# Proportional days in a 365.25 day year
# Ketu: (7/120)*365.25 = 21.3 days
# Venus: (20/120)*365.25 = 60.8 days...

def calculate_mudda_dasha(moon_lon: float, sr_dt: datetime) -> Dict[str, Any]:
    """Calculate Mudda Dasha for the Varshaphala year."""
    from .vimshottari import calculate_dasha_balance
    balance = calculate_dasha_balance(moon_lon)
    start_lord_idx = balance["lord_idx"]

    mahadashas = []
    current_start = sr_dt

    # Scale 120 years to 1 year (365.2425 days)
    SCALE = 365.2425 / 120.0

    from .vimshottari import DASHA_YEARS

    for i in range(9):
        lord = DASHA_SEQUENCE[(start_lord_idx + i) % 9]
        years = balance["balance_years"] if i == 0 else DASHA_YEARS[lord]

        duration_days = years * SCALE * 120 / 120 # simplified: years * (365.25/120)
        duration_days = years * 3.0437 # approx days per dasha-year

        current_end = current_start + timedelta(days=duration_days)
        mahadashas.append({
            "lord": lord,
            "start": current_start,
            "end": current_end,
            "days": round(duration_days, 1)
        })
        current_start = current_end

    return {"mahadashas": mahadashas}
