from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor

def get_marriage_prediction(chart: CanonicalChart) -> DomainPrediction:
    """Analyze marriage/relationships using 7th house, its lord, and Venus/Jupiter."""
    evidence = []
    factors = []
    score = 50.0

    planets = chart.planets
    asc_rashi = chart.asc_rashi

    # 1. 7th house from Ascendant
    seventh_house_rashi = (asc_rashi + 6) % 12
    seventh_lord_name = chart.house_lords[7]
    seventh_lord = planets[seventh_lord_name]

    # Analyze 7th lord
    if "Exalted" in seventh_lord.dignity:
        msg = f"7th lord ({seventh_lord_name}) is Exalted: Harmonious and beneficial relationships."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="7th Lord Dignity", type="lord", direction="positive", weight=0.3, explanation=msg))
        score += 20
    elif seventh_lord.dignity == "Own Sign":
        msg = f"7th lord ({seventh_lord_name}) is in its Own Sign: Stable and lasting partnership."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="7th Lord Dignity", type="lord", direction="positive", weight=0.25, explanation=msg))
        score += 15
    elif "Debilitated" in seventh_lord.dignity:
        msg = f"7th lord ({seventh_lord_name}) is Debilitated: Challenges and friction in partnerships."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="7th Lord Dignity", type="lord", direction="negative", weight=0.3, explanation=msg))
        score -= 20

    # 2. Significators (Venus for men, Jupiter for women - simplified both)
    venus = planets["Venus"]
    if "Exalted" in venus.dignity or venus.dignity == "Own Sign":
        msg = "Venus (Significator of Love) is strong: Natural charm and happiness in love."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Venus Strength", type="planet", direction="positive", weight=0.2, explanation=msg))
        score += 15
    elif "Debilitated" in venus.dignity:
        msg = "Venus (Significator of Love) is weak: Emotional sensitivity and relationship hurdles."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="Venus Strength", type="planet", direction="negative", weight=0.2, explanation=msg))
        score -= 15

    # 3. 7th house occupants
    occupants = [p for p, data in planets.items() if data.house == 7]
    for p in occupants:
        p_data = planets[p]
        if p_data.functional_status == "Functional Benefic":
            msg = f"Benefic planet {p} in 7th house: Pleasant and supportive interactions."
            evidence.append("✓ " + msg)
            factors.append(PredictionFactor(factor="7th House Occupant", type="planet", direction="positive", weight=0.15, explanation=msg))
            score += 10
        elif p_data.functional_status == "Functional Malefic":
            msg = f"Malefic planet {p} in 7th house: Tension and disagreements in relationships."
            evidence.append("⚠ " + msg)
            factors.append(PredictionFactor(factor="7th House Occupant", type="planet", direction="negative", weight=0.15, explanation=msg))
            score -= 10

    # 4. Navamsa (D9) check
    d9 = chart.divisional_charts.get("D9", {})
    if d9:
        d9_lagna = d9.get("Lagna", 0)
        d9_seventh_rashi = (d9_lagna + 6) % 12
        if d9.get(seventh_lord_name) == d9_seventh_rashi:
            msg = "7th lord is in the 7th house of D9: Strong confirmation of relationship stability."
            evidence.append("✓ " + msg)
            factors.append(PredictionFactor(factor="D9 Confirmation", type="varga", direction="positive", weight=0.2, explanation=msg))
            score += 15

    score = max(0.0, min(100.0, score))

    return DomainPrediction(
        domain="Marriage & Relationships",
        score=score,
        confidence="HIGH" if len(factors) >= 3 else "MEDIUM",
        summary=f"The quality of relationships is significantly influenced by {seventh_lord_name} and Venus.",
        evidence=evidence,
        positive_factors=[f for f in factors if f.direction == "positive"],
        negative_factors=[f for f in factors if f.direction == "negative"],
        contradictions=[],
        timing=[],
        recommendations=["Focus on communication and mutual respect.", "Avoid making impulsive decisions during retrograde periods of Venus."]
    )
