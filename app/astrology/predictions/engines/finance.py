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
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets

        # 1. NATAL PROMISE (2nd and 11th Houses)
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

        # 2. CONTRADICTIONS (Malefic Aspects to Wealth Houses)
        # (Simplified malefic check)
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
        maha_lord = dasha.get("current_maha", {}).get("lord")
        antar_lord = dasha.get("current_antar", {}).get("lord")

        relevant_lords = [l2_name, l11_name, "Jupiter", "Venus"]
        if antar_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"FINANCIAL ACTIVATION: Life-period of {antar_lord} triggers major wealth generation cycles.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "RESOURCE STABILITY: Current life-period favors consolidation over high-risk expansion.",
                60.0
            ))

        if maha_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                f"DASHA FOUNDATION: Major life-cycle ruled by {maha_lord} provides underlying support for wealth accumulation.",
                60.0
            ))

        # 4. TIMING
        l11_name = house_lords[11]
        window = timing_engine.calculate_window(chart, ["Jupiter", "Venus", l2_name, l11_name], [2, 11, 1], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 5. SYNTHESIS
        summary_template = (
            "Your financial trajectory shows a {promise} foundation with {strength} alignment for growth. "
            "Hierarchical synthesis results in a {score}% confidence score for fiscal security."
        )

        res = CorroborationEngine.synthesize("Finance & Wealth", promise_level, evidence, summary_template, timing_window=window)

        res.manifestations = [
            "Steady increase in liquid assets or savings.",
            "Opportunities for secondary income streams.",
            "Strategic investments reaching a maturation phase."
        ]
        res.practical_actions = [
            "Focus on long-term resource security during this cycle.",
            "Maintain disciplined budgeting to counter temporary malefic pressure.",
            "Evaluate large-scale investments against dasha timing peaks."
        ]

        return res
