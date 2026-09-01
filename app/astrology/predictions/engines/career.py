from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class CareerPredictionEngine:
    """
    V2 Hardened Career Engine.
    Deep-dives into 10th House (Action), 11th (Gains), 1st (Identity) and D10 (Dashamsha).
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        d10 = chart.divisional_charts.get("D10", {})

        # 1. NATAL PROMISE (10th Lord & House)
        l10_name = house_lords[10]
        l10 = planets[l10_name]

        promise_level = "MODERATE"
        if l10.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High professional status indicated by Kendra/Trikona placement of 10th Lord {l10_name}.",
                90.0, rationale=f"{l10_name} is in house {l10.house}"
            ))
        elif l10.house in [2, 11]:
            evidence.append(CorroborationEngine.create_evidence(
                "SECONDARY_PROMISE",
                f"SECONDARY PROMISE: Supportive house placement (2/11) for 10th Lord {l10_name} provides stable material gains.",
                60.0, rationale=f"{l10_name} is in house {l10.house}"
            ))
        elif l10.house in [6, 8, 12]:
            promise_level = "CONDITIONAL"
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS",
                f"PROMISE OBSTRUCTION: 10th Lord {l10_name} in Dusthana suggests service orientation or initial delays.",
                -40.0, rationale="Placement in challenging house requires remediation."
            ))

        # 2. STRENGTH ANALYSIS (Shadbala)
        if l10.shadbala_score and l10.shadbala_score > 1.2:
             evidence.append(CorroborationEngine.create_evidence(
                "PLANETARY_STRENGTH",
                f"RESILIENCE MODIFIER: Exceptional Shadbala strength of {l10_name} grants authority and endurance.",
                80.0
            ))

        # 3. DIVISIONAL AUDIT (D10 Dashamsha)
        if d10:
            d10_lagna = d10.get("Lagna", 0)
            if d10_lagna in [0, 4, 8]: # Dharma signs in D10
                 evidence.append(CorroborationEngine.create_evidence(
                    "DIVISIONAL_CONFIRM",
                    "VARGA CONFIRMATION: Dashamsha (D10) supports natural professional leadership.",
                    85.0
                ))

        # 4. DASHA ACTIVATION
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)
        maha_lord = dasha.get("current_maha", {}).get("lord")
        antar_lord = dasha.get("current_antar", {}).get("lord")

        relevant_lords = [l10_name, house_lords[11]]
        if antar_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                f"TEMPORAL ACTIVATION: Current life-period ruled by {antar_lord} triggers major professional themes.",
                90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION",
                "STABILITY PHASE: Life-period focuses on maintenance and refinement of current roles.",
                60.0
            ))

        if maha_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_FOUNDATION",
                f"DASHA FOUNDATION: Major life-cycle ruled by {maha_lord} provides underlying support for professional growth.",
                60.0
            ))

        # 5. TIMING GENERATION
        window = timing_engine.calculate_window(chart, ["Jupiter", l10_name], [10, 11, 1], calculation_date=selected_date)
        if window.get("proximity_weight", 0) > 0:
             evidence.append(CorroborationEngine.create_evidence(
                "TRANSIT_TRIGGER", f"TEMPORAL TRIGGER: {window.get('description')}",
                90.0 * window.get("proximity_weight")
            ))

        # 6. SYNTHESIS
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
