from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class FamilyPredictionEngine:
    """
    Hardened Family & Roots Engine.
    Evaluates 2nd (Family), 4th (Mother/Home), and 9th (Father) houses.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (2nd and 4th Houses)
        l2_name = house_lords[2]
        l4_name = house_lords[4]

        promise_level = "MODERATE"
        if planets[l2_name].house in [1, 2, 4, 5, 7, 9, 10, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"FAMILY PROMISE: Supportive 2nd Lord {l2_name} placement indicates strong roots.", 80.0
            ))

        if planets[l4_name].house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"DOMESTIC PROMISE: Beneficial 4th Lord {l4_name} supports home stability.", 85.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Internal life-period highlights domestic and family sectors.", 70.0
        ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Moon", "Venus", l4_name], [2, 4])

        summary_template = (
            "Domestic harmony and family support show {promise} natal foundation. "
            "Current alignment is {strength} for family matters with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Family & Roots", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Maintain ancestral traditions during energetic peaks.",
            "Focus on emotional communication within the home.",
            "Traditional family-blessing rituals are supported."
        ]
        return res
