from typing import Dict, Any, List
from datetime import datetime
from ..astrology.core.chart import calculate_chart_data
from ..astrology.core.models import CanonicalChart

class TransitAlertService:
    """
    V3.22 Real-Time Transit Notification & Astrological Weather Service.
    Monitors planetary transits against natal chart placements (e.g., Sade Sati, Jupiter transits)
    and generates personalized astrological weather forecasts.
    """

    @staticmethod
    def generate_weather_forecast(chart: CanonicalChart, current_datetime: datetime = None) -> Dict[str, Any]:
        if current_datetime is None:
            current_datetime = datetime.utcnow()

        transit_chart = calculate_chart_data(current_datetime, chart.latitude, chart.longitude, chart.timezone)

        alerts = []
        moon_rashi = chart.planets["Moon"].rashi
        saturn_transit = transit_chart.planets.get("Saturn")

        if saturn_transit:
            diff = (saturn_transit.rashi - moon_rashi) % 12
            if diff in [11, 0, 1]:
                alerts.append({
                    "alert_type": "SADE_SATI_ACTIVE",
                    "severity": "HIGH",
                    "message": "Saturn is transiting through the 12th, 1st, or 2nd house from your natal Moon (Sade Sati phase). Focus on patience, discipline, and structural resilience."
                })

        jupiter_transit = transit_chart.planets.get("Jupiter")
        if jupiter_transit:
            diff_j = (jupiter_transit.rashi - moon_rashi) % 12
            if diff_j in [0, 4, 8, 10]:
                alerts.append({
                    "alert_type": "JUPITER_BENEFIC_TRANSIT",
                    "severity": "POSITIVE",
                    "message": "Jupiter is aspecting or transiting in a supportive trine/kendra from your Moon, bringing expansion, wisdom, and favorable opportunities."
                })

        return {
            "forecast_date": current_datetime.isoformat(),
            "overall_weather": "Favorable planetary currents supporting structured growth." if not any(a["severity"] == "HIGH" for a in alerts) else "Transformational transit phase requiring mindful navigation.",
            "active_alerts": alerts
        }
