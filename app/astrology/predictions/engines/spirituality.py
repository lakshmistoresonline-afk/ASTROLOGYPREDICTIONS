from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class SpiritualityPredictionEngine:
    """
    V3 Authoritative Spirituality & Inner Growth Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural spiritual promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "SPIRITUAL_INITIATION") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "SPIRITUAL_INITIATION"
        np_res = evaluate_natal_promise(chart, "SPIRITUALITY", ev)

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

        # 2. DASHA ACTIVATION
        l9_name = house_lords[9]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = [l9_name, house_lords[12], "Jupiter", "Ketu"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "spiritual")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                "STABILITY PHASE: Life-period focuses on inner contemplation and philosophical synthesis.",
                60.0, group="SECONDARY"
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Ketu", l9_name], [9, 12, 5], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Spiritual growth and philosophical alignment show {promise} natal foundation and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for inner evolution."
        )

        res = CorroborationEngine.synthesize("Spirituality & Inner Growth", promise_level, evidence, summary_template, timing_window=window)
        return res
