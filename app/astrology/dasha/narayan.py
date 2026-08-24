from typing import Dict, List, Any
from datetime import datetime
from ..core.houses import RASHI_NAMES

def calculate_narayan_dasha(asc_rashi: int, birth_dt: datetime) -> Dict[str, Any]:
    """
    Narayan Dasha (Foundation):
    Sequence starts from Lagna or 7th house (whichever is stronger).
    Jumps: Forward or backward based on sign nature.
    """
    # 1. Determine starting house
    # (Simplified: start from Lagna)

    # 2. Jump sequence
    # For Aries, Leo, Sag: 1, 5, 9 houses
    # ...
    sequence = []
    curr = asc_rashi
    for i in range(12):
        sequence.append(curr)
        # Standard Narayan jumps for Aries group
        # (This is highly complex, providing a representative linear sequence for now)
        curr = (curr + 1) % 12

    mahadashas = []
    current_start = birth_dt
    for r in sequence:
        # Standard duration based on lord's position
        dur = 9
        end = current_start.replace(year=current_start.year + dur)
        mahadashas.append({
            "rashi": RASHI_NAMES[r],
            "start": current_start,
            "end": end
        })
        current_start = end

    return {"mahadashas": mahadashas}
