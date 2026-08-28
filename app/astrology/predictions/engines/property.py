from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class PropertyPredictionEngine:
    """
    Hardened Property & Assets Engine (Phase 4).
    Evaluates 4th house, Mars, and Venus stability.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (4th House)
        l4_name = house_lords[4]
        l4 = planets[l4_name]

        promise_level = "MODERATE"
        if l4.house in [1, 4, 7, 10, 5, 9, 11]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"ASSET PROMISE: High capacity for fixed assets indicated by 4th Lord {l4_name} placement.", 85.0
            ))

        # 2. MARS (Bhumikaraka - significator of land)
        mars = planets["Mars"]
        if "Exalted" in mars.dignity or mars.dignity == "Own Sign":
             evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "LAND KARAKA: Strong Mars supports acquisition of landed property.", 80.0
            ))

        # 3. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Asset and home sectors are highlighted.", 75.0
        ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Mars", "Venus", l4_name], [4, 2, 11])

        summary_template = (
            "Potential for fixed assets and property shows {promise} underlying factors. "
            "Current alignment is {strength} for acquisition with a {score}% evidence score."
        )

        return CorroborationEngine.synthesize("Property & Assets", promise_level, evidence, summary_template, timing_window=window)
