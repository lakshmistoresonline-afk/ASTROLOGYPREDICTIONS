from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import CanonicalChart, DomainPrediction
from .framework import CorroborationEngine, SignalWeight
from ..timing.precision import timing_engine

def get_finance_prediction(chart: CanonicalChart, selected_date: datetime) -> DomainPrediction:
    """
    Corroborated Wealth Analysis with Weighted Hierarchy (Phase 10/17).
    """
    evidence = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. PRIMARY: DASHA ACTIVATION
    from ..dasha import calculate_vimshottari
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime)
    antar_lord = dasha.get("current_antar", {}).get("lord")

    is_wealth_antar = (antar_lord == house_lords[2] or
                        antar_lord == house_lords[11] or
                        antar_lord == "Jupiter")

    if is_wealth_antar:
        evidence.append(CorroborationEngine.create_evidence(
            "Dasha", f"Current period ({antar_lord}) activates financial sectors, supporting wealth accumulation.",
            95.0, weight=SignalWeight.PRIMARY, planet=antar_lord
        ))

    # 2. SECONDARY: NATAL POTENTIAL (2nd House)
    l2_name = house_lords[2]
    l2 = planets[l2_name]
    if l2.house in [1, 4, 7, 10, 5, 9, 11]:
        evidence.append(CorroborationEngine.create_evidence(
            "D1", f"2nd Lord {l2_name} is well-placed in House {l2.house}, supporting savings.",
            80.0, weight=SignalWeight.SECONDARY, planet=l2_name, house=2
        ))

    # 3. SECONDARY: JUPITER (Karaka for Wealth)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter.dignity or jupiter.dignity == "Own Sign":
        evidence.append(CorroborationEngine.create_evidence(
            "Strength", "Jupiter is naturally strong, granting inherent financial wisdom.",
            90.0, weight=SignalWeight.SECONDARY, planet="Jupiter"
        ))

    # 4. SUPPORTING: ASHTAKAVARGA
    # Check 11th house SAV (Gains)
    asc_rashi = chart.asc_rashi
    h11_rashi = (asc_rashi + 10) % 12
    sav = chart.ashtakavarga.get("SAV", [28]*12)
    if sav[h11_rashi] >= 30:
        evidence.append(CorroborationEngine.create_evidence(
            "Ashtakavarga", f"High SAV in 11th house ({sav[h11_rashi]}) boosts income potential.",
            70.0, weight=SignalWeight.SUPPORTING
        ))

    # 5. DETERMINISTIC TIMING
    supporting = ["Jupiter", "Venus", l2_name]
    window = timing_engine.calculate_window(chart, supporting, [2, 11, 5])

    summary_template = (
        "Your financial blueprint shows {strength} alignment for prosperity. "
        "Overall wealth potential is rated at {score}% based on weighted corroborated signals."
    )

    return CorroborationEngine.synthesize("Finance & Wealth", evidence, summary_template, timing_window=window)
