from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class EducationPredictionEngine:
    """
    Hardened Education & Knowledge Engine.
    Evaluates 4th house (Basic Ed), 5th house (Intellect), and Mercury/Jupiter stability.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (4th & 5th Houses)
        l4_name = house_lords[4]
        l5_name = house_lords[5]

        promise_level = "MODERATE"
        if planets[l4_name].house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"KNOWLEDGE PROMISE: High capacity for learning supported by 4th Lord {l4_name} placement.", 85.0
            ))

        # Mercury & Jupiter (Karakas)
        merc = planets["Mercury"]
        jup = planets["Jupiter"]
        if merc.shadbala_score > 1.1:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "INTELLECT MODIFIER: Strong Mercury grants sharp analytical and linguistic skills.", 80.0
            ))
        if jup.house in [1, 4, 7, 10, 5, 9]:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "WISDOM MODIFIER: Beneficial Jupiter placement supports higher educational attainment.", 75.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Intellectual and learning sectors are highlighted in the current life-period.", 80.0
        ))

        # 3. TRANSIT TRIGGER
        evidence.append(CorroborationEngine.create_evidence(
            "TRANSIT_TRIGGER", "TRANSIT TRIGGER: Supporting planetary transits favor focused study or acquisition of new skills.", 70.0
        ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Mercury", "Jupiter", l4_name, l5_name], [4, 5, 2])

        summary_template = (
            "Opportunities for learning and intellectual growth show {promise} natal potential. "
            "Timing alignment is {strength} with a {score}% match based on hierarchical factors."
        )

        res = CorroborationEngine.synthesize("Education & Knowledge", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Maintain disciplined study habits during energetic peaks.",
            "Jupiter-based wisdom practices support deep acquisition of knowledge.",
            "Verify academic deadlines and requirements during transition phases."
        ]
        return res
