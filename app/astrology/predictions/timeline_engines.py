from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..core.models import CanonicalChart
from ..dasha import calculate_vimshottari

class TimelinePredictionEngine:
    """
    Deterministic Monthly and Yearly forecasting (Phase 36/37).
    """

    @staticmethod
    def get_monthly_summary(chart: CanonicalChart, target_month: int, target_year: int) -> Dict[str, Any]:
        """Synthesizes the most important themes for a given month."""
        # Focus on current Antardasha lord and major transits (Jupiter/Saturn)
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)

        antar = dasha.get("current_antar", {}).get("lord")

        return {
            "month": datetime(target_year, target_month, 1).strftime("%B %Y"),
            "best_period": "Middle of the month (Energetic peak)",
            "challenging_period": "End of the month (Transition phase)",
            "primary_focus": f"Themes related to {antar} activation.",
            "recommended_remedy": f"Strengthen {antar} through consistent practice."
        }

    @staticmethod
    def get_year_ahead(chart: CanonicalChart, start_year: int) -> List[Dict[str, Any]]:
        """Generates a 12-month timeline of opportunity and pressure windows."""
        timeline = []
        for i in range(1, 13):
            # Calculate for each month
            timeline.append(TimelinePredictionEngine.get_monthly_summary(chart, i, start_year))
        return timeline

timeline_predict_engine = TimelinePredictionEngine()
