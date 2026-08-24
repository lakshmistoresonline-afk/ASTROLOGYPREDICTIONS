from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_family_prediction(chart: CanonicalChart, domain_type: str = "Family Support", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """General Family & Lineage Analysis: 2nd house and D12."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 2nd HOUSE (FAMILY LINEAGE & WEALTH)
    l2_name = house_lords[2]
    l2 = planets[l2_name]
    factors.append(EvidenceEngine.create_factor(
        "2nd Lord Placement", "lord", "positive" if l2.house not in [6, 8, 12] else "negative", 10,
        f"2nd Lord {l2_name} in House {l2.house}: Indicates the nature of your early family environment and lineage."
    ))

    # 2. HOUSE OCCUPANTS
    benefics = ["Jupiter", "Venus", "Moon", "Mercury"]
    malefics = ["Mars", "Saturn", "Rahu", "Ketu"]
    h2_planets = [p for p, info in planets.items() if info.house == 2]

    for p in h2_planets:
        if p in benefics:
            factors.append(EvidenceEngine.create_factor("Benefic in 2nd", "house", "positive", 8, f"{p} in the 2nd house brings harmony and sweet speech to family interactions."))
        if p in malefics:
            factors.append(EvidenceEngine.create_factor("Malefic in 2nd", "house", "negative", 8, f"{p} in the 2nd house may cause friction or bluntness in family communication."))

    # Varga Confirmation (D12)
    varga_confirmed = False
    if "D12" in chart.divisional_charts:
        varga_confirmed = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Stability of family heritage confirmed in D12 chart."))

    # 3. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Family Focus", "transit", "positive", 5, "Current transits bring focus to family matters and domestic responsibilities."))

    summary_template = "Family lineage and domestic support strength: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Family Support",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
