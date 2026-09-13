from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class CareerPredictionEngine:
    """
    V3 Authoritative Career Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "PROMOTION") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        d10 = chart.divisional_charts.get("D10", {})

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "PROMOTION"
        np_res = evaluate_natal_promise(chart, "CAREER", ev)

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
                        f"CAREER FRICTION: {item['rationale']}",
                        -70.0, source_layer="NATAL", evidence_type="CONFLICT"
                    ))

        # 2. DASHA ACTIVATION
        l10_name = house_lords[10]
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = {l10_name, house_lords[11], house_lords[9], "Sun", "Jupiter", "Mars"}
        for p_name, p in planets.items():
            if p.house in [10, 11, 1, 5, 9]:
                relevant_lords.add(p_name)

        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, list(relevant_lords), "professional")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                "STABILITY PHASE: Life-period focuses on maintenance and refinement of current roles.",
                60.0, group="SECONDARY"
            ))

        # 3. TIMING GENERATION
        window = timing_engine.calculate_window(chart, ["Jupiter", "Mars", l10_name], [10, 11, 1],
                                                calculation_date=selected_date, domain="Career & Authority")
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Your professional trajectory has a {promise} natal foundation and is currently {strength} aligned. "
            "Hierarchical synthesis shows a {score}% match for status expansion."
        )

        res = CorroborationEngine.synthesize("Career & Authority", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Increased responsibility in existing roles.",
            "Recognition from administrative or governmental authorities.",
            "Development of new action-oriented skillsets."
        ]
        res.practical_actions = [
            "Leverage professional energetic peaks for authority expansion.",
            "Maintain transparency in all formal documentation.",
            "Focus on integrity-driven leadership during this cycle."
        ]

        return res
