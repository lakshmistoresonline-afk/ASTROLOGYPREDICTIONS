from typing import Dict, Any, List
from ..astrology.core.models import CanonicalChart

class DrishtiAspectService:
    """
    V3.22 Interactive Drishti (Aspect) Ray Calculation Service.
    Computes classical Vedic aspects between planets (e.g., Saturn's 3rd, 7th, 10th; Mars' 4th, 7th, 8th; Jupiter's 5th, 7th, 9th).
    """

    @staticmethod
    def calculate_aspects(chart: CanonicalChart) -> List[Dict[str, Any]]:
        planets = chart.planets
        aspects = []

        for p_name, p in planets.items():
            p_house = p.house
            seventh_house = ((p_house + 5) % 12) + 1
            aspects.append({
                "source_planet": p_name,
                "source_house": p_house,
                "aspect_type": "7th House (Full Opposition)",
                "target_house": seventh_house
            })

            if p_name == "Mars":
                for h_offset in [3, 7]:
                    target = ((p_house + h_offset) % 12) + 1
                    aspects.append({
                        "source_planet": "Mars",
                        "source_house": p_house,
                        "aspect_type": f"{h_offset+1}th House Special Aspect",
                        "target_house": target
                    })
            elif p_name == "Jupiter":
                for h_offset in [4, 8]:
                    target = ((p_house + h_offset) % 12) + 1
                    aspects.append({
                        "source_planet": "Jupiter",
                        "source_house": p_house,
                        "aspect_type": f"{h_offset+1}th House Special Aspect",
                        "target_house": target
                    })
            elif p_name == "Saturn":
                for h_offset in [2, 9]:
                    target = ((p_house + h_offset) % 12) + 1
                    aspects.append({
                        "source_planet": "Saturn",
                        "source_house": p_house,
                        "aspect_type": f"{h_offset+1}th House Special Aspect",
                        "target_house": target
                    })

        return aspects
