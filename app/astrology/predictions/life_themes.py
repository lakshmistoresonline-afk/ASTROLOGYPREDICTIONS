from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_life_themes_prediction(chart: CanonicalChart, domain_type: str = "General Life Themes", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """General Life Themes Analysis: Navamsha, Atmakaraka, and major yogas."""
    factors = []
    planets = chart.planets

    # 1. ATMAKARAKA (SOUL'S DESIRE)
    ak_name = chart.jaimini_karakas.get("Atmakaraka")
    if ak_name:
        factors.append(EvidenceEngine.create_factor(
            "Atmakaraka", "planet", "positive", 20,
            f"The soul's journey is deeply tied to the nature of {ak_name} in your chart."
        ))

    # 2. MAJOR YOGAS
    if chart.yogas:
        factors.append(EvidenceEngine.create_factor(
            "Yoga Presence", "yoga", "positive", 15,
            "Multiple planetary yogas indicate a life defined by significant achievements or unique experiences."
        ))

    # Varga Confirmation
    v_conf = False
    if "D1" in chart.divisional_charts or "D9" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "General life themes are confirmed across multiple divisional charts."))

    # 3. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Theme Activation", "transit", "positive", 8, "Major life themes are currently being activated by current planetary movements."))

    summary_template = "Primary life themes and soul direction: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "General Life Themes",
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
