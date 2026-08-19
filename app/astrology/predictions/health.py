from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor

def get_health_prediction(chart: CanonicalChart) -> DomainPrediction:
    """Analyze health using 1st house (Ascendant), its lord, and Dusthana houses."""
    evidence = []
    factors = []
    score = 60.0

    planets = chart.planets
    asc_rashi = chart.asc_rashi

    # 1. Ascendant Lord (Vitality)
    asc_lord_name = chart.house_lords[1]
    asc_lord = planets[asc_lord_name]

    if "Exalted" in asc_lord.dignity or asc_lord.dignity == "Own Sign":
        msg = f"Ascendant lord ({asc_lord_name}) is strong: Robust physical constitution and high immunity."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Ascendant Lord Strength", type="lord", direction="positive", weight=0.3, explanation=msg))
        score += 15
    elif "Debilitated" in asc_lord.dignity:
        msg = f"Ascendant lord ({asc_lord_name}) is Debilitated: Sensitivity to health issues and low vitality."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="Ascendant Lord Strength", type="lord", direction="negative", weight=0.3, explanation=msg))
        score -= 20

    # 2. Sun (Vitality) and Moon (Mental Health)
    sun = planets["Sun"]
    if "Exalted" in sun.dignity or sun.dignity == "Own Sign":
        msg = "Sun (Natural Vitality) is strong: Strong life force and energy levels."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Sun Strength", type="planet", direction="positive", weight=0.2, explanation=msg))
        score += 10
    elif "Debilitated" in sun.dignity:
        msg = "Sun (Natural Vitality) is weak: Tendency towards fatigue and low energy."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="Sun Strength", type="planet", direction="negative", weight=0.2, explanation=msg))
        score -= 10

    # 3. Dusthana check (6, 8, 12)
    dusthana_count = sum(1 for p, d in planets.items() if d.house in [6, 8, 12])
    if dusthana_count >= 4:
        msg = f"Multiple planets ({dusthana_count}) in Dusthana houses: Potential for recurring health challenges."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="Dusthana Influence", type="house", direction="negative", weight=0.25, explanation=msg))
        score -= 15

    # 4. Benefics in Kendra
    kendra_benefics = sum(1 for p, d in planets.items() if d.house in [1, 4, 7, 10] and p in ["Jupiter", "Venus"])
    if kendra_benefics >= 1:
        msg = "Protective benefic planets in Kendra houses: Strong natural protection against diseases."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Kendra Protection", type="house", direction="positive", weight=0.2, explanation=msg))
        score += 10

    score = max(0.0, min(100.0, score))

    return DomainPrediction(
        domain="Health & Vitality",
        score=score,
        confidence="HIGH" if len(factors) >= 3 else "MEDIUM",
        summary=f"Overall health depends on the strength of {asc_lord_name} and the Sun.",
        evidence=evidence,
        positive_factors=[f for f in factors if f.direction == "positive"],
        negative_factors=[f for f in factors if f.direction == "negative"],
        contradictions=[],
        timing=[],
        recommendations=["Maintain a disciplined lifestyle and diet.", "This is an astrological interpretation, not medical advice."]
    )
