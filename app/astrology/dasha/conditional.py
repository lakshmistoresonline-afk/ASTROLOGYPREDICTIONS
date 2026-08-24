from typing import Dict, List, Any
from datetime import datetime, timedelta

def calculate_ashtottari_dasha(moon_nak_idx: int, birth_dt: datetime) -> Dict[str, Any]:
    """
    Ashtottari Dasha (108 years):
    Used if Rahu is in Kendra/Trikona from Lagna Lord (or other specific conditions).
    Sequence: Sun(6), Moon(15), Mars(8), Merc(17), Sat(10), Jup(19), Rahu(12), Ven(21).
    """
    # Sequence depends on Nakshatra at birth
    # Starting nak: Ardra (5)
    # (Simplified sequence mapping)
    SEQUENCE = ["Sun", "Moon", "Mars", "Mercury", "Saturn", "Jupiter", "Rahu", "Venus"]
    YEARS = [6, 15, 8, 17, 10, 19, 12, 21]

    # Starting lord based on birth Nakshatra (Simplified)
    # Actually follows a specific Nakshatra-to-Lord mapping
    mapping = {
        0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2,
        # ... mapped across 27 nakshatras in groups
    }
    start_lord_idx = (moon_nak_idx // 3) % 8

    mahadashas = []
    current_start = birth_dt
    for i in range(8):
        idx = (start_lord_idx + i) % 8
        lord = SEQUENCE[idx]
        dur = YEARS[idx]

        end = current_start.replace(year=current_start.year + dur)
        mahadashas.append({"lord": lord, "start": current_start, "end": end})
        current_start = end

    return {"mahadashas": mahadashas}

def check_dasha_suitability(chart: Any) -> List[str]:
    """Identify which conditional dashas should be prioritized."""
    suits = ["Vimshottari (Universal)"]

    planets = chart.planets
    ll_name = chart.house_lords[1]
    rahu = planets["Rahu"]

    # Ashtottari Condition: Rahu in Kendra/Trikona from Lagna Lord
    ll_house = planets[ll_name].house
    rel_house = (rahu.house - ll_house + 12) % 12 + 1
    if rel_house in [1, 4, 7, 10, 5, 9]:
        suits.append("Ashtottari (Applicable)")

    # Dwishaptati Sama: Lagna Lord in 7th or 7th Lord in Lagna
    l7_name = chart.house_lords[7]
    if planets[ll_name].house == 7 or planets[l7_name].house == 1:
        suits.append("Dwishaptati Sama (High Accuracy)")

    return suits
