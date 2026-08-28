from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_property_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Assets Analysis with Weighted Hierarchy.
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords
    d4 = chart.divisional_charts.get("D4", {})

    # 1. PRIMARY: DASHA ACTIVATION
    from ..dasha import calculate_vimshottari
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord")

    is_property_antar = (antar_lord == house_lords[4] or
                          antar_lord == "Mars" or
                          antar_lord == "Venus")

    if is_property_antar:
        evidence.append(CorroborationEngine.create_evidence(
            "Dasha", f"Current period ({antar_lord}) activates asset and home sectors.",
            95.0, weight=SignalWeight.PRIMARY, planet=antar_lord
        ))

    # 2. SECONDARY: 4th HOUSE (Natal Assets)
    l4_name = house_lords[4]
    l4 = planets[l4_name]
    if l4.house in [1, 4, 7, 10, 5, 9, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"4th Lord {l4_name} is well-placed in House {l4.house}, supporting stability.",
            80.0, weight=SignalWeight.SECONDARY, planet=l4_name, house=4
        ))

    # 3. SECONDARY: MARS STRENGTH
    mars = planets["Mars"]
    if "Exalted" in mars.dignity or mars.dignity == "Own Sign":
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", "Mars is naturally strong, granting capacity for land ownership.",
            85.0, weight=SignalWeight.SECONDARY, planet="Mars"
        ))

    # 4. SUPPORTING: DIVISIONAL CONFIRMATION (D4)
    if d4:
        d4_lagna = d4.get("Lagna", 0)
        d4_l4 = d4.get(l4_name)
        if d4_l4 is not None:
            h_v = (d4_l4 - d4_lagna + 12) % 12 + 1
            if h_v in [1, 4, 7, 10]:
                evidence.append(CorroborationEngine.create_evidence(
                    "Varga", f"Chaturthamsha (D4) corroborates asset stability with 4th Lord in H{h_v}.",
                    75.0, weight=SignalWeight.SUPPORTING
                ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Mars", "Venus", l4_name]
    window = timing_engine.calculate_window(chart, supporting, [4, 11, 2])

    summary_template = (
        "Property and fixed asset potential is {strength} corroborated. "
        "Overall score for real estate and home stability is {score}% based on integrated indicators."
    )

    return CorroborationEngine.synthesize("Property & Assets", evidence, summary_template, timing_window=window)
