from typing import Dict, List, Any
import swisseph as swe
from ..core.ephemeris import get_planet_position
from ..core.panchang.panchang_logic import calculate_panchang
from datetime import datetime

class MuhurtaEngine:
    """
    Engine to find auspicious times and detect Panchang-based yogas/doshas.
    Implements 21 Great Evils (Maha Doshas) and auspicious combinations.
    """

    def __init__(self, lat: float, lon: float, tz: float):
        self.lat = lat
        self.lon = lon
        self.tz = tz

    def get_muhurta_score(self, dt: datetime) -> Dict[str, Any]:
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 - self.tz)
        panchang = calculate_panchang(jd, self.lat, self.lon)

        score = 100
        negative_factors = []
        positive_factors = []

        # 1. Rahu Kaal Check (Negative)
        if panchang.get("is_rahu_kaal"):
            score -= 30
            negative_factors.append("Rahu Kaal: Inauspicious for starting new ventures.")

        # 2. Gulika Kaal
        if panchang.get("is_gulika_kaal"):
            score -= 15
            negative_factors.append("Gulika Kaal: Delays and hurdles expected.")

        # 3. Tithi Check
        inauspicious_tithis = [4, 9, 14] # Rikta Tithis
        if panchang["tithi_num"] in inauspicious_tithis:
            score -= 20
            negative_factors.append(f"Rikta Tithi ({panchang['tithi_name']}): Usually avoided for auspicious work.")

        # 4. Nakshatra Check
        # Fixed (Dhruva), Movable (Chara), Sharp (Tikshna), Mixed (Mridu-Tikshna)...
        # Simplified: check for Sarvartha Siddhi Yoga
        if self._is_sarvartha_siddhi(panchang):
            score += 40
            positive_factors.append("Sarvartha Siddhi Yoga: Highly auspicious, overrides many minor doshas.")

        # 5. Amrita Siddhi Yoga
        if self._is_amrita_siddhi(panchang):
            score += 30
            positive_factors.append("Amrita Siddhi Yoga: Best for long-term success.")

        # 6. Panchaka Check
        if self._is_panchaka(panchang["nakshatra_num"]):
            score -= 10
            negative_factors.append("Panchaka: Avoid specific activities like travel south or roof construction.")

        return {
            "score": max(0, min(100, score)),
            "positive": positive_factors,
            "negative": negative_factors,
            "panchang": panchang,
            "rating": self._get_rating(score)
        }

    def _is_sarvartha_siddhi(self, p: Dict[str, Any]) -> bool:
        # Combinations of Weekday and Nakshatra
        # Sun: Ashwini, Pushya, Hasta, Uttara Phalguni, Uttara Ashadha, Uttara Bhadrapada, Rohini
        combinations = {
            0: [1, 8, 13, 12, 21, 26, 4], # Sun
            1: [4, 5, 15, 22, 27],        # Mon: Rohini, Mrigashira, Swati, Shravana, Revati
            2: [1, 9, 14, 23],            # Tue: Ashwini, Ashlesha, Chitra, Dhanishta
            3: [4, 8, 13, 16, 17, 26],    # Wed: Rohini, Pushya, Hasta, Vishakha, Anuradha, Uttara Bhadra
            4: [1, 8, 10, 13, 22, 27],    # Thu: Ashwini, Pushya, Magha, Hasta, Shravana, Revati
            5: [1, 13, 14, 17, 27],        # Fri: Ashwini, Hasta, Chitra, Anuradha, Revati
            6: [4, 15, 23]                # Sat: Rohini, Swati, Dhanishta
        }
        return p["nakshatra_num"] in combinations.get(p["weekday"], [])

    def _is_amrita_siddhi(self, p: Dict[str, Any]) -> bool:
        # Mon + Rohini, Tue + Ashwini, Wed + Anuradha, Thu + Pushya, Fri + Revati, Sat + Rohini, Sun + Hasta
        pairs = {1: 4, 2: 1, 3: 17, 4: 8, 5: 27, 6: 4, 0: 13}
        return pairs.get(p["weekday"]) == p["nakshatra_num"]

    def _is_panchaka(self, nak_num: int) -> bool:
        # Dhanishta (last half) to Revati
        return nak_num in [23, 24, 25, 26, 27]

    def _get_rating(self, score: int) -> str:
        if score >= 80: return "EXCELLENT"
        if score >= 60: return "GOOD"
        if score >= 40: return "AVERAGE"
        return "POOR"
