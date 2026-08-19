from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor

def get_career_prediction(chart: CanonicalChart) -> DomainPrediction:
    """Analyze career using 10th house, its lord, and D10."""
    evidence = []
    factors = []
    score = 50.0

    planets = chart.planets
    asc_rashi = chart.asc_rashi

    # 1. 10th house from Ascendant
    tenth_house_rashi = (asc_rashi + 9) % 12
    tenth_lord_name = chart.house_lords[10]
    tenth_lord = planets[tenth_lord_name]

    # Analyze 10th lord dignity
    if "Exalted" in tenth_lord.dignity:
        msg = f"10th lord ({tenth_lord_name}) is Exalted: High career status and authority."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="10th Lord Dignity", type="lord", direction="positive", weight=0.3, explanation=msg))
        score += 20
    elif tenth_lord.dignity == "Own Sign":
        msg = f"10th lord ({tenth_lord_name}) is in its Own Sign: Stable and successful professional life."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="10th Lord Dignity", type="lord", direction="positive", weight=0.25, explanation=msg))
        score += 15
    elif "Debilitated" in tenth_lord.dignity:
        msg = f"10th lord ({tenth_lord_name}) is Debilitated: Challenges and struggles in professional growth."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="10th Lord Dignity", type="lord", direction="negative", weight=0.3, explanation=msg))
        score -= 20

    # 2. 10th house occupants
    occupants = [p for p, data in planets.items() if data.house == 10]
    for p in occupants:
        p_data = planets[p]
        if p_data.functional_status == "Functional Benefic":
            msg = f"Benefic planet {p} in 10th house: Harmonious environment and support at work."
            evidence.append("✓ " + msg)
            factors.append(PredictionFactor(factor="10th House Occupant", type="planet", direction="positive", weight=0.15, explanation=msg))
            score += 10
        elif p_data.functional_status == "Functional Malefic":
            msg = f"Malefic planet {p} in 10th house: Obstacles and competition in career."
            evidence.append("⚠ " + msg)
            factors.append(PredictionFactor(factor="10th House Occupant", type="planet", direction="negative", weight=0.15, explanation=msg))
            score -= 10

    # 3. D10 Confirmation
    d10 = chart.divisional_charts.get("D10", {})
    if d10:
        d10_lagna = d10.get("Lagna", 0)
        d10_tenth_rashi = (d10_lagna + 9) % 12
        if d10.get(tenth_lord_name) == d10_tenth_rashi:
            msg = "10th lord is in the 10th house of D10: Strong confirmation of career success."
            evidence.append("✓ " + msg)
            factors.append(PredictionFactor(factor="D10 Confirmation", type="varga", direction="positive", weight=0.2, explanation=msg))
            score += 10

    score = max(0.0, min(100.0, score))

    return DomainPrediction(
        domain="Career & Professional Life",
        score=score,
        confidence="HIGH" if len(factors) >= 3 else "MEDIUM",
        summary=f"Career path is primarily driven by the {tenth_lord.dignity} status of {tenth_lord_name}.",
        evidence=evidence,
        positive_factors=[f for f in factors if f.direction == "positive"],
        negative_factors=[f for f in factors if f.direction == "negative"],
        contradictions=[],
        timing=[],
        recommendations=["Focus on leadership roles if the 10th lord is strong.", "Maintain patience during challenging transits if the 10th lord is weak."]
    )
