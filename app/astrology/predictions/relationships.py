from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_relationships_prediction(chart: CanonicalChart, domain_type: str = "Relationship Harmony", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Relationship Analysis: 3rd, 7th, 11th houses and Venus, D9."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 7th HOUSE (PARTNERSHIPS)
    l7_name = house_lords[7]
    l7 = planets[l7_name]
    factors.append(EvidenceEngine.create_factor(
        "7th Lord Placement", "lord", "positive" if l7.house not in [6, 8, 12] else "negative", 10,
        f"7th Lord {l7_name} in House {l7.house} defines the quality of public and personal partnerships."
    ))

    # 2. 11th HOUSE (SOCIAL CIRCLE)
    l11_name = house_lords[11]
    l11 = planets[l11_name]
    factors.append(EvidenceEngine.create_factor(
        "11th Lord Placement", "lord", "positive" if l11.house not in [6, 8, 12] else "negative", 10,
        f"11th Lord {l11_name} in House {l11.house} indicates gains from social circles and friendships."
    ))

    # 3. VENUS (RELATIONSHIP KARAKA)
    venus = planets["Venus"]
    if "Exalted" in venus.dignity:
        factors.append(EvidenceEngine.create_factor("Venus Strength", "planet", "positive", 15, "Strong Venus favors harmony, diplomacy, and mutual respect in all relationships."))

    # Varga Confirmation
    v_conf = False
    if "D9" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Navamsha (D9) analysis confirms the fruit of social and personal relationships."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Social Activation", "transit", "positive", 8, "Current cycles favor meeting new people and strengthening existing bonds."))

    summary_template = "General relationship harmony and social support: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Relationship Harmony",
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
