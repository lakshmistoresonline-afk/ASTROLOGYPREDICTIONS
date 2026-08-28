from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class HealthPredictionEngine:
    """
    Hardened Health Engine (Phase 4).
    Evaluates Ascendant, 6th house, and Sun/Moon vitality.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (Lagna & 6th House)
        l1_name = house_lords[1]
        l1 = planets[l1_name]

        promise_level = "MODERATE"
        if "Exalted" in l1.dignity or l1.dignity == "Own Sign":
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "VITALITY PROMISE: Strong Lagna Lord supports physical resilience.", 90.0
            ))

        # 6th Lord check (Conflicts)
        l6_name = house_lords[6]
        if planets[l6_name].house == 1:
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS", "HEALTH PRESSURE: 6th Lord in Lagna indicates susceptibility to seasonal stress.", -30.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Focus on daily routine and physical maintenance.", 75.0
        ))

        # 3. MODIFIERS (Sun/Moon vitality)
        sun = planets["Sun"]
        if sun.house in [1, 10, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "VITALITY MODIFIER: Strong Sun placement bolsters natural immunity.", 20.0
            ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Sun", "Moon", l1_name], [1, 5, 9])

        summary_template = (
            "Health and vitality factors show {promise} underlying strength. "
            "Current alignment is {strength} for physical maintenance with a {score}% evidence score."
        )

        # IMPORTANT: Health remains INSUFFICIENT DATA for medical claims (Req 47)
        res = CorroborationEngine.synthesize("Health & Vitality", promise_level, evidence, summary_template, timing_window=window)
        res.validation_status = "INSUFFICIENT DATA"
        res.practical_guidance = [
            "This is not a medical diagnosis. Consult a doctor for any health concerns.",
            "Maintain consistent physical routine and hygiene.",
            "Observe standard safety protocols for daily activity."
        ]
        return res
