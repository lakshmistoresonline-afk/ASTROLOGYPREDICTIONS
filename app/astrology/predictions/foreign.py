from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_foreign_prediction(chart: CanonicalChart, domain_type: str = "Foreign Affairs", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Foreign Affairs Analysis: 7th, 9th, 12th houses, Rahu, and Moon."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords
    asc_rashi = chart.asc_rashi

    # 1. 12th HOUSE (FOREIGN SETTLEMENT)
    l12_name = house_lords[12]
    l12 = planets[l12_name]
    if l12.house in [1, 7, 9, 12]:
        factors.append(EvidenceEngine.create_factor(
            "12th Lord Placement", "lord", "positive", 15,
            f"12th Lord {l12_name} in House {l12.house} indicates strong potential for foreign residence."
        ))

    # 2. 9th HOUSE (LONG TRAVEL)
    l9_name = house_lords[9]
    l9 = planets[l9_name]
    if l9.house in [1, 7, 9, 12]:
        factors.append(EvidenceEngine.create_factor(
            "9th Lord Placement", "lord", "positive", 10,
            f"9th Lord {l9_name} in House {l9.house} favors long-distance journeys and cross-cultural success."
        ))

    # 3. RAHU (FOREIGN KARAKA)
    rahu = planets["Rahu"]
    if rahu.house in [7, 9, 12]:
        factors.append(EvidenceEngine.create_factor(
            "Rahu Placement", "planet", "positive", 12,
            f"Rahu in House {rahu.house} creates deep ambition for foreign experiences."
        ))

    # 4. FOREIGN EMPLOYMENT (Connection between 10th and 12th)
    l10_name = house_lords[10]
    l10 = planets[l10_name]
    if domain_type == "Foreign Employment":
        if l10.house == 12 or l12.house == 10:
            factors.append(EvidenceEngine.create_factor(
                "Foreign Career", "lord", "positive", 15,
                "Direct connection between Career Lord and Foreign House Lord indicates success in international employment."
            ))

    # Varga Confirmation
    v_conf = False
    if "D4" in chart.divisional_charts or "D9" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Divisional chart analysis supports international success and foreign residence."))

    # 5. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.7:
            factors.append(EvidenceEngine.create_factor("Global Activation", "transit", "positive", 10, "Current planetary cycles favor visas, international moves, or global collaboration."))

    summary_template = domain_type + " strength: {score}%. Confidence: {confidence}."

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
