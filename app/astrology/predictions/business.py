from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_business_prediction(chart: CanonicalChart, domain_type: str = "Business & Entrepreneurship", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Business & Trading Analysis: 2nd, 7th, 10th, 11th houses and Mercury, Mars."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 7th HOUSE (PARTNERSHIPS & PUBLIC)
    l7_name = house_lords[7]
    l7 = planets[l7_name]
    if l7.house in [1, 7, 10, 11]:
        factors.append(EvidenceEngine.create_factor("7th Lord Placement", "lord", "positive", 12, "Strong 7th lord supports successful partnerships and public dealings."))

    # 2. MERCURY (TRADING & INTELLECT)
    merc = planets["Mercury"]
    if "Exalted" in merc.dignity or merc.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Mercury Strength", "planet", "positive", 15, "Strong Mercury indicates a talent for trading, commerce, and strategic business planning."))

    # 3. MARS (ENTERPRISE & RISK)
    mars = planets["Mars"]
    if "Exalted" in mars.dignity:
        factors.append(EvidenceEngine.create_factor("Mars Strength", "planet", "positive", 10, "Exalted Mars provides the energy and risk-taking capacity needed for independent enterprise."))

    # 4. WEALTH CONNECTION (2nd and 11th)
    l2_name = house_lords[2]
    l11_name = house_lords[11]
    if l7.rashi == planets[l2_name].rashi or l7.rashi == planets[l11_name].rashi:
        factors.append(EvidenceEngine.create_factor("Business Revenue", "lord", "positive", 10, "Link between partnership lord and wealth lords indicates high business profit potential."))

    # 5. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Expansion Period", "transit", "positive", 10, "Current planetary alignments are ideal for business expansion or starting new ventures."))

    summary_template = domain_type + " trajectory: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        transit_data={"confirmed": t_conf},
        chart=chart
    )
