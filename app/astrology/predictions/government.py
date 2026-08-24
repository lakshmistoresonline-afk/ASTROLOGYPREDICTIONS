from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_government_prediction(chart: CanonicalChart, domain_type: str = "Government & Authority", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Government & Authority Analysis: Sun, Moon, 10th lord, and Rajayogas."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. SUN (THE KING)
    sun = planets["Sun"]
    if sun.house in [1, 10, 11]:
        factors.append(EvidenceEngine.create_factor("Sun Placement", "planet", "positive", 15, "Sun in a Kendra or Trikona provides natural authority and government favor."))
    if "Exalted" in sun.dignity:
        factors.append(EvidenceEngine.create_factor("Sun Strength", "planet", "positive", 20, "Exalted Sun indicates high level of authority and potentially a top government role."))

    # 2. MOON (THE BUREAUCRACY)
    moon = planets["Moon"]
    if moon.house in [1, 4, 7, 10]:
        factors.append(EvidenceEngine.create_factor("Moon Placement", "planet", "positive", 10, "Strong Moon favors roles involving public administration and social stability."))

    # 3. 10th LORD (AUTHORITY)
    l10_name = house_lords[10]
    l10 = planets[l10_name]
    if l10.house in [1, 9, 10, 11]:
        factors.append(EvidenceEngine.create_factor("10th Lord Placement", "lord", "positive", 12, f"Career Lord {l10_name} in House {l10.house} favors public recognition and authority."))

    # 4. YOGAS
    for y in chart.yogas:
        if "Rajayoga" in y["name"] or "Mahapurusha" in y["name"]:
            factors.append(EvidenceEngine.create_factor("Yoga", "yoga", "positive", 15, f"Presence of {y['name']} indicates a high rise in social and professional status."))

    # Varga Confirmation
    v_conf = False
    if "D10" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 12, "Dashamsha (D10) analysis confirms potential for high-level government or administrative roles."))

    # 5. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Rise Period", "transit", "positive", 10, "Current planetary cycles are exceptionally favorable for government recognition or rise in authority."))

    summary_template = "Government and administrative authority potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Government & Authority",
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
