from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class ForeignSettlementEngine:
    """
    V2 Hardened Foreign Settlement & Immigration Engine.
    Evaluates 9th, 12th, and 7th houses for international movement.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (12th House - Foreign Lands)
        l12_name = house_lords[12]
        l12 = planets[l12_name]

        promise_level = "MODERATE"
        if l12.house in [1, 4, 7, 9, 10]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"HORIZON PROMISE: Link between Home (4H/1H) and Foreign (12H) sectors indicates migration potential.",
                85.0
            ))

        # Rahu (Karaka for Foreign things)
        rahu = planets["Rahu"]
        if rahu.house in [1, 4, 7, 9, 10, 12]:
            evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "EXPANSION MODIFIER: Rahu's placement bolsters desire and opportunity for cross-border movement.",
                80.0
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord == l12_name or antar_lord == "Rahu":
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"MIGRATION ACTIVATION: Period of {antar_lord} triggers movement and relocation cycles.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "LOCAL STABILITY: Life-period focuses on maintenance of current domestic base.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Rahu", "Saturn", l12_name], [12, 9, 7], calculation_date=selected_date)

        # 4. SYNTHESIS
        summary_template = (
            "The potential for international relocation shows {promise} underlying factors. "
            "Current alignment is {strength} for foreign engagement with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Foreign Settlement", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Opportunities for long-distance travel or relocation.",
            "Development of international professional or social networks.",
            "Changes in domestic or residential documentation."
        ]
        res.practical_actions = [
            "Verify immigration protocols during lunar peak windows.",
            "Maintain cultural flexibility during transitional phases.",
            "Traditional journey-blessing practices for foreign lands are recommended."
        ]

        return res
