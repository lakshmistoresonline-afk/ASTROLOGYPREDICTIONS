from datetime import datetime, timedelta
from typing import List, Dict

YOGINIS = [
    ("Mangala", 1, "Moon"),
    ("Pingala", 2, "Sun"),
    ("Dhanya", 3, "Jupiter"),
    ("Bhramari", 4, "Mars"),
    ("Bhadrika", 5, "Mercury"),
    ("Ulka", 6, "Saturn"),
    ("Siddha", 7, "Venus"),
    ("Sankata", 8, "Rahu")
]

def calculate_yogini_dasha(moon_nak_idx: int, birth_dt: datetime) -> Dict:
    """
    Calculate Yogini Dasha (36-year cycle).
    moon_nak_idx: 0-26 (Ashwini=0)
    """
    # 1. Determine starting Yogini
    # Standard formula: (Nak + 3) % 8. Ashwini is 1 in traditional numbering.
    start_val = (moon_nak_idx + 1 + 3) % 8
    if start_val == 0: start_val = 8
    start_idx = start_val - 1 # 0-indexed for YOGINIS list

    # 2. Calculate balance at birth
    # Each Yogini period is 360 degrees / cycle years? No.
    # It's based on the portion of Nakshatra remaining.
    # This part is complex, often simplified as % of period elapsed.
    # For now, we'll implement the full 3 cycles (108 years).

    current_dt = birth_dt
    mahadashas = []

    # 3 cycles to cover ~108 years
    for cycle in range(3):
        for i in range(8):
            idx = (start_idx + i) % 8
            name, years, lord = YOGINIS[idx]

            # Simple implementation: doesn't account for partial balance at start yet
            # In a real system, the first period would be shortened.
            start_date = current_dt
            end_date = start_date + timedelta(days=years * 365.2425)

            mahadashas.append({
                "name": name,
                "years": years,
                "lord": lord,
                "start": start_date,
                "end": end_date,
                "is_current": start_date <= datetime.now() < end_date
            })
            current_dt = end_date

    return {
        "cycle_name": "Yogini (36 Years)",
        "mahadashas": mahadashas
    }
