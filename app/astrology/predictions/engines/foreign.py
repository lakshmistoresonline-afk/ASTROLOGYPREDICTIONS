from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class ForeignSettlementEngine:
    """
    V3 Authoritative Foreign Settlement & Immigration Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural foreign promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "FOREIGN_SETTLEMENT") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "FOREIGN_SETTLEMENT"
        np_res = evaluate_natal_promise(chart, "FOREIGN", ev)

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
        l12_name = house_lords[12]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = [l12_name, house_lords[9], "Rahu", "Moon"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "foreign")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                "STABILITY PHASE: Life-period focuses on local stabilization and domestic consolidation.",
                60.0, group="SECONDARY"
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Rahu", "Moon", l12_name], [9, 12, 3], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Foreign settlement dynamics show {promise} natal foundation and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for international movement."
        )

        res = CorroborationEngine.synthesize("Foreign Settlement", promise_level, evidence, summary_template, timing_window=window)
        return res
