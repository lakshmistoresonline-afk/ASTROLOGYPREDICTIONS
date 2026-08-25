from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine

def get_health_prediction(chart: CanonicalChart, domain_type: str = "Health & Vitality", timing_data: Optional[Dict[str, Any]] = None) -> DomainPrediction:
    """Vitality Analysis: 1st, 6th, 8th, 12th houses, Sun, and Moon."""
    factors = []
    planets = chart.planets
    house_lords = chart.house_lords

    # 1. LAGNA LORD (VITALITY)
    ll_name = house_lords[1]
    ll = planets[ll_name]

    if "Exalted" in ll.dignity:
        factors.append(EvidenceEngine.create_factor("Lagna Lord Strength", "lord", "positive", 20, "Lagna Lord is Exalted: Exceptional natural vitality and immunity."))
    elif "Debilitated" in ll.dignity:
        factors.append(EvidenceEngine.create_factor("Lagna Lord Strength", "lord", "negative", 15, "Lagna Lord is Debilitated: Physical vitality may be low; requires care."))

    # 2. 6th HOUSE (DISEASE)
    sixth_lord_name = house_lords[6]
    sixth_lord = planets[sixth_lord_name]
    if sixth_lord.house in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("6th Lord Placement", "lord", "negative", 10, "6th Lord is in a challenging house: Indicates potential for recurring health issues."))

    # 3. SUN (VITALITY)
    sun = planets["Sun"]
    if "Exalted" in sun.dignity:
        factors.append(EvidenceEngine.create_factor("Sun Dignity", "planet", "positive", 10, "Sun is Exalted: Strong core vitality and leadership energy."))

    # 4. MOON (MENTAL HEALTH)
    moon = planets["Moon"]
    if moon.house in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("Moon Placement", "planet", "negative", 8, "Moon in a dusthana house: May indicate emotional sensitivity or mental stress."))

    # 5. RECOVERABILITY (8th HOUSE)
    l8_name = house_lords[8]
    l8 = planets[l8_name]
    if "Exalted" in l8.dignity or l8.dignity == "Own Sign":
        factors.append(EvidenceEngine.create_factor("Life Force", "lord", "positive", 10, "Strong 8th Lord favors longevity and the ability to recover from deep physical transformations."))

    # Varga Confirmation
    varga_confirmed = False
    if "D30" in chart.divisional_charts:
        varga_confirmed = True
        factors.append(EvidenceEngine.create_factor("Varga Confirmation", "varga", "positive", 10, "Trishamsha (D30) analysis provides deeper insight into potential health challenges."))

    # 5b. Advanced Health Points
    # A. 64th Navamsha from Moon (Khara)
    khara_lon = chart.sensitive_points.get("64th Navamsha (Moon)")
    if khara_lon is not None:
        khara_rashi = int(khara_lon // 30)
        # Is any malefic sitting in Khara Rashi?
        for p_name, p_info in planets.items():
            if p_info.rashi == khara_rashi and p_name in ["Saturn", "Mars", "Rahu", "Ketu"]:
                factors.append(EvidenceEngine.create_factor(
                    "Khara Obstruction", "planet", "negative", 15,
                    f"Sensitive Point (64th Navamsha) is influenced by {p_name}, suggesting areas of health requiring vigilance."
                ))

    # B. Dagtha Rashi (Burnt signs for the Tithi)
    if chart.asc_rashi in chart.dagtha_rashis:
        factors.append(EvidenceEngine.create_factor(
            "Burned Vitality", "house", "negative", 12,
            "Lagna falls in a Dagtha Rashi (Burnt sign), which traditionally may lower natural immunity if not balanced by other factors."
        ))

    # C. Kala Purusha Analysis (Body Parts)
    from .health_data import RASHI_BODY_PARTS, PLANET_BODY_PARTS
    for name in ["Saturn", "Mars", "Rahu", "Ketu"]:
        p = planets[name]
        if p.house in [6, 8, 12]:
             factors.append(EvidenceEngine.create_factor(
                 "Physical Vulnerability", "planet", "negative", 8,
                 f"{name} in {RASHI_BODY_PARTS.get(p.rashi, 'Body')} segment indicates area needing care. Potential impact: {', '.join(PLANET_BODY_PARTS.get(name, []))}."
             ))

    # D. Upagraha Influence (Gulika/Mandi)
    gulika = planets.get("Gulika")
    if gulika and gulika.house in [1, 6, 8]:
        factors.append(EvidenceEngine.create_factor(
            "Karmic Health Pressure", "planet", "negative", 15,
            f"Gulika in House {gulika.house}: This sensitive point suggests deeper karmic triggers or chronic sensitivities requiring holistic care."
        ))

    # E. Ayurvedic Dosha Analysis (Vata, Pitta, Kapha)
    dosha_scores = {"Vata": 0, "Pitta": 0, "Kapha": 0}
    # Simplified mapping:
    # Vata: Saturn, Rahu, Mercury (mixed)
    # Pitta: Sun, Mars, Ketu
    # Kapha: Moon, Jupiter, Venus

    mapping = {
        "Sun": "Pitta", "Moon": "Kapha", "Mars": "Pitta", "Mercury": "Vata",
        "Jupiter": "Kapha", "Venus": "Kapha", "Saturn": "Vata", "Rahu": "Vata", "Ketu": "Pitta"
    }

    for p_name, p_info in planets.items():
        if p_name in mapping:
            weight = 2 if p_name == ll_name else 1
            dosha_scores[mapping[p_name]] += weight

    dominant_dosha = max(dosha_scores, key=dosha_scores.get)
    factors.append(EvidenceEngine.create_factor(
        "Ayurvedic Constitution", "constitution", "neutral", 0,
        f"Dominant Ayurvedic influence: {dominant_dosha}. This constitution suggests specific dietary and lifestyle paths for optimal health."
    ))

    # F. Specific Disease Indicators (Example: Diabetes, Heart, Bone)
    # Heart: Sun, 4th House, Leo
    if planets["Sun"].house in [6, 8, 12] or house_lords[4] in [6, 8, 12]:
        factors.append(EvidenceEngine.create_factor("Circulatory System", "organ", "negative", 5, "Sun and 4th Lord placements suggest vigilance regarding heart and blood pressure."))

    # Bones: Saturn, 10th House, Capricorn
    if planets["Saturn"].dignity == "Debilitated":
        factors.append(EvidenceEngine.create_factor("Skeletal System", "organ", "negative", 5, "Debilitated Saturn suggests potential for bone or joint-related sensitivities."))

    from .medical import get_medical_astrology_insights
    med_insights = get_medical_astrology_insights(chart)
    for mi in med_insights:
        factors.append(EvidenceEngine.create_factor("Medical Signature", "medical", "negative", 5, mi))

    # 6. Timing Integration
    t_conf = False
    if timing_data:
        t_conf = timing_data.get("transit_confirmed", False)
        if timing_data.get("total_timing_score", 0) < 0.4:
            factors.append(EvidenceEngine.create_factor("Caution Period", "transit", "negative", 10, "Current planetary cycles suggest a period where extra attention to health and vitality is recommended."))

    summary_template = (
        domain_type + " alignment is {score}%. "
        "With {confidence} confidence, the analysis suggests "
        + ("exceptional natural resilience and high energy levels currently." if ll.house in [1, 4, 7, 10, 5, 9, 11] and "Exalted" in ll.dignity else "that maintaining physical and mental balance should be a priority through disciplined lifestyle choices.")
    )

    return analyze_domain(
        domain_type,
        factors,
        summary_template,
        varga_data={"confirmed": varga_confirmed},
        transit_data={"confirmed": t_conf},
        chart=chart
    )
