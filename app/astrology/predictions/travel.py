from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_travel_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Travel Analysis with Weighted Hierarchy.
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. PRIMARY: DASHA ACTIVATION
    from ..dasha import calculate_vimshottari
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord")

    is_travel_antar = (antar_lord == house_lords[3] or
                        antar_lord == house_lords[9] or
                        antar_lord == house_lords[12] or
                        antar_lord == "Rahu")

    if is_travel_antar:
        evidence.append(CorroborationEngine.create_evidence(
            "Dasha", f"Current period ({antar_lord}) activates movement and foreign sectors.",
            90.0, weight=SignalWeight.PRIMARY, planet=antar_lord
        ))

    # 2. SECONDARY: 9th HOUSE (Natal Long Travel)
    l9_name = house_lords[9]
    l9 = planets[l9_name]
    if l9.house in [1, 7, 9, 12]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"9th Lord {l9_name} is well-placed for international or philosophical journeys.",
            80.0, weight=SignalWeight.SECONDARY, planet=l9_name, house=9
        ))

    # 3. SECONDARY: RAHU (Foreign Indicator)
    rahu = planets["Rahu"]
    if rahu.house in [9, 12]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", "Rahu in foreign sectors suggests unconventional or overseas movement.",
            85.0, weight=SignalWeight.SECONDARY, planet="Rahu"
        ))

    # 4. SUPPORTING: MOON STRENGTH
    moon = planets["Moon"]
    if moon.house in [3, 7, 9, 12]:
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", "Moon in a travel house supports frequent movement.",
            70.0, weight=SignalWeight.SUPPORTING, planet="Moon"
        ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Moon", "Rahu", l9_name]
    window = timing_engine.calculate_window(chart, supporting, [3, 9, 12])

    summary_template = (
        "Journey and travel potential is {strength} corroborated. "
        "Overall movement score is {score}% based on integrated weighted indicators."
    )

    return CorroborationEngine.synthesize("Travel & Journeys", evidence, summary_template, timing_window=window)
