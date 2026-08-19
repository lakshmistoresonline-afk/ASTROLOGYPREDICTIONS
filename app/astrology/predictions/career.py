from typing import Dict, Any

def get_career_prediction(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze career using 10th house, its lord, and D10."""
    evidence = []
    score = 50.0

    planets = chart["planets"]
    asc_rashi = chart["asc_rashi"]

    # 10th house from Ascendant
    tenth_house_rashi = (asc_rashi + 9) % 12

    # Find 10th lord
    from ..strength.functional import RASHI_LORDS
    tenth_lord_name = RASHI_LORDS[tenth_house_rashi]
    tenth_lord = planets[tenth_lord_name]

    # Analyze 10th lord dignity
    if "Exalted" in tenth_lord["dignity"]:
        evidence.append(f"✓ 10th lord ({tenth_lord_name}) is Exalted (+20)")
        score += 20
    elif tenth_lord["dignity"] == "Own Sign":
        evidence.append(f"✓ 10th lord ({tenth_lord_name}) is in its Own Sign (+15)")
        score += 15
    elif "Debilitated" in tenth_lord["dignity"]:
        evidence.append(f"⚠ 10th lord ({tenth_lord_name}) is Debilitated (-20)")
        score -= 20

    # Analyze 10th house occupants
    tenth_house_num = 10
    occupants = [p for p, data in planets.items() if data["house"] == tenth_house_num]

    for p in occupants:
        p_data = planets[p]
        if p_data["functional_status"] == "Functional Benefic":
            evidence.append(f"✓ Benefic planet {p} in 10th house (+10)")
            score += 10
        elif p_data["functional_status"] == "Functional Malefic":
            evidence.append(f"⚠ Malefic planet {p} in 10th house (-10)")
            score -= 10

    # D10 Confirmation (Simplified)
    d10 = chart["divisional"]["D10"]
    d10_lagna = d10["Lagna"]
    d10_tenth_rashi = (d10_lagna + 9) % 12
    if d10[tenth_lord_name] == d10_tenth_rashi:
        evidence.append("✓ 10th lord confirmed in 10th house in D10 (+10)")
        score += 10

    score = max(0.0, min(100.0, score))

    return {
        "domain": "Career",
        "score": score,
        "evidence": evidence,
        "confidence": "HIGH" if len(evidence) >= 3 else "MEDIUM"
    }
