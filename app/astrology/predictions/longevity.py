from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_longevity_prediction(chart: CanonicalChart, domain_type: str = "Vitality & Longevity", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Vitality & Longevity Analysis: 1st, 8th houses and Saturn."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 1st HOUSE (VITALITY)
    l1_name = house_lords[1]
    l1 = planets[l1_name]
    if "Exalted" in l1.dignity or l1.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Lagna Lord Strength", "lord", "positive", 15, "Strong Lagna Lord indicates high natural vitality and structural strength of the body."))
    elif "Debilitated" in l1.dignity:
        factors.append(EvidenceEngine.create_factor("Lagna Lord Strength", "lord", "negative", 10, "Weak Lagna Lord may indicate lower physical resilience."))

    # 2. 8th HOUSE (LONGEVITY)
    l8_name = house_lords[8]
    l8 = planets[l8_name]
    if l8.house not in [6, 12]:
        factors.append(EvidenceEngine.create_factor("8th Lord Placement", "lord", "positive", 10, f"8th Lord {l8_name} in House {l8.house} defines the quality of life duration and transformation."))

    # Shadbala facts for Longevity
    if l1.shadbala_score and l1.shadbala_score > 1.0: # Assuming 1.0 is a decent score
         factors.append(EvidenceEngine.create_factor("Lagna Lord Vitality", "strength", "positive", 15, "Strong Lagna Lord Shadbala supports physical longevity."))

    # 3. SATURN (AYUSH KARAKA)
    saturn = planets["Saturn"]
    if saturn.house in [1, 8, 10]:
        factors.append(EvidenceEngine.create_factor("Saturn Placement", "planet", "positive", 12, "Saturn (Karaka for Longevity) in a strong house traditionally favors a long and disciplined life."))

    # 3b. Mathematical Longevity (Ayurdaya)
    from ..strength.longevity_calculation import calculate_pindayu
    pindayu = calculate_pindayu(planets)
    total_y = sum(pindayu.values())
    if total_y > 60:
        factors.append(EvidenceEngine.create_factor("Pindayu Support", "strength", "positive", 10, f"Mathematical Ayurdaya calculation ({round(total_y, 1)} years) indicates strong inherent life force."))

    # 3c. Ashtakavarga Longevity (Ayurdaya)
    from ..strength.longevity_calculation import calculate_ashtakavarga_ayurdaya
    av_y = calculate_ashtakavarga_ayurdaya(planets, chart.ashtakavarga)
    if av_y > 75:
        factors.append(EvidenceEngine.create_factor("Ashtakavarga Longevity", "ashtakavarga", "positive", 8, f"High bindu contribution across Vargas ({round(av_y, 1)} years) suggests vital stability."))

    # Varga Confirmation
    v_conf = False
    if "D8" in chart.divisional_charts:
        v_conf = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Ashtamsha (D8) analysis supports longevity and vital stability."))

    # 4. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) < 0.4:
            factors.append(EvidenceEngine.create_factor("Caution Period", "transit", "negative", 5, "Current planetary transits suggest a phase where physical energy should be conserved and health prioritized."))

    summary_template = "General vitality and longevity indicators: {score}%. Confidence: {confidence}."

    return analyze_domain(
        "Vitality & Longevity",
        factors,
        summary_template,
        varga_data={"confirmed": v_conf},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
