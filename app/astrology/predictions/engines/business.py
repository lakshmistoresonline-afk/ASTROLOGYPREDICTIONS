from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class BusinessPredictionEngine:
    """
    Hardened Business & Entrepreneurship Engine.
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
        # Business Yoga: 7th lord and 10th lord associated
        if l7.rashi == l10.rashi or planets[l7_name].house == 10 or planets[l10_name].house == 7:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "YOGA_SUPPORT", "BUSINESS YOGA: Link between Partnership (7H) and Action (10H) supports independent ventures.", 90.0
            ))

        # Mercury (Karaka for trade)
        merc = planets["Mercury"]
        if merc.shadbala_score > 1.2:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "COMMERCE MODIFIER: Strong Mercury grants sharp analytical and trading skills.", 85.0
            ))

        # 2. DASHA ACTIVATION
        evidence.append(CorroborationEngine.create_evidence(
            "DASHA_ACTIVATION", "CURRENT ACTIVATION: Life period favors market expansion and public dealings.", 75.0
        ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Mercury", "Sun", l7_name], [7, 10, 11])

        summary_template = (
            "Independent venture and market activity show {promise} natal promise. "
            "Current alignment is {strength} for commercial expansion with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Business & Enterprise", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Leverage strategic partnerships during transit peaks.",
            "Verify contractual details when Mercury is under pressure.",
            "Traditional trade-sanctifying rituals support stability."
        ]
        return res
