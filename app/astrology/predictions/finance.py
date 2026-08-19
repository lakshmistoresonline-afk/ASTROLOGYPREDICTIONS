from typing import Dict, Any, List
from ..strength.functional import RASHI_LORDS

def get_finance_prediction(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze finance using 2nd and 11th houses, their lords, and D2."""
    evidence = []
    score = 50.0

    planets = chart["planets"]
    asc_rashi = chart["asc_rashi"]

    # Houses
    second_house_rashi = (asc_rashi + 1) % 12
    eleventh_house_rashi = (asc_rashi + 10) % 12

    # Lords
    second_lord_name = RASHI_LORDS[second_house_rashi]
    eleventh_lord_name = RASHI_LORDS[eleventh_house_rashi]

    second_lord = planets[second_lord_name]
    eleventh_lord = planets[eleventh_lord_name]

    # 1. Analyze 2nd lord (Wealth)
    if "Exalted" in second_lord["dignity"]:
        evidence.append(f"✓ 2nd lord ({second_lord_name}) is Exalted (+15)")
        score += 15
    elif second_lord["dignity"] == "Own Sign":
        evidence.append(f"✓ 2nd lord ({second_lord_name}) is in its Own Sign (+10)")
        score += 10
    elif "Debilitated" in second_lord["dignity"]:
        evidence.append(f"⚠ 2nd lord ({second_lord_name}) is Debilitated (-15)")
        score -= 15

    # 2. Analyze 11th lord (Gains)
    if "Exalted" in eleventh_lord["dignity"]:
        evidence.append(f"✓ 11th lord ({eleventh_lord_name}) is Exalted (+15)")
        score += 15
    elif eleventh_lord["dignity"] == "Own Sign":
        evidence.append(f"✓ 11th lord ({eleventh_lord_name}) is in its Own Sign (+10)")
        score += 10

    # 3. Jupiter (Dhanakaraka)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter["dignity"] or jupiter["dignity"] == "Own Sign":
        evidence.append(f"✓ Jupiter (Significator of Wealth) is strong (+10)")
        score += 10

    # 4. Dhana Yoga (Partial check: 2nd/11th/9th/5th lords association)
    # Association of 2nd lord and 11th lord
    if second_lord["house"] == 11 or eleventh_lord["house"] == 2:
        evidence.append(f"✓ Strong association between 2nd and 11th houses (+15)")
        score += 15

    score = max(0.0, min(100.0, score))

    return {
        "domain": "Finance",
        "score": score,
        "evidence": evidence,
        "confidence": "HIGH" if len(evidence) >= 3 else "MEDIUM"
    }
