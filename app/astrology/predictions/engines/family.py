from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class FamilyPredictionEngine:
    """
    V2 Hardened Family & Roots Engine.
    Evaluates 2nd (Family), 4th (Mother/Home), and 9th (Father) houses.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (2nd and 4th Houses)
        l2_name = house_lords[2]
        l4_name = house_lords[4]

        promise_level = "MODERATE"
        l2_house = planets[l2_name].house
        if l2_house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: Strong 2nd Lord {l2_name} in Kendra/Trikona indicates deep family roots.",
                90.0, rationale=f"{l2_name} is in house {l2_house}"
            ))
        elif l2_house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 2nd Lord {l2_name} provides stable family foundation.",
                60.0, rationale=f"{l2_name} is in house {l2_house}"
            ))
        elif planets[l2_name].house in [1, 2, 4, 5, 7, 9, 10, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"FAMILY PROMISE: Supportive 2nd Lord {l2_name} placement indicates strong roots.",
                80.0
            ))

        l4_house = planets[l4_name].house
        if l4_house in [1, 4, 7, 10, 5, 9]:
             promise_level = "STRONG"
             evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: Beneficial 4th Lord {l4_name} in Kendra/Trikona supports home stability.",
                90.0, rationale=f"{l4_name} is in house {l4_house}"
            ))
        elif l4_house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 4th Lord {l4_name} provides stable domestic base.",
                60.0, rationale=f"{l4_name} is in house {l4_house}"
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord in [l2_name, l4_name, "Moon"]:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"ROOTS ACTIVATION: Period of {antar_lord} highlights domestic and family sectors.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Focus on maintenance of domestic foundations.",
                65.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Moon", "Venus", l4_name], [2, 4], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Domestic harmony and family support show {promise} natal foundation. "
            "Current alignment is {strength} for family matters with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Family & Roots", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Increased focus on family traditions and gatherings.",
            "Development of domestic infrastructure or home comfort.",
            "Changes in roles or responsibilities within the family unit."
        ]
        res.practical_actions = [
            "Maintain ancestral traditions during lunar peak windows.",
            "Focus on emotional communication within the home.",
            "Traditional family-blessing rituals are supported during this phase."
        ]

        return res
