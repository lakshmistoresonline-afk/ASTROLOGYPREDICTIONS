from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class MarriagePredictionEngine:
    """
    V3 Authoritative Marriage & Relationship Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural relationship promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "MARRIAGE") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "MARRIAGE"
        np_res = evaluate_natal_promise(chart, "MARRIAGE", ev)

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
                        f"RELATIONSHIP PRESSURE: {item['rationale']}",
                        -50.0, source_layer="NATAL", evidence_type="CONFLICT"
                    ))

        # 2. DASHA ACTIVATION
        l7_name = house_lords[7]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        maha_lord = dasha.get("current_maha", {}).get("lord")
        antar_lord = dasha.get("current_antar", {}).get("lord")

        relevant_lords = [l7_name, "Venus"]
        if antar_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"SOCIAL ACTIVATION: Life-period of {antar_lord} triggers partnership and public union themes.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "RELATIONAL STABILITY: Current life-period focuses on maintenance and internal consistency.",
                65.0
            ))

        if maha_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                f"DASHA FOUNDATION: Major life-cycle ruled by {maha_lord} provides underlying support for relational longevity.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Venus", "Jupiter", l7_name], [7, 5, 2], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Partnership and relational dynamics show {promise} natal strength and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for union themes."
        )

        event_class = "relationship progression, partnership discussion, commitment development, or relationship-status decision"

        res = CorroborationEngine.synthesize("Marriage & Relationships", promise_level, evidence, summary_template,
                                                timing_window=window, what_may_develop=event_class)

        res.manifestations = [
            "Formalization of existing commitments.",
            "Increased focus on shared long-term objectives.",
            "Expansion of social and public networking cycles."
        ]
        res.practical_actions = [
            "Maintain diplomatic communication during transit peaks.",
            "Traditional Vedic alignment practices for Venus support harmony.",
            "Verify commitment transparency during this life-cycle."
        ]

        return res
