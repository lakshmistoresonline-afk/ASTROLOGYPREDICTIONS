from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_travel_prediction(chart: CanonicalChart, domain_type: str = "Travel & Journeys", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Travel Analysis: 3rd, 7th, 9th houses and Moon."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 3rd HOUSE (SHORT TRAVEL)
    l3_name = house_lords[3]
    l3 = planets[l3_name]
    if l3.house in [1, 3, 7, 9, 11]:
        factors.append(EvidenceEngine.create_factor("Short Travel Potential", "lord", "positive", 8, f"3rd Lord {l3_name} well-placed for frequent short-distance journeys."))

    # 2. 9th HOUSE (LONG TRAVEL / PILGRIMAGE)
    l9_name = house_lords[9]
    l9 = planets[l9_name]
    if l9.house in [1, 7, 9, 12]:
        factors.append(EvidenceEngine.create_factor("Long Distance Travel", "lord", "positive", 12, f"9th Lord {l9_name} supports long-distance travel and philosophical journeys."))

    # 3. MOON (THE KARAKA FOR TRAVEL)
    moon = planets["Moon"]
    if moon.rashi in [3, 7, 11] or moon.house in [3, 7, 9, 12]:
        factors.append(EvidenceEngine.create_factor("Lunar Support", "planet", "positive", 8, "Moon in a movable sign or travel house indicates a natural love for movement and travel."))

    # Varga Confirmation
    v_conf = False
    if "D4" in chart.divisional_charts or "D9" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Divisional chart analysis supports frequent movement and travel success."))

    # 3b. Advanced Travel Insights
    # A. Punya Saham (Fortune Point) - Sometimes triggers travel
    p_saham = chart.sahams.get("Punya Saham")
    if p_saham is not None:
        ps_rashi = int(p_saham // 30)
        # Is travel lord linked to Punya Saham?
        if l9.rashi == ps_rashi:
            factors.append(EvidenceEngine.create_factor(
                "Fortunate Travel", "yoga", "positive", 15,
                "The Fortune Point (Saham) is linked to your travel house, suggesting journeys bring significant luck."
            ))

    # B. Nadi Connection: Rahu (Travel Karaka)
    rahu_links = chart.nadi_connections.get("Rahu", [])
    if "Moon" in rahu_links or "Venus" in rahu_links:
        factors.append(EvidenceEngine.create_factor(
            "Nadi Travel Path", "yoga", "positive", 12,
            "Nadi links between Rahu and personal planets indicate a destiny involving significant movement or relocation."
        ))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Travel Window", "transit", "positive", 10, "Current planetary alignments are ideal for planning or embarking on journeys."))

    summary_template = "Travel and journey potential: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Travel & Journeys",
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
