from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class EducationPredictionEngine:
    """
    V3 Authoritative Education & Knowledge Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural educational promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "ACADEMIC_ENROLLMENT") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "ACADEMIC_ENROLLMENT"
        np_res = evaluate_natal_promise(chart, "EDUCATION", ev)

        promise_level = "MODERATE"
        if np_res["promise_level"] != "INSUFFICIENT_EVIDENCE":
            if np_res["promise_level"] in ["STRONG_PROMISE", "MODERATE_PROMISE"]:
                promise_level = "STRONG"
            elif np_res["promise_level"] == "WEAK_PROMISE" or np_res["promise_level"] == "WITHHELD":
                promise_level = "CONDITIONAL"

            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: Structural {ev} support is {np_res['promise_level']} (Score: {np_res['promise_score']}).",
                float(np_res['promise_score']) * 100.0,
                rationale=f"Authoritative event-specific evaluation: {len(np_res['positive_evidence'])} positive items.",
                source_layer="NATAL", evidence_type="INDEPENDENT"
            ))

            for item in np_res.get("evidence_items", []):
                if item["polarity"] == "NEGATIVE":
                    evidence.append(CorroborationEngine.create_evidence(
                        "CONFLICTS",
                        f"EDUCATIONAL PRESSURE: {item['rationale']}",
                        -50.0, source_layer="NATAL", evidence_type="CONFLICT"
                    ))

        # 2. DASHA ACTIVATION
        l4_name = house_lords[4]
        l5_name = house_lords[5]
        l9_name = house_lords[9]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = [l4_name, l5_name, l9_name, "Mercury", "Jupiter"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "educational")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
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
