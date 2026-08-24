from typing import Dict, List, Any
from datetime import datetime, timedelta

# Dwishaptati Sama Dasha (72 Years)
# Sequence: Sun, Moon, Mars, Merc, Jup, Ven, Sat, Rahu (8 lords)
SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
YEARS = [9, 9, 9, 9, 9, 9, 9, 9] # Total 72

def calculate_dwishaptati_dasha(moon_nak_idx: int, birth_dt: datetime) -> Dict[str, Any]:
    """
    Calculate Dwishaptati Sama Dasha.
    Starting lord depends on birth Nakshatra.
    """
    # Moola (18) starts with Sun?
    # Formula: (Nak - 1) / 3?
    start_lord_idx = (moon_nak_idx // 4) % 8

    mahadashas = []
    current_start = birth_dt

    # 2 cycles to cover life
    for cycle in range(2):
        for i in range(8):
            idx = (start_lord_idx + i) % 8
            lord = SEQUENCE[idx]
            dur = YEARS[idx]

            end = current_start.replace(year=current_start.year + dur)
            mahadashas.append({
                "lord": lord,
                "start": current_start,
                "end": end,
                "cycle": cycle + 1
            })
            current_start = end

    return {"mahadashas": mahadashas}
