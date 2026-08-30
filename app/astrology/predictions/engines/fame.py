from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class FamePredictionEngine:
    """
    Hardened Fame & Reputation Engine.
    Evaluates 10th house (Karma), 1st (Identity), and 5th (Recognition).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (10th and 1st Houses)
        l10_name = house_lords[10]
        l1_name = house_lords[1]

        promise_level = "MODERATE"
        # Dig-Bala (Directional Strength) for Sun or Jupiter in 10th
        if planets["Sun"].house == 10 or planets["Jupiter"].house == 10:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "LEADERSHIP MODIFIER: Powerful directional strength in 10th house indicates public visibility.", 90.0
            ))

        if planets[l10_name].house in [1, 4, 7, 10, 5, 9]:
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"REPUTATION PROMISE: High status potential indicated by 10th Lord {l10_name} placement.", 85.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Life-period supports expansion of public identity and status.", 75.0
        ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Sun", "Jupiter", l10_name], [10, 1, 5])

        summary_template = (
            "The potential for public recognition and status shows {promise} underlying factors. "
            "Current alignment is {strength} for achievement with a {score}% hierarchical match."
        )

        res = CorroborationEngine.synthesize("Fame & Reputation", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Focus on integrity and public service during status peaks.",
            "Traditional Sun-related alignment practices support visibility.",
            "Maintain transparency in professional dealings during transition windows."
        ]
        return res
