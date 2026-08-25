from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine, are_associated

def get_spirituality_prediction(chart: CanonicalChart, domain_type: str = "Spirituality & Moksha", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Spiritual Analysis: 5th, 9th, 12th houses, Ketu, and Jupiter."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. 12th HOUSE (LIBERATION & MOKSHA)
    twelfth_lord_name = house_lords[12]
    twelfth_lord = planets[twelfth_lord_name]
    if twelfth_lord.house in [9, 12]:
        factors.append(EvidenceEngine.create_factor("12th Lord Placement", "lord", "positive", 15, "Strong connection to higher realms and spiritual liberation."))

    # 2. KETU (KARAKA FOR MOKSHA)
    ketu = planets["Ketu"]
    if ketu.house in [9, 12]:
        factors.append(EvidenceEngine.create_factor("Ketu Placement", "planet", "positive", 20, "Ketu in a spiritual house: Deep inclination toward detachment and enlightenment."))

    # 3. JUPITER (DHARMA & WISDOM)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter.dignity:
        factors.append(EvidenceEngine.create_factor("Jupiter Strength", "planet", "positive", 10, "Favorable Jupiter: Growth through traditional wisdom and dharmic practices."))

    # 4. MEDITATION (SATURN-KETU)
    saturn = planets["Saturn"]
    if saturn.house in [9, 12] or are_associated("Saturn", "Ketu", planets):
        factors.append(EvidenceEngine.create_factor("Introspective Depth", "planet", "positive", 8, "Saturn's connection to spiritual sectors favors disciplined meditation and inner silence."))

    # 5. D20 CONFIRMATION
    varga_confirmed = False
    d20 = chart.divisional_charts.get("D20", {})
    if d20:
        varga_confirmed = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Vimshamsha (D20) indicates a significant spiritual journey."))

    # 5b. Advanced Soul Path Indicators
    # A. Atmakaraka (AK) - Soul's Desire
    ak_name = chart.jaimini_karakas.get("Atmakaraka (AK) - Soul")
    if ak_name:
        ak = planets[ak_name]
        # AK in 12th from AK Navamsha (Karakamsha) is ideal, but for now use D1
        if ak.house in [9, 12]:
            factors.append(EvidenceEngine.create_factor(
                "Soul Alignment", "planet", "positive", 20,
                f"Your Soul Planet ({ak_name}) is placed in a moksha house, indicating a lifetime dedicated to spiritual evolution."
            ))

    # B. Karakamsha (Lagna in AK sign in D9)
    # (Simplified: check if Lagna Lord and AK are associated)
    if are_associated(house_lords[1], ak_name, planets):
        factors.append(EvidenceEngine.create_factor(
            "Karmic Focus", "yoga", "positive", 15,
            "Strong link between self and soul-planet facilitates clear spiritual direction."
        ))

    # 6. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) > 0.6:
            factors.append(EvidenceEngine.create_factor("Awakening Period", "transit", "positive", 10, "Current planetary alignments are ideal for spiritual retreats, initiation, or deep practice."))

    summary_template = (
        "Spiritual path alignment is {score}%. "
        "With {confidence} confidence, your soul trajectory suggests "
        + ("a deep innate capacity for higher knowledge and detachment." if ketu.house in [9, 12] or twelfth_lord.house in [9, 12] else "that spiritual growth will come through active service and balanced worldly engagement.")
    )

    return analyze_domain(
        "Spirituality & Moksha",
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
