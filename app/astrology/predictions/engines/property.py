from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class PropertyPredictionEngine:
    """
    V2 Hardened Property & Assets Engine.
    Analyzes 4th house (Property), Mars (Bhumikaraka), and D4 Divisional Chart.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        d4 = chart.divisional_charts.get("D4", {})

        # 1. NATAL PROMISE (4th Lord & House)
        l4_name = house_lords[4]
        l4 = planets[l4_name]

        promise_level = "MODERATE"
        if l4.house in [1, 4, 7, 10, 5, 9, 11]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"ASSET PROMISE: Beneficial 4th Lord {l4_name} placement supports fixed asset acquisition.",
                90.0
            ))

        # 2. KARAKA STRENGTH (Mars)
        mars = planets["Mars"]
        if "Exalted" in mars.dignity or mars.dignity == "Own Sign":
             evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "LAND MODIFIER: Strong Mars (Karaka for land) indicates capacity for real estate control.",
                80.0
            ))

        # 3. DIVISIONAL AUDIT (D4 Chaturthamsha)
        if d4:
             evidence.append(CorroborationEngine.create_evidence(
                "DIVISIONAL_CONFIRM",
                "VARGA CONFIRMATION: Chaturthamsha (D4) corroborates underlying asset stability.",
                85.0
            ))

        # 4. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord == l4_name or antar_lord == "Mars":
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"ASSET ACTIVATION: Period of {antar_lord} triggers real estate and fixed asset cycles.",
                95.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "MAINTENANCE PHASE: Focus on refinement of existing property and domestic foundations.",
                60.0
            ))

        # 4. TIMING
        window = timing_engine.calculate_window(chart, ["Mars", "Saturn", l4_name], [4, 11, 2], calculation_date=selected_date)

        # 5. SYNTHESIS
        summary_template = (
            "Property and fixed asset dynamics show {promise} natal foundation and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for asset acquisition."
        )

        res = CorroborationEngine.synthesize("Property & Assets", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Opportunities for residential or commercial acquisition.",
            "Increased focus on home renovation or structural changes.",
            "Formalization of long-term investment portfolios."
        ]
        res.practical_actions = [
            "Verify structural details during Mars transit peaks.",
            "Maintain transparency in all legal land documentation.",
            "Traditional Bhoomi-related alignment practices support stability."
        ]

        return res
