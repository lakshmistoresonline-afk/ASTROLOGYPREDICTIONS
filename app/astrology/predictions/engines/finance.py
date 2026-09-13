from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class FinancePredictionEngine:
    """
    V2 Hardened Finance & Wealth Engine.
    Analyzes 2nd House (Accumulation), 11th (Gains), and 8th (Inheritance/Sudden).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime, event_type: str = "INCOME_EXPANSION") -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (Event-Specific Propagation)
        from ..v5_natal_promise import evaluate_natal_promise
        np_res = evaluate_natal_promise(chart, "FINANCE", event_type)
        if np_res["promise_level"] != "INSUFFICIENT_EVIDENCE":
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: Structural {event_type} support is {np_res['promise_level']} (Score: {np_res['promise_score']}).",
                float(np_res['promise_score']) * 100.0,
                rationale=f"Event-specific evaluation for {event_type}: {len(np_res['positive_evidence'])} positive items.",
                source_layer="NATAL", evidence_type="INDEPENDENT"
            ))

        l2_name = house_lords[2]
        l11_name = house_lords[11]
        l2 = planets[l2_name]
        l11 = planets[l11_name]

        promise_level = "MODERATE"
        if l2.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High wealth capacity indicated by Kendra/Trikona placement of 2nd Lord {l2_name}.",
                90.0, rationale=f"{l2_name} is in house {l2.house}"
            ))
        elif l2.house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 2nd Lord {l2_name} provides stable accumulation.",
                60.0, rationale=f"{l2_name} is in house {l2.house}"
            ))

        if l11.house in [1, 4, 7, 10, 5, 9]:
             evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"GAINS PROMISE: High revenue potential indicated by Kendra/Trikona placement of 11th Lord {l11_name}.",
                90.0, rationale=f"{l11_name} is in house {l11.house}."
            ))
        elif l11.house in [2, 11]:
             evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 11th Lord {l11_name} provides stable gains.",
                60.0, rationale=f"{l11_name} is in house {l11.house}."
            ))

        # 2. CONTRADICTIONS
        if planets["Saturn"].house in [2, 11, 12]:
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS",
                "RESOURCE PRESSURE: Saturnian influence suggests slow accumulation or heavy commitments.",
                30.0
            ))

        # 3. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

        relevant_lords = [l2_name, l11_name, "Jupiter", "Venus"]
        dasha_evidence = CorroborationEngine.audit_dasha_activation(dasha, chart, relevant_lords, "financial")
        if dasha_evidence:
            evidence.extend(dasha_evidence)
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                "RESOURCE STABILITY: Current life-period favors consolidation over high-risk expansion.",
                60.0, group="SECONDARY"
            ))

        # 4. TIMING
        l11_name = house_lords[11]
        window = timing_engine.calculate_window(chart, ["Jupiter", l2_name, l11_name], [2, 11, 1],
                                                calculation_date=selected_date, domain="Wealth & Finance")
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        summary_template = (
            "Your financial baseline has a {promise} natal foundation and is currently {strength} aligned. "
            "Hierarchical synthesis shows a {score}% match for asset accumulation."
        )

        res = CorroborationEngine.synthesize("Wealth & Finance", promise_level, evidence, summary_template, timing_window=window)
        return res
