from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class HealthPredictionEngine:
    """
    Hardened Health & Vitality Engine (Phase 4).
    Evaluates Ascendant, 6th house, and Sun/Moon vitality.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        l1_name = house_lords[1]
        l1 = planets[l1_name]
        l6_name = house_lords[6]
        l6 = planets[l6_name]

        # 1. NATAL PROMISE (Lagna & 6th House)
        promise_level = "MODERATE"
        if "Exalted" in l1.dignity or l1.dignity == "Own Sign":
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"VITALITY PROMISE: Strong Lagna Lord {l1_name} provides deep physical resilience.", 90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"PHYSICAL BASELINE: Lagna Lord {l1_name} establishes a stable vitality foundation.", 60.0
            ))

        # 2. STRENGTH (Shadbala)
        if l1.shadbala_score > 1.1:
             evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "IMMUNITY MODIFIER: High Shadbala of Ascendant Lord bolsters natural recovery.", 75.0
            ))

        # 3. DUSTHANA DYNAMICS (Conflicts)
        if l6.house == 1 or l1.house == 6:
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS", "HEALTH PRESSURE: Interaction between Lagna and 6th Lord suggests susceptibility to seasonal stress.", -35.0
            ))

        # 4. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord == l6_name:
             evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION", f"CURRENT ACTIVATION: Period of 6th Lord {antar_lord} requires disciplined routine.", 80.0
            ))
        else:
             evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION", "STABILITY PHASE: Life-period favors maintenance and balanced physical habits.", 65.0
            ))

        # 5. MODIFIERS (Sun/Moon vitality)
        sun = planets["Sun"]
        if sun.house in [1, 10, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "VITALITY MODIFIER: Strong Sun placement grants natural internal immunity.", 25.0
            ))

        # 6. TIMING
        window = timing_engine.calculate_window(chart, ["Sun", "Moon", l1_name], [1, 5, 9])

        summary_template = (
            "Health and vitality factors show {promise} underlying factors. "
            "Current alignment is {strength} for maintenance with a {score}% evidence score."
        )

        # IMPORTANT: Health remains INSUFFICIENT DATA for medical claims (Req 47)
        res = CorroborationEngine.synthesize("Health & Vitality", promise_level, evidence, summary_template, timing_window=window)
        res.validation_status = "INSUFFICIENT DATA"
        res.practical_guidance = [
            "This is not a medical diagnosis. Consult a doctor for any health concerns.",
            "Maintain consistent physical routine and hygiene.",
            "Observe standard safety protocols for daily activity."
        ]
        return res
