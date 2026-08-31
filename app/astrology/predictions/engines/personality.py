from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

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
        if l1.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High physical and mental vitality indicated by Kendra/Trikona placement of Lagna Lord {l1_name}.",
                90.0, rationale=f"{l1_name} is in house {l1.house}"
            ))
        elif l1.house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for Lagna Lord {l1_name} provides stable energetic baseline.",
                60.0, rationale=f"{l1_name} is in house {l1.house}"
            ))
        elif "Exalted" in l1.dignity or l1.dignity == "Own Sign":
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"NATAL PROMISE: Strong Lagna Lord {l1_name} indicates high physical and mental vitality.", 90.0
            ))

        # 2. LAGNA CHARACTERISTICS
        asc_rashi = chart.asc_rashi
        r_types = ["Movable (Action-oriented)", "Fixed (Stability-focused)", "Dual (Adaptable)"]
        r_elements = ["Fire (Inspirational)", "Earth (Practical)", "Air (Intellectual)", "Water (Emotional)"]

        evidence.append(CorroborationEngine.create_evidence(
            "MODIFIERS", f"TEMPERAMENT: {r_elements[asc_rashi % 4]} and {r_types[asc_rashi % 3]} nature defines your core approach.", 60.0
        ))

        # 3. MOON DISPOSITION (Mental State)
        moon = planets["Moon"]
        m_nak = moon.nakshatra.name
        if moon.house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", f"MENTAL ESSENCE: Moon in a Kendra/Trikona supports emotional stability and clarity.", 70.0
            ))

        from ..data import NAKSHATRA_MEANINGS
        m_nak_meaning = NAKSHATRA_MEANINGS.get(m_nak, "General lunar influence.")
        evidence.append(CorroborationEngine.create_evidence(
            "MODIFIERS", f"LUNAR SIGNATURE: Birth in {m_nak} Nakshatra indicates: {m_nak_meaning}", 55.0
        ))

        # 4. YOGAS (Gaja Kesari, etc.)
        for yoga in chart.yogas:
             if yoga["name"] in ["Gaja Kesari Yoga", "Pancha Mahapurusha"]:
                 evidence.append(CorroborationEngine.create_evidence(
                    "YOGA_SUPPORT", f"YOGA MODIFIER: {yoga['name']} enhances leadership and character.", 85.0
                ))

        # 5. TIMING
        window = timing_engine.calculate_window(chart, ["Moon", l1_name], [1, 4, 7, 10], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Your personality and mental essence show a {promise} natal foundation. "
            "Hierarchical synthesis results in a {score}% match for character strength."
        )

        res = CorroborationEngine.synthesize("Personality & Essence", promise_level, evidence, summary_template, timing_window=window)
        res.practical_actions = [
            "Observe the activation of the Lagna Lord for self-growth.",
            "Maintain emotional hygiene through meditation and mindfulness.",
            "Traditional Vedic alignment practices for the Moon are supported."
        ]
        return res
