from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor

def get_finance_prediction(chart: CanonicalChart) -> DomainPrediction:
    """Analyze finance using 2nd and 11th houses, their lords, and D2."""
    evidence = []
    factors = []
    score = 50.0

    planets = chart.planets
    asc_rashi = chart.asc_rashi

    # 1. Lords
    second_lord_name = chart.house_lords[2]
    eleventh_lord_name = chart.house_lords[11]

    second_lord = planets[second_lord_name]
    eleventh_lord = planets[eleventh_lord_name]

    # 2. Analyze 2nd lord (Accumulated Wealth)
    if "Exalted" in second_lord.dignity:
        msg = f"2nd lord ({second_lord_name}) is Exalted: Exceptional ability to accumulate wealth."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="2nd Lord Dignity", type="lord", direction="positive", weight=0.25, explanation=msg))
        score += 15
    elif second_lord.dignity == "Own Sign":
        msg = f"2nd lord ({second_lord_name}) is in its Own Sign: Financial stability and secure assets."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="2nd Lord Dignity", type="lord", direction="positive", weight=0.2, explanation=msg))
        score += 10
    elif "Debilitated" in second_lord.dignity:
        msg = f"2nd lord ({second_lord_name}) is Debilitated: Challenges in saving and financial instability."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="2nd Lord Dignity", type="lord", direction="negative", weight=0.25, explanation=msg))
        score -= 15

    # 3. Analyze 11th lord (Gains and Income)
    if "Exalted" in eleventh_lord.dignity:
        msg = f"11th lord ({eleventh_lord_name}) is Exalted: High income potential and multiple sources of gains."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="11th Lord Dignity", type="lord", direction="positive", weight=0.25, explanation=msg))
        score += 15
    elif eleventh_lord.dignity == "Own Sign":
        msg = f"11th lord ({eleventh_lord_name}) is in its Own Sign: Regular and reliable flow of income."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="11th Lord Dignity", type="lord", direction="positive", weight=0.2, explanation=msg))
        score += 10

    # 4. Jupiter (Dhanakaraka)
    jupiter = planets["Jupiter"]
    if "Exalted" in jupiter.dignity or jupiter.dignity == "Own Sign":
        msg = "Jupiter (Significator of Wealth) is strong: Divine blessings for prosperity."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Jupiter Strength", type="planet", direction="positive", weight=0.15, explanation=msg))
        score += 10

    # 5. Dhana Yoga
    if second_lord.house == 11 or eleventh_lord.house == 2:
        msg = "Strong association between 2nd and 11th houses (Dhana Yoga): Wealth creation through professional gains."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Dhana Yoga", type="yoga", direction="positive", weight=0.2, explanation=msg))
        score += 15

    score = max(0.0, min(100.0, score))

    return DomainPrediction(
        domain="Finance & Wealth",
        score=score,
        confidence="HIGH" if len(factors) >= 3 else "MEDIUM",
        summary=f"Financial status is largely determined by the strength of {second_lord_name} and {eleventh_lord_name}.",
        evidence=evidence,
        positive_factors=[f for f in factors if f.direction == "positive"],
        negative_factors=[f for f in factors if f.direction == "negative"],
        contradictions=[],
        timing=[],
        recommendations=["Invest in long-term assets if the 2nd lord is strong.", "Focus on expanding networking and income streams if the 11th lord is strong."]
    )
