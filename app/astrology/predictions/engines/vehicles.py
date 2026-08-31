from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class VehiclesPredictionEngine:
    """
    V2 Hardened Vehicles & Mobility Engine.
    Evaluates 4th house and Venus (Vahanakaraka).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (4th House)
        l4_name = house_lords[4]

        promise_level = "MODERATE"
        if planets[l4_name].house in [1, 4, 7, 10, 5, 9, 11]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"MOBILITY PROMISE: Beneficial 4th Lord {l4_name} supports acquisition of vehicles.",
                80.0
            ))

        # Venus (Karaka for luxury/vehicles)
        ven = planets["Venus"]
        if ven.shadbala_score and ven.shadbala_score > 1.1:
             evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "LUXURY MODIFIER: Strong Venus indicates potential for high-quality mobility.",
                85.0
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord == l4_name or antar_lord == "Venus":
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"MOBILITY ACTIVATION: Period of {antar_lord} triggers asset acquisition cycles.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Life-period focuses on maintenance of current assets.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Venus", "Mars", l4_name], [4, 11], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Potential for vehicle acquisition and mobility shows {promise} potential. "
            "Current alignment is {strength} for upgrades with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Vehicles & Mobility", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Upgrading personal or professional transport.",
            "Increased focus on journey-related safety and comfort.",
            "Changes in mobility-related documentation or registration."
        ]
        res.practical_actions = [
            "Verify safety features during lunar peak windows.",
            "Traditional vehicle-sanctifying practices are recommended.",
            "Observe Venus-based alignment for smoothness in journeys."
        ]

        return res
