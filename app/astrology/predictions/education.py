from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_education_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Academic Analysis with Weighted Hierarchy.
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords
    d24 = chart.divisional_charts.get("D24", {})

    # 1. PRIMARY: DASHA ACTIVATION
    from ..dasha import calculate_vimshottari
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord")

    is_edu_antar = (antar_lord == house_lords[4] or
                     antar_lord == house_lords[5] or
                     antar_lord == "Mercury" or
                     antar_lord == "Jupiter")

    if is_edu_antar:
        evidence.append(CorroborationEngine.create_evidence(
            "Dasha", f"Current period ({antar_lord}) activates learning and intelligence triggers.",
            90.0, weight=SignalWeight.PRIMARY, planet=antar_lord
        ))

    # 2. SECONDARY: 5th HOUSE (Intelligence)
    l5_name = house_lords[5]
    l5 = planets[l5_name]
    if l5.house in [1, 4, 7, 10, 5, 9, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"5th Lord {l5_name} is well-placed in House {l5.house}, supporting focus.",
            85.0, weight=SignalWeight.SECONDARY, planet=l5_name, house=5
        ))

    # 3. SECONDARY: MERCURY (Logic Karaka)
    mercury = planets["Mercury"]
    if "Exalted" in mercury.dignity or mercury.dignity == "Own Sign":
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", "Mercury is naturally sharp, granting analytical depth.",
            80.0, weight=SignalWeight.SECONDARY, planet="Mercury"
        ))

    # 4. SUPPORTING: DIVISIONAL SCAN (D24)
    if d24:
        evidence.append(CorroborationEngine.create_evidence(
            "Varga", "Siddhamsha (D24) indicates a high capacity for specialized knowledge.",
            70.0, weight=SignalWeight.SUPPORTING
        ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Mercury", "Jupiter", l5_name]
    window = timing_engine.calculate_window(chart, supporting, [4, 5, 9])

    summary_template = (
        "Educational and intellectual capacity is {strength} aligned. "
        "Overall knowledge-acquisition potential score is {score}% based on weighted indicators."
    )

    return CorroborationEngine.synthesize("Education & Knowledge", evidence, summary_template, timing_window=window)
