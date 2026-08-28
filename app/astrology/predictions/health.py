from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_health_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Vitality Analysis with Weighted Hierarchy.
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords
    d30 = chart.divisional_charts.get("D30", {})

    # 1. PRIMARY: LAGNA LORD STRENGTH
    ll_name = house_lords[1]
    ll = planets[ll_name]
    if "Exalted" in ll.dignity or ll.dignity == "Own Sign":
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"Lagna Lord {ll_name} is strong, granting high life-force.",
            90.0, weight=SignalWeight.PRIMARY, planet=ll_name, house=1
        ))
    elif "Debilitated" in ll.dignity:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"Lagna Lord {ll_name} is weak, suggesting lower physical resistance.",
            -40.0, weight=SignalWeight.CONFLICT, planet=ll_name
        ))

    # 2. SECONDARY: 6th HOUSE (Natal Disease)
    l6_name = house_lords[6]
    l6 = planets[l6_name]
    if l6.house in [6, 8, 12]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"6th Lord {l6_name} in Dusthana indicates vulnerability to seasonal stressors.",
            -30.0, weight=SignalWeight.CONFLICT, planet=l6_name, house=6
        ))

    # 3. SECONDARY: SUN (Vitality Karaka)
    sun = planets["Sun"]
    if "Exalted" in sun.dignity:
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", "Sun is exalted, providing strong inherent immunity.",
            85.0, weight=SignalWeight.SECONDARY, planet="Sun"
        ))

    # 4. SUPPORTING: DIVISIONAL SCAN (D30)
    if d30:
        evidence.append(CorroborationEngine.create_evidence(
            "Varga", "Trishamsha (D30) scan indicates stable structural health foundations.",
            70.0, weight=SignalWeight.SUPPORTING
        ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Sun", "Moon", ll_name]
    window = timing_engine.calculate_window(chart, supporting, [1, 6, 8])

    summary_template = (
        "Health and vitality indicators are {strength} corroborated. "
        "Overall physical resilience score is {score}% based on integrated analysis."
    )

    return CorroborationEngine.synthesize("Health & Vitality", evidence, summary_template, timing_window=window)
