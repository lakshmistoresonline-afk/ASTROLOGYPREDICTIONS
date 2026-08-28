from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_marriage_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Relationship Analysis with Weighted Hierarchy (Phase 10/18).
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords
    d9 = chart.divisional_charts.get("D9", {})

    # 1. PRIMARY: DASHA ACTIVATION
    from ..dasha import calculate_vimshottari
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord")

    is_marriage_antar = (antar_lord == house_lords[7] or
                          antar_lord == "Venus" or
                          antar_lord == "Jupiter")

    if is_marriage_antar:
        evidence.append(CorroborationEngine.create_evidence(
            "Dasha", f"Current period ({antar_lord}) activates relationship triggers.",
            90.0, weight=SignalWeight.PRIMARY, planet=antar_lord
        ))

    # 2. SECONDARY: NATAL POTENTIAL (7th House)
    l7_name = house_lords[7]
    l7 = planets[l7_name]
    if l7.house in [1, 4, 7, 10, 5, 9, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"7th Lord {l7_name} is well-placed in House {l7.house}, supporting unions.",
            80.0, weight=SignalWeight.SECONDARY, planet=l7_name, house=7
        ))
    elif l7.house in [6, 8, 12]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"7th Lord {l7_name} in Dusthana indicates relational tests or delays.",
            -35.0, weight=SignalWeight.CONFLICT, planet=l7_name
        ))

    # 3. SECONDARY: DIVISIONAL CONFIRMATION (D9)
    if d9:
        d9_lagna = d9.get("Lagna", 0)
        d9_l7 = d9.get(l7_name)
        if d9_l7 is not None:
            h_v = (d9_l7 - d9_lagna + 12) % 12 + 1
            if h_v in [1, 4, 7, 10, 5, 9]:
                evidence.append(CorroborationEngine.create_evidence(
                    "Varga", f"Navamsa (D9) corroborates stability with 7th Lord in House {h_v}.",
                    85.0, weight=SignalWeight.SECONDARY
                ))

    # 4. SUPPORTING: VENUS STRENGTH
    venus = planets["Venus"]
    if "Exalted" in venus.dignity or venus.dignity == "Own Sign":
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", "Venus is naturally strong, granting relational harmony.",
            75.0, weight=SignalWeight.SUPPORTING, planet="Venus"
        ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Venus", "Jupiter", l7_name]
    window = timing_engine.calculate_window(chart, supporting, [7, 11, 2])

    summary_template = (
        "Relational trajectory is {strength} corroborated. "
        "Overall partnership score is {score}% based on integrated weighted indicators."
    )

    return CorroborationEngine.synthesize("Marriage & Relationships", evidence, summary_template, timing_window=window)
