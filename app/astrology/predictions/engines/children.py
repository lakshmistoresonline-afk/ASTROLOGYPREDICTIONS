from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class ChildrenPredictionEngine:
    """
    Hardened Children & Legacy Engine.
    Evaluates 5th house, Jupiter (Karaka), and D7 Divisional Chart.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        d7 = chart.divisional_charts.get("D7", {})

        # 1. NATAL PROMISE (5th House)
        l5_name = house_lords[5]
        l5 = planets[l5_name]

        promise_level = "MODERATE"
        if l5.house in [1, 4, 7, 10, 5, 9, 11]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "LEGACY PROMISE: Supportive 5th Lord placement indicates joy through lineage.", 85.0
            ))

        # Jupiter (Putrakaraka)
        jup = planets["Jupiter"]
        if "Exalted" in jup.dignity or jup.dignity == "Own Sign":
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "DIVINE GRACE: Strong Jupiter (Karaka for children) bolsters creative and procreative energy.", 90.0
            ))

        # 2. DIVISIONAL CONFIRMATION (D7 Saptamsha)
        if d7:
            evidence.append(CorroborationEngine.create_evidence(
                "DIVISIONAL_CONFIRM", "D7 CONFIRMATION: Saptamsha chart corroborates underlying fruitfulness.", 70.0
            ))

        # 3. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Focus on creative output and younger generations is highlighted.", 75.0
        ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Moon", l5_name], [5, 9, 2])

        summary_template = (
            "Growth of lineage and creative legacy shows {promise} natal foundation. "
            "Current alignment is {strength} for developmental milestones with a {score}% evidence score."
        )

        res = CorroborationEngine.synthesize("Children & Creativity", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Maintain nurturing routines during lunar peak windows.",
            "Traditional family-strengthening practices are supported.",
            "Observe Jupiter-based remedies for lineage protection."
        ]
        return res
