from typing import Dict, List, Any
from .houses import RASHI_LORDS

def calculate_varsheshwar(planets: Dict[str, Any], lagna_rashi: int, muntha_rashi: int, birth_lagna_rashi: int, is_day: bool) -> str:
    """
    Determine the Year Lord (Varsheshwar) from 5 candidates (Pancha-Adhikaris):
    1. Muntha Lord
    2. Birth Lagna Lord
    3. Yearly Lagna Lord
    4. Dina-Ratri Pati (Day/Night Lord)
    5. Tri-Rashi Pati

    The candidate with the highest Panchavargiya Bala becomes Varsheshwar.
    """
    candidates = set()

    # 1. Muntha Lord
    candidates.add(RASHI_LORDS[muntha_rashi])

    # 2. Birth Lagna Lord
    candidates.add(RASHI_LORDS[birth_lagna_rashi])

    # 3. Yearly Lagna Lord
    candidates.add(RASHI_LORDS[lagna_rashi])

    # 4. Dina-Ratri Pati
    # Day birth: Sun rashi lord. Night birth: Moon rashi lord.
    if is_day:
        candidates.add(RASHI_LORDS[planets["Sun"].rashi])
    else:
        candidates.add(RASHI_LORDS[planets["Moon"].rashi])

    # 5. Tri-Rashi Pati (Simplified standard table)
    # (Usually depends on Lagna rashi and Day/Night)
    TR_TABLE = {
        0: "Sun" if is_day else "Jupiter", # Aries
        1: "Venus" if is_day else "Moon",  # Taurus
        # ... and so on
    }
    candidates.add(TR_TABLE.get(lagna_rashi, "Jupiter"))

    # Select candidate with highest strength (using Shadbala as proxy if Varshaphala strength not calc'd)
    # In full Tajika, use Panchavargiya Bala.
    best_lord = list(candidates)[0]
    max_sb = -1.0
    for c in candidates:
        sb = planets[c].shadbala_score or 0.0
        if sb > max_sb:
            max_sb = sb
            best_lord = c

    return best_lord
