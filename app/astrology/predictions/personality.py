from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_personality_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Identity Analysis with Weighted Hierarchy.
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. PRIMARY: LAGNA & LAGNA LORD (Physical Self)
    l1_name = house_lords[1]
    l1 = planets[l1_name]
    if l1.house in [1, 4, 7, 10, 5, 9, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"Lagna Lord {l1_name} is well-placed in House {l1.house}, granting high life-force.",
            90.0, weight=SignalWeight.PRIMARY, planet=l1_name, house=1
        ))

    # 2. SECONDARY: SUN (Soul Essence)
    sun = planets["Sun"]
    if sun.house in [1, 9, 10, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", "Sun is well-placed, indicating strong self-awareness and leadership potential.",
            80.0, weight=SignalWeight.SECONDARY, planet="Sun"
        ))

    # 3. SECONDARY: MOON (Mental Disposition)
    moon = planets["Moon"]
    if moon.house in [1, 4, 5, 7, 9]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", "Moon placement supports emotional intelligence and intuitive depth.",
            75.0, weight=SignalWeight.SECONDARY, planet="Moon"
        ))

    # 4. SUPPORTING: ATMAKARAKA (Soul Indicator)
    ak_name = chart.jaimini_karakas.get("Atmakaraka (AK) - Soul")
    if ak_name:
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", f"Soul Indicator ({ak_name}) provides consistent internal guidance.",
            70.0, weight=SignalWeight.SUPPORTING, planet=ak_name
        ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Sun", "Moon", l1_name]
    window = timing_engine.calculate_window(chart, supporting, [1, 5, 9])

    summary_template = (
        "Your core identity and essence are {strength} corroborated. "
        "Overall life-force alignment score is {score}% based on integrated weighted indicators."
    )

    return CorroborationEngine.synthesize("Personality & Essence", evidence, summary_template, timing_window=window)
