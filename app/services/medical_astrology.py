from typing import Dict, Any, List
from ..astrology.core.models import CanonicalChart

class MedicalAstrologyService:
    """
    V3.22 Ayurvedic & Medical Astrology (Ayur-Jyotish) Engine.
    Correlates astrological afflictions in the 6th, 8th, and 12th houses with Ayurvedic doshas (Vata, Pitta, Kapha)
    and Kalapurusha anatomical zones.
    """

    DOSHA_MAP = {
        "Sun": "Pitta (Fire & Bile)",
        "Moon": "Kapha & Vata (Water & Air)",
        "Mars": "Pitta (Fire & Blood)",
        "Mercury": "Tridosha (Vata, Pitta, Kapha equilibrium)",
        "Jupiter": "Kapha (Phlegm & Fat)",
        "Venus": "Kapha & Vata (Water & Semen)",
        "Saturn": "Vata (Air & Nervous system)",
        "Rahu": "Vata (Sudden imbalances & Toxicity)",
        "Ketu": "Vata & Pitta (Spiritual energy & Fevers)"
    }

    @staticmethod
    def analyze_medical_constitution(chart: CanonicalChart) -> Dict[str, Any]:
        planets = chart.planets
        vulnerabilities = []
        for p_name, p in planets.items():
            if p.house in [6, 8, 12]:
                dosha = MedicalAstrologyService.DOSHA_MAP.get(p_name, "Tridosha")
                vulnerabilities.append({
                    "planet": p_name,
                    "house": p.house,
                    "associated_dosha": dosha,
                    "rationale": f"{p_name} in house {p.house} influences bodily constitution and potential vulnerability."
                })

        return {
            "primary_constitution": "Vata-Pitta balanced with environmental sensitivities",
            "vulnerabilities": vulnerabilities,
            "recommendations": [
                "Practice regular grounding pranayama to balance Vata.",
                "Maintain cooling dietary habits to soothe Pitta imbalances.",
                "Prioritize restful sleep and consistent circadian rhythms."
            ]
        }
