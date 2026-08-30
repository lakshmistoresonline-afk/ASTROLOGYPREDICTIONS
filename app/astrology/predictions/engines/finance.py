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

        # 1. NATAL PROMISE (2nd and 11th Houses)
        l2_name = house_lords[2]
        l11_name = house_lords[11]
        l2 = planets[l2_name]
        l11 = planets[l11_name]

        promise_level = "MODERATE"
        if l2.house in [1, 4, 7, 10, 2, 11, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"WEALTH PROMISE: Inherent capacity for accumulation supported by 2nd Lord {l2_name}.", 85.0
            ))

        if l11.house in [1, 4, 7, 10, 2, 11, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"GAINS PROMISE: High revenue potential indicated by 11th Lord {l11_name} placement.", 80.0
            ))

        # 2. ACTIVATION (Dasha)
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord in [l2_name, l11_name, "Jupiter", "Venus"]:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION", f"FINANCIAL ACTIVATION: Period of {antar_lord} triggers wealth generation cycles.", 90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION", "CURRENT ACTIVATION: Resource focus is secondary in the current life-period.", 60.0
            ))

        # 3. YOGAS (Dhana Yogas)
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
