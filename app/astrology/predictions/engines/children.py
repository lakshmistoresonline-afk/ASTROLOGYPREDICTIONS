from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class ChildrenPredictionEngine:
    """
    V3 Authoritative Children & Legacy Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural children/legacy promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "CHILD_BIRTH") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "CHILD_BIRTH"
        np_res = evaluate_natal_promise(chart, "CHILDREN", ev)

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
                        f"CREATIVE PRESSURE: {item['rationale']}",
                        -50.0, source_layer="NATAL", evidence_type="CONFLICT"
                    ))

        # 2. DASHA ACTIVATION
        l5_name = house_lords[5]
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        maha_lord = dasha.get("current_maha", {}).get("lord")
        antar_lord = dasha.get("current_antar", {}).get("lord")

        relevant_lords = [l5_name, "Jupiter"]
        if antar_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"LEGACY ACTIVATION: Period of {antar_lord} triggers sectors of creation and procreation.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "NURTURING PHASE: Focus on maintenance of existing foundations.",
                60.0
            ))

        if maha_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                f"DASHA FOUNDATION: Major life-cycle ruled by {maha_lord} provides underlying support for creative legacy.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Jupiter", "Moon", l5_name], [5, 9, 2], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Growth of lineage and creative legacy shows {promise} natal foundation. "
            "Current alignment is {strength} for developmental milestones with a {score}% evidence score."
        )

        res = CorroborationEngine.synthesize("Children & Creativity", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Increased focus on child-related developmental phases.",
            "Activation of creative or procreative goals.",
            "Development of new intellectual or artistic projects."
        ]
        res.practical_actions = [
            "Maintain nurturing routines during lunar peak windows.",
            "Observe Jupiter-based remedies for lineage protection.",
            "Traditional family-strengthening practices are supported during this phase."
        ]

        return res
