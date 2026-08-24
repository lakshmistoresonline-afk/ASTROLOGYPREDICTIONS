from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_siblings_prediction(chart: CanonicalChart, domain_type: str = "Sibling Harmony", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Sibling Harmony Analysis: 3rd, 11th houses and Mars, D3."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 3rd HOUSE (YOUNGER SIBLINGS)
    l3_name = house_lords[3]
    l3 = planets[l3_name]
    factors.append(EvidenceEngine.create_factor(
        "Younger Siblings", "lord", "positive" if l3.house not in [6, 8, 12] else "negative", 10,
        f"3rd Lord {l3_name} in House {l3.house} indicates relationship with younger siblings and cousins."
    ))

    # 2. 11th HOUSE (ELDER SIBLINGS)
    l11_name = house_lords[11]
    l11 = planets[l11_name]
    factors.append(EvidenceEngine.create_factor(
        "Elder Siblings", "lord", "positive" if l11.house not in [6, 8, 12] else "negative", 10,
        f"11th Lord {l11_name} in House {l11.house} relates to support and gains from elder siblings."
    ))

    # 3. MARS (SIBLING KARAKA)
    mars = planets["Mars"]
    if "Exalted" in mars.dignity or mars.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Mars Strength", "planet", "positive", 12, "Strong Mars indicates vitality in sibling relationships and mutual support."))

    # Varga Confirmation (D3)
    varga_confirmed = False
    d3 = chart.divisional_charts.get("D3", {})
    if d3:
        varga_confirmed = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Sibling harmony and collective strength supported in D3 chart."))

        # Advanced D3: 3rd from Mars (Co-borns)
        mars_r = d3.get("Mars")
        d3_lagna = d3.get("Lagna", 0)
        if mars_r is not None:
            c_r = (mars_r + 2) % 12 # 3rd from Mars
            c_h = (c_r - d3_lagna + 12) % 12 + 1
            if c_h in [1, 4, 7, 10, 5, 9, 11]:
                factors.append(EvidenceEngine.create_factor("Karmic Sibling Link", "varga", "positive", 12, "Strong indicators for shared destiny and mutual support with siblings in Drekkana."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Interaction Period", "transit", "positive", 5, "Current planetary cycles favor communication and shared activities with siblings."))

    summary_template = "Relationship and harmony with siblings: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Sibling Harmony",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
