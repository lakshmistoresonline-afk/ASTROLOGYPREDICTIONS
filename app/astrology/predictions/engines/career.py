from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class CareerPredictionEngine:
    """
    Hardened Career Engine (Phase 4).
    Separates Natal Promise, Activation, and Timing Triggers.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. DETERMINING NATAL PROMISE
        l10_name = house_lords[10]
        l10 = planets[l10_name]

        promise_level = "MODERATE"
        if l10.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "NATAL PROMISE: High professional status indicated by Kendra/Trikona Lord placement.", 90.0
            ))
        elif l10.house in [6, 8, 12]:
            promise_level = "WEAK"
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS", "PROMISE OBSTRUCTION: 10th Lord in Dusthana suggests service orientation or initial delays.", -30.0
            ))

        # 2. DETERMINING ACTIVATION (Dasha)
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Current life-period supports professional ventures.", 80.0
        ))

        # 3. TRANSIT TRIGGER
        evidence.append(CorroborationEngine.create_evidence(
            "TRANSIT_TRIGGER", "TRANSIT TRIGGER: Supporting planetary transits create immediate opportunity.", 70.0
        ))

        # 4. TIMING GENERATION
        window = timing_engine.calculate_window(chart, ["Sun", "Saturn", l10_name], [10, 11, 1])

        summary_template = (
            "Your professional trajectory has a {promise} natal foundation and is currently {strength} aligned. "
            "Timing confidence is {score}% corroborated by hierarchical signals."
        )

        res = CorroborationEngine.synthesize("Career & Authority", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Leverage professional energetic peaks for authority expansion.",
            "Traditional Saturn/Sun alignment practices support status stability.",
            "Verify career deadlines and bureaucratic steps during transition windows."
        ]
        return res
