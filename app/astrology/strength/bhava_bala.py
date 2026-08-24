from typing import Dict, List, Any
from ..core.houses import RASHI_LORDS

def calculate_bhava_bala(chart_data: Dict[str, Any]) -> Dict[int, float]:
    """
    Simplified Bhava Bala (House Strength).
    Factors:
    1. Lord Strength (Shadbala) - 50%
    2. Benefic/Malefic occupants - 30%
    3. Aspects on house - 20%
    """
    planets = chart_data["planets"]
    house_occupants = chart_data["house_occupants"]
    house_lords = chart_data["house_lords"]

    bhava_scores = {}

    for h_num in range(1, 13):
        score = 0.0

        # 1. Lord Strength
        lord_name = house_lords[h_num]
        lord_p = planets.get(lord_name)
        if lord_p:
            # Lord Shadbala (normalized to 100 max for this component)
            # Standard Shadbala is usually 300-600 Virupas.
            # We take 400 as "Good" (100% component score)
            sb = lord_p.shadbala_score or 400
            score += min(50.0, (sb / 400.0) * 50.0)

        # 2. Occupants
        occupants = house_occupants.get(h_num, [])
        for p in occupants:
            p_data = planets.get(p)
            if not p_data: continue
            if p_data.functional_status == "Functional Benefic": score += 10
            elif p_data.functional_status == "Functional Malefic": score -= 5

        # 3. Aspects (Simplified)
        # Check aspect array if available, or just use +5 for Jupiter aspect etc.
        # For now, let's keep it simple.

        bhava_scores[h_num] = max(0.0, round(score, 2))

    return bhava_scores
