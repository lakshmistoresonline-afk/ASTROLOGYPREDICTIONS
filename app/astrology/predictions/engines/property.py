from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class PropertyPredictionEngine:
    """
    V3 Authoritative Property & Assets Engine.
    Consumes canonical evaluate_natal_promise() as the single source of structural asset promise.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "PROPERTY_PURCHASE") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. AUTHORITATIVE NATAL PROMISE
        from ..v5_natal_promise import evaluate_natal_promise
        ev = event_type or "PROPERTY_PURCHASE"
        np_res = evaluate_natal_promise(chart, "PROPERTY", ev)

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
                        f"ASSET PRESSURE: {item['rationale']}",
                        -50.0, source_layer="NATAL", evidence_type="CONFLICT"
                    ))

        # 2. DASHA ACTIVATION
        l4_name = house_lords[4]
        from ...dasha import calculate_vimshottari
        moon_lon = planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        maha_lord = dasha.get("current_maha", {}).get("lord")
        antar_lord = dasha.get("current_antar", {}).get("lord")

        relevant_lords = [l4_name, "Mars"]
        if antar_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"ASSET ACTIVATION: Period of {antar_lord} triggers real estate and fixed asset cycles.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "MAINTENANCE PHASE: Focus on refinement of existing property and domestic foundations.",
                60.0
            ))

        if maha_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                f"DASHA FOUNDATION: Major life-cycle ruled by {maha_lord} provides underlying support for asset acquisition.",
                60.0
            ))

        # 3. TIMING
        window = timing_engine.calculate_window(chart, ["Mars", "Saturn", l4_name], [4, 11, 2], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 4. SYNTHESIS
        summary_template = (
            "Property and fixed asset dynamics show {promise} natal foundation and {strength} current alignment. "
            "Hierarchical synthesis shows a {score}% match for asset acquisition."
        )

        event_class = "property purchase, sale, registration, financing, renovation, or significant property decision"

        res = CorroborationEngine.synthesize("Property & Assets", promise_level, evidence, summary_template,
                                                timing_window=window, what_may_develop=event_class)

        res.manifestations = [
            "Opportunities for residential or commercial acquisition.",
            "Increased focus on home renovation or structural changes.",
            "Formalization of long-term investment portfolios."
        ]
        res.practical_actions = [
            "Verify structural details during Mars transit peaks.",
            "Maintain transparency in all legal land documentation.",
            "Traditional Bhoomi-related alignment practices support stability."
        ]

        return res
