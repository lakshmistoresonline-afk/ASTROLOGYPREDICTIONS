from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class LegalPredictionEngine:
    """
    V2 Hardened Legal & Conflict Engine.
    Evaluates 6th house (Enemies/Litigation) and Jupiter (Justice).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (6th House)
        l6_name = house_lords[6]

        promise_level = "MODERATE"
        # 6th lord in Upachaya (3, 6, 10, 11) is strong to defeat enemies
        if planets[l6_name].house in [3, 6, 10, 11]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                "CONFLICT RESOLUTION: Strong 6th Lord suggests victory over legal hurdles.",
                85.0
            ))

        # Jupiter (Significator of law and justice)
        jup = planets["Jupiter"]
        if jup.house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "JUSTICE MODIFIER: Well-placed Jupiter supports favorable legal outcomes.",
                80.0
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord == l6_name or antar_lord == "Jupiter":
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"ADMINISTRATIVE ACTIVATION: Period of {antar_lord} triggers resolution of disputes.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Focus on maintenance of existing formal commitments.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Saturn", l6_name], [6, 10, 1], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Legal matters and conflict resolution show {promise} natal strength. "
            "Current alignment is {strength} for success with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Legal & Disputes", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Resolution of pending disputes or administrative hurdles.",
            "Increased focus on formal documentation and compliance.",
            "Successful navigation of competitive or adversarial cycles."
        ]
        res.practical_actions = [
            "Verify documentation and evidence during lunar peak windows.",
            "Maintain transparency in all formal dealings.",
            "Traditional Jupiter-based justice rituals support truth."
        ]

        return res
