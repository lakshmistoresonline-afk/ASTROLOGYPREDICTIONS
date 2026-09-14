from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class PersonalityPredictionEngine:
    """
    V3 Authoritative Personality & Essence Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural identity promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = None) -> DomainPrediction:
        evidence = []
        planets = chart.planets
        house_lords = chart.house_lords

        promise_level = "MODERATE"
        if event_type:
            from ..v5_natal_promise import evaluate_natal_promise
            np_res = evaluate_natal_promise(chart, "PERSONALITY", event_type)
            if np_res["promise_level"] != "INSUFFICIENT_EVIDENCE":
                if np_res["promise_level"] in ["STRONG_PROMISE", "MODERATE_PROMISE"]:
                    promise_level = "STRONG"
                elif np_res["promise_level"] == "WEAK_PROMISE" or np_res["promise_level"] == "WITHHELD":
                    promise_level = "CONDITIONAL"

                evidence.append(CorroborationEngine.create_evidence(
                    "NATAL_PROMISE",
                    f"NATAL PROMISE: Structural {event_type} support is {np_res['promise_level']} (Score: {np_res['promise_score']}).",
                    float(np_res['promise_score']) * 100.0,
                    rationale=f"Authoritative event-specific evaluation: {len(np_res['positive_evidence'])} positive items.",
                    source_layer="NATAL", evidence_type="INDEPENDENT"
                ))

        # 2. DASHA ACTIVATION
        l1_name = house_lords[1]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = [l1_name, "Sun", "Moon"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "personal")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                "STABILITY PHASE: Life-period focuses on inner self-reflection and personal growth.",
                60.0, group="SECONDARY"
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Sun", "Moon", l1_name], [1, 4],
                                                calculation_date=selected_date, domain="Personality & Essence")
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Personal expression and core identity show {promise} natal baseline and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for self-actualization."
        )

        res = CorroborationEngine.synthesize("Personality & Essence", promise_level, evidence, summary_template, timing_window=window)
        return res
