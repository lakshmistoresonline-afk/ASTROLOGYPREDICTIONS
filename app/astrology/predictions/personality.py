from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction, PredictionFactor
from .scoring import calculate_weighted_score, get_label_from_score

def get_personality_prediction(chart: CanonicalChart) -> DomainPrediction:
    evidence = []
    factors = []

    planets = chart.planets
    asc_rashi = chart.asc_rashi
    asc_nak = chart.asc_nakshatra

    # 1. Lagna Rashi influence
    rashi_themes = {
        0: "Energetic, assertive, and pioneering (Aries).",
        1: "Stable, patient, and artistic (Taurus).",
        2: "Communicative, versatile, and intellectual (Gemini).",
        3: "Emotional, protective, and nurturing (Cancer).",
        4: "Confident, leadership-oriented, and creative (Leo).",
        5: "Analytical, practical, and detail-oriented (Virgo).",
        6: "Balanced, social, and harmonious (Libra).",
        7: "Intense, mystical, and transformative (Scorpio).",
        8: "Optimistic, philosophical, and adventurous (Sagittarius).",
        9: "Disciplined, ambitious, and pragmatic (Capricorn).",
        10: "Humanitarian, innovative, and intellectual (Aquarius).",
        11: "Spiritual, imaginative, and compassionate (Pisces)."
    }

    themes = rashi_themes.get(asc_rashi, "Complex temperament.")
    evidence.append(f"Lagna in {chart.asc_nakshatra.name}: {themes}")
    factors.append(PredictionFactor(
        factor="Lagna Rashi",
        type="house",
        direction="neutral",
        weight=0.3,
        explanation=themes
    ))

    # 2. Lagna Lord dignity
    asc_lord_name = chart.house_lords[1]
    asc_lord = planets[asc_lord_name]
    if "Exalted" in asc_lord.dignity:
        msg = f"Ascendant Lord ({asc_lord_name}) is Exalted, giving strong self-confidence."
        evidence.append("✓ " + msg)
        factors.append(PredictionFactor(factor="Lagna Lord Dignity", type="lord", direction="positive", weight=0.2, explanation=msg))
    elif "Debilitated" in asc_lord.dignity:
        msg = f"Ascendant Lord ({asc_lord_name}) is Debilitated, indicating self-doubt or health sensitivity."
        evidence.append("⚠ " + msg)
        factors.append(PredictionFactor(factor="Lagna Lord Dignity", type="lord", direction="negative", weight=0.2, explanation=msg))

    # 3. Moon (Mind) and Sun (Soul)
    moon = planets["Moon"]
    sun = planets["Sun"]

    evidence.append(f"Moon in {moon.nakshatra.name} indicates a {moon.nakshatra.lord}-ruled mental style.")
    evidence.append(f"Sun in {sun.nakshatra.name} indicates {sun.nakshatra.lord}-ruled core vitality.")

    # Calculate a dummy score for now based on lord dignity
    raw_score = 50.0
    if "Exalted" in asc_lord.dignity: raw_score += 20
    if "Own Sign" in asc_lord.dignity: raw_score += 15
    if "Debilitated" in asc_lord.dignity: raw_score -= 20

    score = max(0.0, min(100.0, raw_score))

    return DomainPrediction(
        domain="Personality & Temperament",
        score=score,
        confidence="MEDIUM",
        summary=f"Primary personality is shaped by {rashi_themes[asc_rashi]} and the influence of {asc_lord_name}.",
        positive_factors=[f for f in factors if f.direction == "positive"],
        negative_factors=[f for f in factors if f.direction == "negative"],
        contradictions=[],
        timing=[],
        recommendations=["Practice mindfulness to balance the core temperament."]
    )
