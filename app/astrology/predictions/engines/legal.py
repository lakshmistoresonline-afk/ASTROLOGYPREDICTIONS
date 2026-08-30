from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class LegalPredictionEngine:
    """
    Hardened Legal & Conflict Engine.
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
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "CONFICT RESOLUTION: Strong 6th Lord suggests victory over legal hurdles.", 85.0
            ))

        # Jupiter (Significator of law and justice)
        jup = planets["Jupiter"]
        if jup.house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "JUSTICE MODIFIER: Well-placed Jupiter supports favorable legal outcomes.", 80.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Focus on resolution of disputes and administrative matters.", 75.0
        ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Saturn", l6_name], [6, 10, 1])

        summary_template = (
            "Legal matters and conflict resolution show {promise} natal strength. "
            "Current alignment is {strength} for administrative success with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Legal & Disputes", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Verify documentation and evidence during Saturn transition windows.",
            "Traditional Jupiter-based justice rituals support truth.",
            "Maintain transparency in all formal dealings."
        ]
        return res
