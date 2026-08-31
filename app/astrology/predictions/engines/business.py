from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class BusinessPredictionEngine:
    """
    V2 Hardened Business & Entrepreneurship Engine.
    Evaluates 7th house (Partnerships/Market), 10th (Action), and 11th (Gains).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (7th and 10th Lords)
        l7_name = house_lords[7]
        l10_name = house_lords[10]
        l7 = planets[l7_name]
        l10 = planets[l10_name]

        promise_level = "MODERATE"
        # Business Yoga: 7th lord and 10th lord association
        if l7.rashi == l10.rashi or l7.house == 10 or l10.house == 7:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "YOGA_SUPPORT",
                "BUSINESS YOGA: Link between Market (7H) and Action (10H) supports independent enterprise.",
                90.0, rationale=f"Exchange or conjunction between {l7_name} and {l10_name}."
            ))

        # Mercury (Karaka for trade)
        merc = planets["Mercury"]
        if merc.shadbala_score and merc.shadbala_score > 1.2:
            evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                "COMMERCE MODIFIER: Strong Mercury grants sharp analytical and trading precision.",
                85.0
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord in [l7_name, l10_name, "Mercury"]:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"COMMERCIAL ACTIVATION: Period of {antar_lord} triggers active trade and market engagement.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Life-period favors consolidation of existing market presence.",
                65.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Mercury", "Sun", l7_name, l10_name], [7, 10, 11], calculation_date=selected_date)

        # 4. SYNTHESIS
        summary_template = (
            "Independent venture and market activity show {promise} natal promise. "
            "Current alignment is {strength} for commercial expansion with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Business & Enterprise", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "New partnership opportunities or strategic alliances.",
            "Increased focus on market research and scalability.",
            "Formalization of independent action-oriented projects."
        ]
        res.practical_actions = [
            "Leverage strategic partnerships during lunar peak windows.",
            "Verify contractual details when Mercury is under pressure.",
            "Traditional trade-sanctifying rituals support long-term stability."
        ]

        return res
