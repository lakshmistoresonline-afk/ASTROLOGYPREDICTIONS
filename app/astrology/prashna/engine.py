from typing import Dict, Any, List
from datetime import datetime
from ..core.chart import calculate_chart_data
from ..core.models import CanonicalChart

def calculate_prashna_chart(dt: datetime, lat: float, lon: float, tz: str) -> CanonicalChart:
    """Calculate the chart for the exact moment of the question."""
    return calculate_chart_data(dt, lat, lon, tz)

def analyze_prashna(chart: CanonicalChart, question_type: str, panchang: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Standard Prashna (Horary) Analysis.
    Focuses on Lagna, Lagna Lord, and the house relevant to the question.
    """
    planets = chart.planets
    ll_name = chart.house_lords[1]
    lagna_lord = planets[ll_name]

    # Map question type to house
    house_map = {
        "Career": 10, "Marriage": 7, "Finance": 2, "Health": 1,
        "Travel": 9, "Property": 4, "Children": 5, "Education": 5,
        "Business": 7, "Legal": 6, "Fame": 10, "Spirituality": 12,
        "Parents": 4, "Enemies": 6, "Secrets": 8, "Ambition": 11,
        "Victory": 6, "Investment": 5, "Relocation": 4
    }
    target_house = house_map.get(question_type, 1)
    target_lord_name = chart.house_lords[target_house]
    target_lord = planets[target_lord_name]

    # 1. Ithasala Yoga (Applying aspect between LL and TL)
    from ..strength.aspects import get_graha_drishti

    ll_pos = lagna_lord.longitude
    tl_pos = target_lord.longitude

    # Simple relative speed check (Moon is always fastest)
    PLANET_SPEED_RANK = {
        "Moon": 1, "Mercury": 2, "Venus": 3, "Sun": 4,
        "Mars": 5, "Jupiter": 6, "Saturn": 7
    }

    ll_rank = PLANET_SPEED_RANK.get(ll_name, 10)
    tl_rank = PLANET_SPEED_RANK.get(target_lord_name, 10)

    ithasala = False
    # Conjunction
    if lagna_lord.rashi == target_lord.rashi:
        if ll_rank < tl_rank: # LL is faster and behind TL?
             if ll_pos < tl_pos: ithasala = True
        elif tl_rank < ll_rank: # TL is faster and behind LL?
             if tl_pos < ll_pos: ithasala = True

    # Aspect
    ll_aspects = get_graha_drishti(ll_name, lagna_lord.rashi)
    tl_aspects = get_graha_drishti(target_lord_name, target_lord.rashi)

    if target_lord.rashi in ll_aspects or lagna_lord.rashi in tl_aspects:
        association = True
    else:
        association = False

    # 2. Moon's position
    moon = planets["Moon"]

    # 3. Micro-Timing
    hora_lord = panchang.get("current_hora") if panchang else "N/A"
    tatva = panchang.get("tatva", {}).get("name", "N/A")
    tatva_q = panchang.get("tatva", {}).get("quality", "Neutral") if panchang else "Neutral"

    verdict = "Neutral"
    if (association or ithasala) and moon.house not in [6, 8, 12]:
        verdict = "Positive"
    elif moon.house in [6, 8, 12]:
        verdict = "Challenging"
    elif not association and not ithasala:
        verdict = "Delayed/Unclear"

    # Final confidence adjustment
    confidence = "HIGH" if ithasala else "MEDIUM"
    if verdict == "Positive" and tatva_q == "Auspicious":
        confidence = "VERY HIGH"

    return {
        "question": question_type,
        "verdict": verdict,
        "lagna_lord": ll_name,
        "target_lord": target_lord_name,
        "moon_status": f"Moon in House {moon.house}",
        "ithasala": ithasala,
        "micro_timing": {"tatva": tatva, "hora": hora_lord},
        "confidence": confidence
    }
