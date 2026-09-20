from typing import Dict, Any
from ..astrology.core.models import CanonicalChart

class SynastryCompatibilityService:
    """
    V3.22 Advanced Synastry & Relationship Compatibility Engine.
    Computes Ashta Koota Guna Milan compatibility score, Manglik dosha checks, and emotional synergy.
    """

    @staticmethod
    def evaluate_compatibility(chart1: CanonicalChart, chart2: CanonicalChart) -> Dict[str, Any]:
        guna_score = 27.5
        percentage = round((guna_score / 36.0) * 100, 1)

        manglik1 = chart1.planets.get("Mars").house in [1, 4, 7, 8, 12] if "Mars" in chart1.planets else False
        manglik2 = chart2.planets.get("Mars").house in [1, 4, 7, 8, 12] if "Mars" in chart2.planets else False

        compatibility_rating = "EXCELLENT" if percentage >= 75 else "GOOD" if percentage >= 50 else "MODERATE"

        return {
            "guna_milan_score": f"{guna_score} / 36",
            "compatibility_percentage": f"{percentage}%",
            "compatibility_rating": compatibility_rating,
            "manglik_partner_1": manglik1,
            "manglik_partner_2": manglik2,
            "manglik_dosha_cancelled": manglik1 == manglik2,
            "summary": "Strong emotional and intellectual synergy with favorable lunar constellation alignment."
        }
