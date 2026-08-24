from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_legal_prediction(chart: CanonicalChart, domain_type: str = "Legal & Disputes", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Legal & Dispute Analysis: 6th, 7th, 8th houses, Mars, and Jupiter."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 6th HOUSE (ENEMIES & DISPUTES)
    sixth_lord_name = house_lords[6]
    sixth_lord = planets[sixth_lord_name]

    if sixth_lord.house in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("6th Lord Placement", "lord", "negative", 10, "6th Lord in a dusthana: May indicate vulnerability to legal disputes or hidden challenges."))
    elif "Exalted" in sixth_lord.dignity:
        factors.append(EvidenceEngine.create_factor("6th Lord Strength", "lord", "positive", 15, "Strong 6th Lord: Inherent ability to overcome opponents and win legal battles."))

    # 2. JUPITER (JUSTICE)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter.dignity:
        factors.append(EvidenceEngine.create_factor("Jupiter Strength", "planet", "positive", 10, "Favorable Jupiter: Protection from law and fair outcomes in disputes."))

    # 3. MARS (LITIGATION & AGGRESSION)
    mars = planets["Mars"]
    if "Debilitated" in mars.dignity:
        factors.append(EvidenceEngine.create_factor("Mars Dignity", "planet", "negative", 10, "Weak Mars: Lack of courage in legal battles or potential for losses."))

    # Varga Confirmation
    v_conf = False
    if "D30" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Trishamsha (D30) analysis confirms strength in navigating disputes and legal challenges."))

    # 3b. Advanced Legal Insights
    # A. Gnatikaraka (GK) - Indicator of challenges/rivals
    gk_name = chart.jaimini_karakas.get("Gnatikaraka (GK) - Challenges")
    if gk_name:
        gk = planets[gk_name]
        factors.append(EvidenceEngine.create_factor(
            "Conflict Indicator", "planet", "negative" if gk.house in [1, 7, 10] else "neutral", 12,
            f"{gk_name} is your Gnatikaraka. Its position in House {gk.house} defines your relationship with rivals and legal hurdles."
        ))

    # B. Argala on 6th House (Support in conflicts)
    argala_6 = chart.argala_analysis.get(6, {})
    if argala_6.get("primary"):
        # Check if benefics are providing argala to 6th house
        for p_name, p_info in planets.items():
            if p_info.house in argala_6["primary"] and p_name in ["Jupiter", "Venus", "Mercury"]:
                factors.append(EvidenceEngine.create_factor(
                    "Structural Support", "house", "positive", 15,
                    f"Strong structural intervention (Argala) from {p_name} facilitates favorable legal resolutions."
                ))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) < 0.4:
            factors.append(EvidenceEngine.create_factor("Adversarial Window", "transit", "negative", 10, "Current planetary cycles suggest caution in legal matters; avoid unnecessary confrontation."))

    summary_template = domain_type + " potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
