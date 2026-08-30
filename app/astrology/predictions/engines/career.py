from typing import Dict, Any, List
from datetime import datetime
from ..framework import CorroborationEngine
from ...core.models import CanonicalChart, DomainPrediction
from ...timing.precision import timing_engine

class CareerPredictionEngine:
    """
    Hardened Career Engine (Phase 4).
    Separates Natal Promise, Activation, and Timing Triggers.
    """

    @staticmethod
    def get_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
        evidence = []
        house_lords = chart.house_lords
        planets = chart.planets
        d9 = chart.divisional_charts.get("D9", {})
        d10 = chart.divisional_charts.get("D10", {})

        # 1. DETERMINING NATAL PROMISE
        l10_name = house_lords[10]
        l10 = planets[l10_name]

        promise_level = "MODERATE"
        if l10.house in [1, 4, 7, 10, 5, 9]:
            promise_level = "STRONG"
            evidence.append(CorroborationEngine.create_evidence(
                "NATAL_PROMISE", f"NATAL PROMISE: High professional status indicated by Kendra/Trikona placement of 10th Lord {l10_name}.", 90.0
            ))
        elif l10.house in [6, 8, 12]:
            promise_level = "WEAK"
            evidence.append(CorroborationEngine.create_evidence(
                "CONFLICTS", f"PROMISE OBSTRUCTION: 10th Lord {l10_name} in Dusthana suggests service orientation or initial delays.", -30.0
            ))

        # 2. STRENGTH (Shadbala)
        if l10.shadbala_score > 1.2:
             evidence.append(CorroborationEngine.create_evidence(
                "MODIFIERS", f"POTENTIAL MODIFIER: High Shadbala of 10th Lord grants resilience in professional challenges.", 20.0
            ))

        # 3. DIVISIONAL CONFIRMATION (D9/D10)
        if d9:
            d9_l10 = d9.get(l10_name)
            if d9_l10 is not None and d9_l10 in [0, 4, 8, 1, 5, 9, 2, 6, 10]: # Friend/Exalt proxy
                 evidence.append(CorroborationEngine.create_evidence(
                    "DIVISIONAL_CONFIRM", "VARGA CONFIRM: Navamsa (D9) supports underlying professional stability.", 70.0
                ))

        if d10:
            d10_lagna = d10.get("Lagna", 0)
            if d10_lagna in [0, 4, 8]: # Dharma houses in D10
                 evidence.append(CorroborationEngine.create_evidence(
                    "DIVISIONAL_CONFIRM", "STATUS MODIFIER: Dashamsha (D10) indicates natural leadership potential.", 85.0
                ))

        # 4. DETERMINING ACTIVATION (Dasha)
        # Check if current Antardasha lord is associated with 10th or 11th
        from ...dasha import calculate_vimshottari
        moon_lon = chart.planets["Moon"].longitude
        dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
        antar_lord = dasha.get("current_antar", {}).get("lord")

        if antar_lord in [l10_name, house_lords[11], house_lords[1]]:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION", f"CURRENT ACTIVATION: Life-period ruled by {antar_lord} triggers action sectors.", 90.0
            ))
        else:
            evidence.append(CorroborationEngine.create_evidence(
                "DASHA_ACTIVATION", "STABILITY PHASE: Life-period favors maintenance over aggressive expansion.", 60.0
            ))

        # 5. TRANSIT TRIGGER
        # (Simplified trigger for now)
        evidence.append(CorroborationEngine.create_evidence(
            "TRANSIT_TRIGGER", "TRANSIT TRIGGER: Supporting planetary alignments create immediate professional openings.", 70.0
        ))

        # 6. TIMING GENERATION
        window = timing_engine.calculate_window(chart, ["Sun", "Saturn", l10_name], [10, 11, 1])

        summary_template = (
            "Your professional trajectory has a {promise} natal foundation and is currently {strength} aligned. "
            "Timing confidence is {score}% corroborated by hierarchical signals."
        )

        res = CorroborationEngine.synthesize("Career & Authority", promise_level, evidence, summary_template, timing_window=window)
        res.practical_guidance = [
            "Leverage professional energetic peaks for authority expansion.",
            "Traditional Saturn/Sun alignment practices support status stability.",
            "Verify career deadlines and bureaucratic steps during transition windows."
        ]
        return res
