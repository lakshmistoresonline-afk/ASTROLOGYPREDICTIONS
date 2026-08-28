from typing import List, Dict, Any, Optional
from ..core.models import CanonicalChart

class RemedyDecisionEngine:
    """
    Multidimensional Contextual Remedy Engine (Phase 4).
    Evaluates functional lordship, house, dignity, and activation.
    """

    @staticmethod
    def get_contextual_remedy(chart: CanonicalChart, planet_name: str, problem: str) -> Dict[str, Any]:
        info = chart.planets.get(planet_name)
        if not info: return {}

        status = info.functional_status
        dignity = info.dignity
        house = info.house
        is_retro = info.is_retrograde

        # Decision logic (Phase 11/12)
        approach = "Balance"
        rationale = ""

        if status == "Yogakaraka" or "Benefic" in status:
            if "Debilitated" in dignity or info.is_combust:
                approach = "Strengthen (Mantra/Worship)"
                rationale = "The planet has a high-quality promise but lacks the strength to manifest it."
            else:
                approach = "Balance (Meditation)"
                rationale = "Enhance the already positive vibration of this indicator."
        elif "Malefic" in status:
            approach = "Pacify (Charity/Seva)"
            rationale = "The planet represents structural friction; pacifying it reduces the karmic impact."
            if is_retro:
                approach = "Discipline (Service/Vows)"
                rationale = "Karmic review required: focus on self-discipline in this house's themes."

        return {
            "planet": planet_name,
            "problem": problem,
            "approach": approach,
            "priority": "HIGH PRIORITY" if approach == "Pacify (Charity/Seva)" else "MEDIUM PRIORITY",
            "why": rationale,
            "how": f"Observe traditional {approach} practices related to {planet_name}.",
            "traditional_purpose": f"Traditionally used to {approach.lower()} planetary expression.",
            "safety": "Observe standard ritual hygiene; do not replace medical advice."
        }

def get_personalized_remedies(chart: CanonicalChart) -> List[Dict[str, Any]]:
    remedies = []
    # Identify Top 3 Problems
    candidates = []
    for name, info in chart.planets.items():
        if "Debilitated" in info.dignity: candidates.append((name, "Dignity Pressure"))
        if info.house in [6, 8, 12]: candidates.append((name, "Location Stress"))

    for name, problem in candidates[:3]:
        remedy = RemedyDecisionEngine.get_contextual_remedy(chart, name, problem)
        if remedy: remedies.append(remedy)

    return remedies
