from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class SpiritualityPredictionEngine:
    """
    V2 Hardened Spirituality & Inner Growth Engine.
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
                "NATAL_PROMISE",
                "DHARMIC PROMISE: Strong alignment of wisdom and liberation sectors in the natal map.",
                90.0
            ))

        # Ketu (Karaka for Moksha)
        ketu = planets["Ketu"]
        if ketu.house in [8, 12]:
            evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "MYSTIC MODIFIER: Ketu in a hidden house enhances intuitive and meditative depth.",
                85.0
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord in [l9_name, l12_name, "Jupiter", "Ketu"]:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"INTERNAL ACTIVATION: Period of {antar_lord} favors introspection and study of truth.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Life-period focuses on maintenance of external commitments.",
                65.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Ketu", l9_name, l12_name], [9, 12, 8], calculation_date=selected_date)
        if window.get("timing_confidence") == "HIGH (Transit Verified)":
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"PRECISION TRIGGER: {window.get('description')}", 90.0
            ))

        # 4. SYNTHESIS
        summary_template = (
            "The trajectory for inner growth and wisdom shows {promise} potential. "
            "Current alignment is {strength} for deep practice with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Spirituality & Growth", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Increased interest in philosophical or dharmic study.",
            "Development of consistent meditative or ritual practices.",
            "Detachment from material or social complexities."
        ]
        res.practical_actions = [
            "Leverage dharmic windows for deep meditation and seva.",
            "Traditional pilgrimage or retreat cycles are supported.",
            "Maintain consistency in internal discipline during transitions."
        ]

        return res
