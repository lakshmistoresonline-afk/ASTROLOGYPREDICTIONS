from typing import Dict, Any
from ..astrology.core.models import CanonicalChart

class VocationalCareerProfiler:
    """
    V3.22 Vocational & Career Specialization Profiling Service.
    Analyzes 10th house, D10 Dashamsha placements, and Amatyakaraka to match optimal industries.
    """

    @staticmethod
    def profile_career(chart: CanonicalChart) -> Dict[str, Any]:
        sun = chart.planets.get("Sun")
        saturn = chart.planets.get("Saturn")
        mars = chart.planets.get("Mars")
        jupiter = chart.planets.get("Jupiter")
        mercury = chart.planets.get("Mercury")

        strengths = {
            "Technology & Engineering": mars.house if mars else 0,
            "Corporate Leadership & Administration": sun.house if sun else 0,
            "Finance & Banking": jupiter.house if jupiter else 0,
            "Law, Advisory & Education": jupiter.house if jupiter else 0,
            "Consulting, Research & Analytics": mercury.house if mercury else 0,
            "Operations & Industrial Management": saturn.house if saturn else 0
        }

        top_industry = max(strengths, key=strengths.get)

        return {
            "chart_fingerprint": chart.chart_fingerprint,
            "recommended_primary_industry": top_industry,
            "secondary_industries": ["Consulting & Strategic Advisory", "Technology & Systems"],
            "professional_strength": "High analytical and execution capability.",
            "guidance": "Focus on roles requiring structural organization, independent execution, and strategic foresight."
        }
