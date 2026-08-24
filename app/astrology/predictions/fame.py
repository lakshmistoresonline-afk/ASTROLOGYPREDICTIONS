from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_fame_prediction(chart: CanonicalChart, domain_type: str = "Fame & Recognition", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Social Status Analysis: 1st, 5th, 10th, 11th houses, Sun, and Rajayogas."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 10th HOUSE (STATUS)
    tenth_lord_name = house_lords[10]
    tenth_lord = planets[tenth_lord_name]
    if "Exalted" in tenth_lord.dignity:
        factors.append(EvidenceEngine.create_factor("10th Lord Strength", "lord", "positive", 25, "10th Lord is Exalted: High potential for fame and public recognition."))

    # 2. SUN (RECOGNITION)
    sun = planets["Sun"]
    if sun.house in [1, 10, 11]:
        factors.append(EvidenceEngine.create_factor("Sun Placement", "planet", "positive", 15, "Sun in a powerful house: Natural charisma and social authority."))

    # 3. YOGAS (RAJAYOGA)
    for y in chart.yogas:
        if "Rajayoga" in y["name"] or "Mahapurusha" in y["name"]:
            factors.append(EvidenceEngine.create_factor("Yoga", "yoga", "positive", 20, f"Presence of {y['name']}: Indicates significant rise in social status."))

    # Varga Confirmation
    v_conf = False
    if "D10" in chart.divisional_charts or "D1" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 12, "Divisional chart analysis supports public recognition and fame potential."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Peak Period", "transit", "positive", 15, "Current planetary cycles are exceptionally favorable for public recognition and success."))

    summary_template = "Fame and social status potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
