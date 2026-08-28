from typing import Dict, List, Any
from datetime import datetime, timedelta

# Shat-trimsha Sama Dasha (36 Years)
SEQUENCE = ["Moon", "Sun", "Jupiter", "Rahu", "Mercury", "Saturn", "Mars", "Venus"]
YEARS = [1, 2, 3, 4, 5, 6, 7, 8]

def calculate_shattrimsha_dasha(moon_nak_idx: int, birth_dt: datetime) -> Dict[str, Any]:
    """
    Calculate Shat-trimsha Sama Dasha.
    """
    if moon_nak_idx is None:
        raise ValueError("Moon Nakshatra index required for Shattrimsha calculation.")

    start_lord_idx = (moon_nak_idx // 3) % 8
    mahadashas = []
    current_start = birth_dt

    for cycle in range(3):
        for i in range(8):
            idx = (start_lord_idx + i) % 8
            lord = SEQUENCE[idx]
            dur = YEARS[idx]
            end = current_start.replace(year=current_start.year + dur)
            mahadashas.append({"lord": lord, "start": current_start, "end": end, "cycle": cycle + 1})
            current_start = end

    return {"mahadashas": mahadashas}
