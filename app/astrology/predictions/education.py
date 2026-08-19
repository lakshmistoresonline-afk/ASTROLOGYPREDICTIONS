from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor

def get_education_prediction(chart: CanonicalChart) -> DomainPrediction:
    evidence = []
    factors = []
    score = 50.0

    planets = chart.planets

    # 1. 2nd House (Early education)
    second_lord = planets[chart.house_lords[2]]
    if "Exalted" in second_lord.dignity:
        evidence.append(f"2nd Lord ({second_lord.name}) is Exalted: Strong foundation.")
        score += 10

    # 2. 4th House (Basic education/College)
    fourth_lord = planets[chart.house_lords[4]]
    if "Exalted" in fourth_lord.dignity:
        evidence.append(f"4th Lord ({fourth_lord.name}) is Exalted: Excellent academic potential.")
        score += 15
    elif "Debilitated" in fourth_lord.dignity:
        evidence.append(f"4th Lord ({fourth_lord.name}) is Debilitated: Challenges in basic studies.")
        score -= 15

    # 3. 5th House (Intelligence/Competitive exams)
    fifth_lord = planets[chart.house_lords[5]]
    if "Exalted" in fifth_lord.dignity:
        evidence.append(f"5th Lord ({fifth_lord.name}) is Exalted: High intelligence.")
        score += 15

    # 4. Mercury (Significator of Education)
    mercury = planets["Mercury"]
    if "Exalted" in mercury.dignity:
        evidence.append("Mercury (Karaka) is Exalted: Sharp learning ability.")
        score += 15

    # 5. D24 (Chaturvimshamsha) - Education Varga
    d24 = chart.divisional_charts.get("D24", {})
    if d24:
        d24_lagna = d24.get("Lagna", 0)
        # Check if 5th lord is strong in D24
        # (Simplified check)
        pass

    score = max(0.0, min(100.0, score))

    return DomainPrediction(
        domain="Education & Knowledge",
        score=score,
        confidence="MEDIUM",
        summary="Educational prospects are driven by the strength of the 2nd, 4th, and 5th houses.",
        evidence=evidence,
        positive_factors=[f for f in factors if f.direction == "positive"],
        negative_factors=[f for f in factors if f.direction == "negative"],
        contradictions=[],
        timing=[],
        recommendations=["Consistent study habits will maximize the natal potential."]
    )
