from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_vehicles_prediction(chart: CanonicalChart, domain_type: str = "Vehicles & Conveyances", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Conveyances Analysis: 4th house and Venus, D16."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 4th HOUSE (CONVEYANCES)
    l4_name = house_lords[4]
    l4 = planets[l4_name]
    if l4.house in [1, 4, 7, 10, 5, 9, 11]:
        factors.append(EvidenceEngine.create_factor(
            "4th Lord Placement", "lord", "positive", 10,
            f"4th Lord {l4_name} in House {l4.house} favors the acquisition of high-quality vehicles and comfortable travel."
        ))

    # 2. VENUS (KARAKA FOR LUXURY VEHICLES)
    venus = planets["Venus"]
    if "Exalted" in venus.dignity or venus.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Venus Strength", "planet", "positive", 15, "Strong Venus provides a natural inclination toward luxury conveyances and comforts."))

    # 3. VARGA (D16 SHODASHAMSHA)
    varga_confirmed = False
    d16 = chart.divisional_charts.get("D16", {})
    if d16:
        d16_lagna = d16.get("Lagna", 0)
        d16_pos = d16.get(l4_name)
        if d16_pos is not None:
            rel_h = (d16_pos - d16_lagna + 12) % 12 + 1
            if rel_h in [1, 4, 5, 9, 10, 11]:
                varga_confirmed = True
                factors.append(EvidenceEngine.create_factor("Varga Support", "varga", "positive", 12, "Favorable D16 (Shodashamsha) indicators for owning conveyances."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Purchase Window", "transit", "positive", 10, "Current planetary cycles are supportive for vehicle acquisition or upgrade."))

    summary_template = "Potential for vehicles and conveyances: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Vehicles & Conveyances",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
