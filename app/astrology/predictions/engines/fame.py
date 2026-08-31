from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class FamePredictionEngine:
    """
    V2 Hardened Fame & Reputation Engine.
    Evaluates 10th house (Action), 1st (Identity), and 5th (Recognition).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (10th and 1st Houses)
        l10_name = house_lords[10]
        l1_name = house_lords[1]

        promise_level = "MODERATE"
        # Dig-Bala (Directional Strength) for Sun or Jupiter in 10th
        if planets["Sun"].house == 10 or planets["Jupiter"].house == 10:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "YOGA_SUPPORT",
                "LEADERSHIP MODIFIER: Powerful directional strength in 10th house indicates high public visibility.",
                90.0
            ))

        l10_house = planets[l10_name].house
        if l10_house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High status potential indicated by Kendra/Trikona placement of 10th Lord {l10_name}.",
                90.0, rationale=f"{l10_name} is in house {l10_house}"
            ))
        elif l10_house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 10th Lord {l10_name} provides stable reputation base.",
                60.0, rationale=f"{l10_name} is in house {l10_house}"
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord in [l10_name, l1_name, "Sun"]:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"RECOGNITION ACTIVATION: Period of {antar_lord} triggers expansion of public identity.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Life-period favors maintenance of existing status.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", l10_name], [10, 1, 5], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "The potential for public recognition and status shows {promise} underlying factors. "
            "Current alignment is {strength} for achievement with a {score}% match."
        )

        res = CorroborationEngine.synthesize("Fame & Reputation", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Recognition within professional or social circles.",
            "Increased visibility in public or administrative roles.",
            "Formalization of status-oriented achievements."
        ]
        res.practical_actions = [
            "Focus on integrity and public service during peak windows.",
            "Traditional Sun-related alignment practices support visibility.",
            "Maintain transparency in professional dealings during this phase."
        ]

        return res
