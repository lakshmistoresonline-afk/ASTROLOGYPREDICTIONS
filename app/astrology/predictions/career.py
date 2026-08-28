from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_career_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Career Analysis with Weighted Evidence Hierarchy (Phase 10/16).
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords
    d10 = chart.divisional_charts.get("D10", {})

    # 1. PRIMARY: DASHA ACTIVATION
    from ..dasha import calculate_vimshottari
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord")

    is_career_antar = (antar_lord == house_lords[10] or
                       planets[antar_lord].house in [10, 11, 1])

    if is_career_antar:
        evidence.append(CorroborationEngine.create_evidence(
            "Dasha", f"Current period ({antar_lord}) activates career houses, creating professional momentum.",
            90.0, weight=SignalWeight.PRIMARY, planet=antar_lord
        ))

    # 2. SECONDARY: NATAL POTENTIAL (D1)
    l10_name = house_lords[10]
    l10 = planets[l10_name]
    if l10.house in [1, 4, 7, 10, 5, 9, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"10th Lord {l10_name} is well-placed in House {l10.house}, indicating strong natal promise.",
            85.0, weight=SignalWeight.SECONDARY, planet=l10_name, house=10
        ))
    elif l10.house in [6, 8, 12]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"10th Lord {l10_name} in Dusthana (House {l10.house}) suggests initial hurdles or service bias.",
            -30.0, weight=SignalWeight.CONFLICT, planet=l10_name
        ))

    # 3. SECONDARY: DIVISIONAL CONFIRMATION (D10)
    if d10:
        d10_lagna = d10.get("Lagna", 0)
        d10_l10 = d10.get(l10_name)
        if d10_l10 is not None:
            h_v = (d10_l10 - d10_lagna + 12) % 12 + 1
            if h_v in [1, 4, 7, 10]:
                evidence.append(CorroborationEngine.create_evidence(
                    "Varga", f"Dashamsha (D10) corroborates professional authority with {l10_name} in Kendra.",
                    85.0, weight=SignalWeight.SECONDARY
                ))

    # 4. SUPPORTING: YOGAS
    for yoga in chart.yogas:
        if "Raja Yoga" in yoga["name"] and (10 in yoga.get("houses", [])):
            evidence.append(CorroborationEngine.create_evidence(
                "Yoga", f"Presence of {yoga['name']} provides supportive social elevation.",
                75.0, weight=SignalWeight.SUPPORTING
            ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Sun", "Saturn", l10_name]
    window = timing_engine.calculate_window(chart, supporting, [10, 11, 6])

    summary_template = (
        "Your professional trajectory is {strength} aligned with your purpose. "
        "Overall career strength score is {score}% based on weighted corroborated factors."
    )

    return CorroborationEngine.synthesize("Career & Authority", evidence, summary_template, timing_window=window)
