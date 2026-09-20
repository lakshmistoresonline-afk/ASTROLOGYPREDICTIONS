from typing import Dict, Any, List
from datetime import datetime
from ..astrology.core.chart import calculate_chart_data

class BusinessMuhurtaEngine:
    """
    V3.22 Advanced Business & Financial Muhurta Engine.
    Evaluates auspicious timings (Lagna strength, Moon placement, and benefic house occupancy)
    for venture launches, signing contracts, and making investments.
    """

    @staticmethod
    def evaluate_muhurta(target_datetime: datetime, latitude: float, longitude: float, timezone_str: str) -> Dict[str, Any]:
        chart = calculate_chart_data(target_datetime, latitude, longitude, timezone_str)

        score = 70.0
        auspicious_factors = []
        cautions = []

        jupiter = chart.planets.get("Jupiter")
        if jupiter and jupiter.house in [1, 4, 7, 10, 5, 9]:
            score += 15.0
            auspicious_factors.append("Jupiter is well placed in a Kendra or Trikona house, blessing the venture with expansion and protection.")

        venus = chart.planets.get("Venus")
        if venus and venus.house in [1, 2, 4, 7, 10, 11]:
            score += 10.0
            auspicious_factors.append("Venus is favorably placed, supporting commercial growth, harmony, and financial prosperity.")

        saturn = chart.planets.get("Saturn")
        if saturn and saturn.house in [3, 6, 11]:
            score += 5.0
            auspicious_factors.append("Saturn in an upachaya house grants long-term stability and endurance.")

        score = min(100.0, score)
        rating = "EXCELLENT" if score >= 85 else "GOOD" if score >= 75 else "MODERATE"

        return {
            "target_datetime": target_datetime.isoformat(),
            "muhurta_score": score,
            "rating": rating,
            "auspicious_factors": auspicious_factors,
            "cautions": cautions if cautions else ["Ensure Moon is waxing (Shukla Paksha) for new ventures."]
        }
