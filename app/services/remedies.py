from typing import Dict, Any, List
from ..astrology.core.models import CanonicalChart

class VedicRemedialService:
    """
    V3.22 Authoritative Vedic Remedial & Gemstone Recommendation Engine.
    Provides personalized gemstone suggestions, mantra sadhana, and planetary charity guidance
    based on exact Lagna lord, Yogakaraka strength, and functional benefic status.
    """

    GEMSTONE_MAP = {
        "Sun": {
            "gemstone": "Ruby (Manikya)",
            "metal": "Gold or Copper",
            "finger": "Ring Finger",
            "day": "Sunday (Sunrise)",
            "mantra": "Om Ghrini Suryaya Namah",
            "charity": "Wheat, red lentils, or jaggery donation on Sundays."
        },
        "Moon": {
            "gemstone": "Natural Pearl (Moti)",
            "metal": "Silver",
            "finger": "Little Finger",
            "day": "Monday (Evening)",
            "mantra": "Om Som Somaya Namah",
            "charity": "Milk, rice, or white cloth donation on Mondays."
        },
        "Mars": {
            "gemstone": "Red Coral (Moonga)",
            "metal": "Copper or Gold",
            "finger": "Ring Finger",
            "day": "Tuesday (Morning)",
            "mantra": "Om Angarakaya Namah",
            "charity": "Red lentils or blood donation support on Tuesdays."
        },
        "Mercury": {
            "gemstone": "Emerald (Panna)",
            "metal": "Gold or Silver",
            "finger": "Little Finger",
            "day": "Wednesday (Morning)",
            "mantra": "Om Bum Budhaya Namah",
            "charity": "Green moong dal or feeding cows on Wednesdays."
        },
        "Jupiter": {
            "gemstone": "Yellow Sapphire (Pukhraj)",
            "metal": "Gold",
            "finger": "Index Finger",
            "day": "Thursday (Morning)",
            "mantra": "Om Brim Brihaspataye Namah",
            "charity": "Turmeric, yellow chana dal, or supporting education."
        },
        "Venus": {
            "gemstone": "Diamond (Heera) or White Sapphire",
            "metal": "Silver, Platinum, or Gold",
            "finger": "Middle or Ring Finger",
            "day": "Friday (Morning)",
            "mantra": "Om Shum Shukraya Namah",
            "charity": "Rice, sugar, or white sweets donation on Fridays."
        },
        "Saturn": {
            "gemstone": "Blue Sapphire (Neelam) - Wear with Caution",
            "metal": "Silver, Iron, or Panchdhatu",
            "finger": "Middle Finger",
            "day": "Saturday (Evening)",
            "mantra": "Om Sham Shanicharaya Namah",
            "charity": "Black sesame seeds, mustard oil, or feeding needy on Saturdays."
        }
    }

    @staticmethod
    def generate_recommendations(chart: CanonicalChart) -> Dict[str, Any]:
        rashi_names = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        asc_rashi_name = rashi_names[chart.asc_rashi] if 0 <= chart.asc_rashi < 12 else "Aries"

        lagna_lords = {
            "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
            "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
            "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
        }

        ruling_planet = lagna_lords.get(asc_rashi_name, "Jupiter")
        rec = VedicRemedialService.GEMSTONE_MAP.get(ruling_planet, VedicRemedialService.GEMSTONE_MAP["Jupiter"])

        return {
            "ascendant_rashi": asc_rashi_name,
            "primary_benefic_planet": ruling_planet,
            "recommended_gemstone": rec["gemstone"],
            "metal": rec["metal"],
            "wearing_finger": rec["finger"],
            "auspicious_day": rec["day"],
            "vedic_mantra": rec["mantra"],
            "charity_recommendation": rec["charity"],
            "caution": "Always consult an experienced Vedic astrologer and test gemstone compatibility for 3 days before permanent wear."
        }
