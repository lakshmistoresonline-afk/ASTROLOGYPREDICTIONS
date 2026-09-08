from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class EducationPredictionEngine:
    """
    Hardened Education & Knowledge Engine.
    Evaluates 4th house (Basic Ed), 5th house (Intellect), and Mercury/Jupiter stability.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (4th & 5th Houses)
        l4_name = house_lords[4]
        l5_name = house_lords[5]

        promise_level = "MODERATE"

        # Occupancy Promise (V3.14)
        for p_name, p in planets.items():
            if p.house in [4, 5] and p_name in ["Mercury", "Jupiter", "Sun"]:
                 promise_level = "STRONG"
                 evidence.append(CorroborationEngine.create_evidence(
                    "NATAL_PROMISE",
                    f"NATAL SIGNAL: Strong presence in academic houses (H{p.house}) indicates learning focus.",
                    85.0
                 ))

        l4_house = planets[l4_name].house
        if l4_house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High capacity for learning supported by Kendra/Trikona placement of 4th Lord {l4_name}.",
                90.0, rationale=f"{l4_name} is in house {l4_house}"
            ))
        elif l4_house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 4th Lord {l4_name} provides stable educational base.",
                60.0, rationale=f"{l4_name} is in house {l4_house}"
            ))

        # Mercury & Jupiter (Karakas)
        merc = planets["Mercury"]
        jup = planets["Jupiter"]
        if merc.shadbala_score > 1.1:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "INTELLECT MODIFIER: Strong Mercury grants sharp analytical and linguistic skills.", 80.0
            ))
        if jup.house in [1, 4, 7, 10, 5, 9]:
            evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", "WISDOM MODIFIER: Beneficial Jupiter placement supports higher educational attainment.", 75.0
            ))

        # 2. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        l9_name = house_lords[9]
        relevant_lords = [l4_name, l5_name, l9_name, "Mercury", "Jupiter"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "educational")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION", # Changed from ACTIVATION to FOUNDATION for fallback
                "STABILITY PHASE: Life-period favors maintenance of existing knowledge base.",
                65.0, group="SECONDARY"
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Mercury", "Jupiter", "Sun", l4_name, l5_name, l9_name], [4, 5, 9],
                                                calculation_date=selected_date, domain="Education & Knowledge")
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Opportunities for learning and intellectual growth show {promise} natal potential. "
            "Timing alignment is {strength} with a {score}% match based on hierarchical factors."
        )

        event_class = "educational advancement, certification, formal study, skill acquisition, or intellectual project milestones"

        res = CorroborationEngine.synthesize("Education & Knowledge", promise_level, evidence, summary_template,
                                                timing_window=window, what_may_develop=event_class)
        res.practical_actions = [
            "Maintain disciplined study habits during energetic peaks.",
            "Jupiter-based wisdom practices support deep acquisition of knowledge.",
            "Verify academic deadlines and requirements during transition phases."
        ]
        return res
