from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class TravelPredictionEngine:
    """
    Hardened Travel Engine (Phase 4).
    Evaluates 3rd, 9th, and 12th houses for short and long-distance travel.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (9th & 12th Houses)
        l9_name = house_lords[9]
        l12_name = house_lords[12]

        promise_level = "MODERATE"
        l9_house = planets[l9_name].house
        if l9_house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High travel potential indicated by Kendra/Trikona placement of 9th Lord {l9_name}.",
                90.0, rationale=f"{l9_name} is in house {l9_house}"
            ))
        elif l9_house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 9th Lord {l9_name} provides stable travel foundation.",
                60.0, rationale=f"{l9_name} is in house {l9_house}"
            ))
        l12_house = planets[l12_name].house
        if l12_house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"HORIZON PROMISE: High migration potential indicated by Kendra/Trikona placement of 12th Lord {l12_name}.",
                90.0, rationale=f"{l12_name} is in house {l12_house}"
            ))
        elif l12_house in [2, 11]:
             evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 12th Lord {l12_name} provides stable transition potential.",
                60.0, rationale=f"{l12_name} is in house {l12_house}"
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Movement and expansion sectors are currently triggered.", 80.0
        ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, [l9_name, l12_name, "Moon"], [9, 12, 3], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Opportunities for travel and expansion show {promise} natal potential. "
            "Timing alignment is {strength} with a {score}% hierarchical match."
        )

        res = CorroborationEngine.synthesize("Travel & Horizons", promise_level, evidence, summary_template, timing_window=window)
        res.practical_actions = [
            "Verify travel documents and insurance before departure.",
            "Traditional journey-blessing practices are recommended.",
            "Maintain flexibility during planetary transition periods."
        ]
        return res
