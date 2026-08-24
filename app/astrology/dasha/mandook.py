from typing import Dict, List, Any
from datetime import datetime
from ..core.houses import RASHI_NAMES

def calculate_mandook_dasha(asc_rashi: int, birth_dt: datetime) -> Dict[str, Any]:
    """
    Mandook (Frog) Dasha:
    Jump sequence: 1st, 3rd, 5th, 7th... (approx logic)
    Standard: Jumps of 3 signs.
    """
    # Jump sequence from Lagna
    sequence = []
    curr = asc_rashi
    for i in range(12):
        sequence.append(curr)
        curr = (curr + 3) % 12

    mahadashas = []
    current_start = birth_dt
    for r in sequence:
        # Standard duration: 9 years or similar based on specific variation
        dur = 7
        end = current_start.replace(year=current_start.year + dur)
        mahadashas.append({
            "rashi": RASHI_NAMES[r],
            "start": current_start,
            "end": end
        })
        current_start = end

    return {"mahadashas": mahadashas}
