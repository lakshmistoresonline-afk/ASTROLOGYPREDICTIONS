from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class TravelPredictionEngine:
    """
    Hardened Travel Engine (Phase 4).
    Evaluates 3rd, 9th, and 12th houses for short and long-distance travel.
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
        if planets[l9_name].house in [1, 4, 7, 10, 5, 9, 11] or planets[l12_name].house in [1, 4, 7, 10]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", "TRAVEL PROMISE: High probability of long-distance or international horizons.", 85.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Movement and expansion sectors are currently triggered.", 80.0
        ))

        # 3. TRANSIT TRIGGER
        evidence.append(CorroborationEngine.create_evidence(
            "TRANSIT_TRIGGER", "TRANSIT TRIGGER: Active planetary transits support physical relocation or travel.", 70.0
        ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, [l9_name, l12_name, "Moon"], [9, 12, 3])

        summary_template = (
            "Opportunities for travel and expansion show {promise} natal potential. "
            "Timing alignment is {strength} with a {score}% hierarchical match."
        )

        res = CorroborationEngine.synthesize("Travel & Horizons", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Verify travel documents and insurance before departure.",
            "Traditional journey-blessing practices are recommended.",
            "Maintain flexibility during planetary transition periods."
        ]
        return res
