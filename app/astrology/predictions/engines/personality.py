from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction

class PersonalityPredictionEngine:
    """
    Hardened Personality & Essence Engine (Phase 4).
    Evaluates Ascendant, Moon Sign, and Lagna Lord dignity.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        planets = chart.planets
        house_lords = chart.house_lords

        # 1. LAGNA & LAGNA LORD (Natal Promise)
        l1_name = house_lords[1]
        l1 = planets[l1_name]

        promise_level = "MODERATE"
        if "Exalted" in l1.dignity or l1.dignity == "Own Sign":
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"NATAL PROMISE: Strong Lagna Lord {l1_name} indicates physical and mental vitality.", 90.0
            ))

        # 2. MOON DISPOSITION (Mental State)
        moon = planets["Moon"]
        if moon.house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "MENTAL ESSENCE: Moon in a Kendra/Trikona supports emotional stability.", 70.0
            ))

        # 3. YOGAS (Gaja Kesari, etc.)
        for yoga in chart.yogas:
             if yoga["name"] in ["Gaja Kesari Yoga", "Pancha Mahapurusha"]:
                 evidence.append(CorroborationEngine.create_evidence(
                    "YOGA_SUPPORT", f"YOGA MODIFIER: {yoga['name']} enhances leadership and character.", 85.0
                ))

        summary_template = (
            "Your personality and mental essence show a {promise} natal foundation. "
            "Hierarchical synthesis results in a {score}% match for character strength."
        )

        return CorroborationEngine.synthesize("Personality & Essence", promise_level, evidence, summary_template)
