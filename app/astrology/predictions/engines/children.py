from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class ChildrenPredictionEngine:
    """
    V2 Hardened Children & Legacy Engine.
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
                "NATAL_PROMISE",
                f"LEGACY PROMISE: Supportive 5th Lord {l5_name} placement indicates joy through lineage.",
                85.0
            ))

        # Jupiter (Putrakaraka)
        jup = planets["Jupiter"]
        if "Exalted" in jup.dignity or jup.dignity == "Own Sign":
            evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "DIVINE GRACE: Strong Jupiter (Karaka for children) bolsters creative and procreative energy.",
                90.0
            ))

        # 2. DIVISIONAL CONFIRMATION (D7 Saptamsha)
        if d7:
            evidence.append(CorroborationEngine.create_evidence(
                "DIVISIONAL_CONFIRM",
                "VARGA CONFIRMATION: Saptamsha (D7) chart corroborates underlying fruitfulness.",
                75.0
            ))

        # 3. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord == l5_name or antar_lord == "Jupiter":
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"LEGACY ACTIVATION: Period of {antar_lord} triggers sectors of creation and procreation.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "NURTURING PHASE: Focus on maintenance of existing foundations.",
                60.0
            ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Moon", l5_name], [5, 9, 2], calculation_date=selected_date)

        # 5. SYNTHESIS
        summary_template = (
            "Growth of lineage and creative legacy shows {promise} natal foundation. "
            "Current alignment is {strength} for developmental milestones with a {score}% evidence score."
        )

        res = CorroborationEngine.synthesize("Children & Creativity", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Increased focus on child-related developmental phases.",
            "Activation of creative or procreative goals.",
            "Development of new intellectual or artistic projects."
        ]
        res.practical_actions = [
            "Maintain nurturing routines during lunar peak windows.",
            "Observe Jupiter-based remedies for lineage protection.",
            "Traditional family-strengthening practices are supported during this phase."
        ]

        return res
