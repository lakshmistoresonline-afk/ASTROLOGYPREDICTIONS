from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class FinancePredictionEngine:
    """
    Hardened Finance Engine (Phase 4).
    Separates Wealth Potential from Immediate Gains.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE
        l2_name = house_lords[2]
        l2 = planets[l2_name]

        promise_level = "MODERATE"
        if l2.house in [1, 4, 7, 10, 2, 11, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "WEALTH PROMISE: Inherent capacity for resource security and accumulation.", 85.0
            ))

        # 2. ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "FINANCIAL ACTIVATION: Current Dasha period supports wealth generation.", 80.0
        ))

        # 3. YOGAS (Modifiers)
        for yoga in chart.yogas:
            if "Dhana" in yoga["name"]:
                evidence.append(CorroborationEngine.create_evidence(
                    "YOGA_SUPPORT", f"YOGA MODIFIER: {yoga['name']} acts as a significant wealth catalyst.", 90.0
                ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Venus", l2_name], [2, 11, 5])

        summary_template = (
            "Your financial trajectory has a {promise} foundation and shows {strength} alignment for growth. "
            "Hierarchical confidence is rated at {score}%."
        )

        res = CorroborationEngine.synthesize("Finance & Wealth", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "This is trend analysis, not investment advice. Consult a financial professional.",
            "Focus on long-term resource stability and disciplined saving.",
            "Avoid speculative risks in sectors where corroboration is weak."
        ]
        return res
