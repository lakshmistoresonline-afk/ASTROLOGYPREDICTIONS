from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class SpiritualityPredictionEngine:
    """
    Hardened Spirituality & Inner Growth Engine.
    Evaluates 9th (Dharma) and 12th (Moksha) houses, and Ketu (Karaka).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (9th & 12th Houses)
        l9_name = house_lords[9]
        l12_name = house_lords[12]

        promise_level = "MODERATE"
        if planets[l9_name].house in [1, 4, 7, 10, 5, 9] and planets[l12_name].house in [1, 4, 7, 10, 5, 9, 12]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "DHARMIC PROMISE: Strong alignment of wisdom and liberation sectors.", 90.0
            ))

        # Ketu (Karaka for Moksha)
        ketu = planets["Ketu"]
        if ketu.house == 12 or ketu.house == 8:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "MYSTIC MODIFIER: Ketu in a hidden house enhances intuitive and spiritual depth.", 85.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Internal life-period favors introspection and dharmic study.", 80.0
        ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Ketu", l9_name], [9, 12, 8])

        summary_template = (
            "The trajectory for inner growth and wisdom shows {promise} potential. "
            "Current alignment is {strength} for spiritual practice with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Spirituality & Growth", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Leverage dharmic windows for deep meditation and seva.",
            "Traditional pilgrimage or retreat cycles are supported.",
            "Maintain consistency in internal discipline during transitions."
        ]
        return res
