from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_property_prediction(chart: CanonicalChart, domain_type: str = "Property & Assets", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Assets Analysis: 4th House, Mars, and D4 (Chaturthamsha)."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 4th HOUSE (FIXED ASSETS & HOME)
    l4_name = house_lords[4]
    l4 = planets[l4_name]
    factors.append(EvidenceEngine.create_factor(
        "4th Lord Placement", "lord", "positive" if l4.house in [1, 4, 5, 9, 10, 11] else "negative", 10,
        f"4th Lord {l4_name} in House {l4.house}: Primary indicator for home and real estate potential."
    ))

    # 2. MARS (KARAKA FOR LAND)
    mars = planets["Mars"]
    if "Exalted" in mars.dignity or mars.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Mars Strength", "planet", "positive", 15, "Strong Mars: Traditionally favorable for land ownership and construction ventures."))

    # 3. D4 CONFIRMATION
    varga_confirmed = False
    d4 = chart.divisional_charts.get("D4", {})
    if d4:
        d4_lagna = d4.get("Lagna", 0)
        d4_pos = d4.get(l4_name)
        if d4_pos is not None:
            rel_h = (d4_pos - d4_lagna + 12) % 12 + 1
            if rel_h in [1, 4, 5, 9, 10, 11]:
                varga_confirmed = True
                factors.append(EvidenceEngine.create_factor("Varga Support", "varga", "positive", 12, f"4th Lord well-placed (H{rel_h}) in Chaturthamsha (D4)."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Acquisition Window", "transit", "positive", 10, "Current planetary cycles are supportive for property acquisition or relocation."))

    summary_template = "Property and real estate trajectory: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Property & Assets",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
