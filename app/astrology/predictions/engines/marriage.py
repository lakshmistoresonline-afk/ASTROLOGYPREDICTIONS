from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class MarriagePredictionEngine:
    """
    V2 Hardened Marriage & Relationship Engine.
    Analyzes 7th House (Partnerships), Venus (Karaka), and D9 (Navamsha).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        d9 = chart.divisional_charts.get("D9", {})

        # 1. NATAL PROMISE (7th Lord & House)
        l7_name = house_lords[7]
        l7 = planets[l7_name]

        promise_level = "MODERATE"
        if l7.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High relationship stability indicated by Kendra/Trikona placement of 7th Lord {l7_name}.",
                90.0, rationale=f"{l7_name} is in house {l7.house}"
            ))
        elif l7.house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 7th Lord {l7_name} provides stable partnership foundation.",
                60.0, rationale=f"{l7_name} is in house {l7.house}"
            ))
        elif l7.house in [6, 8, 12]:
            promise_level = "CONDITIONAL"
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS",
                f"RELATIONSHIP PRESSURE: 7th Lord {l7_name} in Dusthana suggests karmic complexity in partnerships.",
                40.0, rationale=f"{l7_name} in challenging house {l7.house}."
            ))

        # 2. KARAKA STRENGTH (Venus/Jupiter)
        ven = planets["Venus"]
        if "Exalted" in ven.dignity or ven.dignity == "Own Sign":
             evidence.append(CorroborationEngine.create_evidence(
                "YOGA_SUPPORT",
                "HARMONY MODIFIER: Strong Venus (Karaka for marriage) supports aesthetic and emotional bonding.",
                80.0
            ))

        # 3. DIVISIONAL AUDIT (D9 Navamsha)
        if d9:
            d9_l7 = d9.get(l7_name)
            if d9_l7 is not None and d9_l7 in [0, 4, 8, 1, 5, 9]:
                 evidence.append(CorroborationEngine.create_evidence(
                    "DIVISIONAL_CONFIRM",
                    "VARGA CONFIRMATION: Navamsha (D9) corroborates underlying relational longevity.",
                    85.0
                ))

        # 4. DASHA ACTIVATION
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

        # 5. TIMING
        window = timing_engine.calculate_window(chart, ["Venus", "Jupiter", l7_name], [7, 5, 2], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 6. SYNTHESIS
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
