from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_speculation_prediction(chart: CanonicalChart, domain_type: str = "Speculation & Trading", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Speculation Analysis: 5th house, 8th house, 11th house and Mercury, Rahu."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 5th HOUSE (SPECULATION)
    l5_name = house_lords[5]
    l5 = planets[l5_name]
    factors.append(EvidenceEngine.create_factor(
        "5th Lord Status", "lord", "positive" if l5.house in [1, 5, 9, 10, 11] else "negative", 15,
        f"5th Lord {l5_name} in House {l5.house} determines your natural luck in speculative ventures."
    ))

    # 2. RAHU (SUDDEN GAINS/RISK)
    rahu = planets["Rahu"]
    if rahu.house in [5, 8, 11]:
        factors.append(EvidenceEngine.create_factor("Rahu Influence", "planet", "positive", 10, "Rahu in speculative sectors indicates an appetite for risk and potential for sudden gains."))

    # 3. MERCURY (TRADING INTELLECT)
    merc = planets["Mercury"]
    if "Exalted" in merc.dignity:
        factors.append(EvidenceEngine.create_factor("Mercury Sharpness", "planet", "positive", 12, "Strong Mercury provides the analytical depth required for successful market trading."))

    # 4. SUDDENNESS (8th HOUSE)
    l8_name = house_lords[8]
    if l8_name in ["Rahu", "Mars"] or planets[l8_name].house == 5:
        factors.append(EvidenceEngine.create_factor("Sudden Volatility", "lord", "negative", 8, "Connection between 8th and 5th lords indicates high volatility in speculative outcomes."))

    # Varga (D9/D10 for professional trading)
    v_conf = False
    if "D9" in chart.divisional_charts:
        v_conf = True

    # Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)

    summary_template = "Market speculation and risk-taking potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
