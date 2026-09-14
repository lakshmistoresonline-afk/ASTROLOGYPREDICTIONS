from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class TravelPredictionEngine:
    """
    V3 Authoritative Travel Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural travel promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = None) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        promise_level = "MODERATE"
        if event_type:
            from ..v5_natal_promise import evaluate_natal_promise
            np_res = evaluate_natal_promise(chart, "TRAVEL", event_type)
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
        l9_name = house_lords[9]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = [l9_name, house_lords[3], "Moon"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "travel")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                "STABILITY PHASE: Life-period focuses on domestic continuity and routine stability.",
                60.0, group="SECONDARY"
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Moon", "Mercury", l9_name], [3, 9, 12],
                                                calculation_date=selected_date, domain="Travel & Horizons")
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Mobility and travel horizons show {promise} natal foundation and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for movement."
        )

        res = CorroborationEngine.synthesize("Travel & Horizons", promise_level, evidence, summary_template, timing_window=window)
        return res
