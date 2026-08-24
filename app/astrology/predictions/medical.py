from typing import Dict, Any, List
from ..core.models import CanonicalChart

# Rashi to Body Part mapping (Kala Purusha)
KALA_PURUSHA = {
    0: "Head and Brain", 1: "Face and Eyes", 2: "Neck and Throat",
    3: "Chest and Heart", 4: "Upper Abdomen and Stomach", 5: "Lower Abdomen and Intestines",
    6: "Kidneys and Pelvic region", 7: "Private parts and Excretory", 8: "Thighs and Hips",
    9: "Knees and Joints", 10: "Ankles and Calves", 11: "Feet and Toes"
}

def get_medical_astrology_insights(chart: CanonicalChart) -> List[str]:
    """Identify medical signatures based on afflicted houses and planets."""
    insights = []
    planets = chart.planets

    # 1. Check for malefics in the 6th, 8th, or 12th house
    for p_name in ["Saturn", "Mars", "Rahu", "Ketu"]:
        p = planets.get(p_name)
        if p and p.house in [6, 8, 12]:
             body_part = KALA_PURUSHA.get(p.rashi, "General health")
             insights.append(f"Vulnerability: {p_name} in H{p.house} affects {body_part}.")

    # 2. Check 6th lord position
    l6_name = chart.house_lords[6]
    l6 = planets[l6_name]
    insights.append(f"Disease Indicator: 6th Lord ({l6_name}) in H{l6.house} suggests potential chronic issues in {KALA_PURUSHA.get(l6.rashi, 'general area')}.")

    # 3. Sun (Immunity) and Moon (Psychological)
    if planets["Sun"].house in [6, 8, 12]:
        insights.append("Immunity: Sun in a difficult house may lower natural resistance.")
    if planets["Moon"].house in [6, 8, 12]:
        insights.append("Psychological: Moon in a difficult house may increase sensitivity to stress.")

    return insights
