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

        # 1. NATAL PROMISE
        l10_name = house_lords[10]
        l10 = planets[l10_name]

        promise_level = "MODERATE"

        # Occupancy Promise
        for p_name, p in planets.items():
            if p.house == 10 and p_name in ["Jupiter", "Sun", "Mars", "Saturn", "Mercury"]:
                 promise_level = "STRONG"
                 evidence.append(CorroborationEngine.create_evidence(
                    "NATAL_PROMISE",
                    f"NATAL SIGNAL: Strong presence in the 10th house ({p_name}) supports major career events.",
                    85.0, source_layer="NATAL", evidence_type="INDEPENDENT"
                 ))

        if l10.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE",
                f"NATAL PROMISE: High professional status indicated by Kendra/Trikona placement of 10th Lord {l10_name}.",
                90.0, rationale=f"{l10_name} is in house {l10.house}",
                source_layer="NATAL", evidence_type="INDEPENDENT"
            ))
        elif l10.house in [6, 8, 12]:
             evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS",
                f"CAREER FRICTION: 10th Lord {l10_name} in Dusthana ({l10.house}) suggests instability or shifts.",
                -70.0, source_layer="NATAL", evidence_type="CONFLICT"
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
                40.0, rationale="Placement in challenging house requires remediation."
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

        relevant_lords = {l10_name, house_lords[11], house_lords[9], "Sun", "Jupiter", "Mars"}
        # Include major occupants as relevant lords (V3.15)
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

        # 5. TIMING GENERATION
        window = timing_engine.calculate_window(chart, ["Jupiter", "Mars", l10_name], [10, 11, 1],
                                                calculation_date=selected_date, domain="Career & Authority")
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
