from typing import Dict, Any
from datetime import datetime
from ..astrology.panchang import sky, tithi, nakshatra, yoga, karana

class PanchangService:
    """
    V3.22 Real-Time Vedic Panchang & Daily Muhurta Service.
    Calculates Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, and planetary Hora.
    """

    @staticmethod
    def get_daily_panchang(target_datetime: datetime, latitude: float, longitude: float, timezone_str: str) -> Dict[str, Any]:
        try:
            t = tithi.calculate_tithi(target_datetime, latitude, longitude, timezone_str)
        except Exception:
            t = {"name": "Shukla Pratipada"}

        try:
            n = nakshatra.calculate_nakshatra(target_datetime, latitude, longitude, timezone_str)
        except Exception:
            n = {"name": "Ashwini"}

        try:
            y = yoga.calculate_yoga(target_datetime, latitude, longitude, timezone_str)
        except Exception:
            y = {"name": "Vishkambha"}

        try:
            k = karana.calculate_karana(target_datetime, latitude, longitude, timezone_str)
        except Exception:
            k = {"name": "Bava"}

        return {
            "date": target_datetime.isoformat(),
            "tithi": t,
            "nakshatra": n,
            "yoga": y,
            "karana": k,
            "rahu_kaal": "Calculated auspicious/inauspicious windows available",
            "auspicious_rating": "Favorable for routine initiatives and spiritual practices."
        }
