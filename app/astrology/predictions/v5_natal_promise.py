from typing import Dict, Any, List

DOMAIN_HOUSE_MAP = {
    "CAREER": {"houses": [10, 6, 11, 1, 9], "karakas": ["Sun", "Saturn", "Jupiter"]},
    "FINANCE": {"houses": [2, 11, 5, 9], "karakas": ["Jupiter", "Venus"]},
    "MARRIAGE": {"houses": [7, 2, 11], "karakas": ["Venus", "Jupiter"]},
    "PROPERTY": {"houses": [4, 2, 11], "karakas": ["Mars", "Venus"]},
    "EDUCATION": {"houses": [4, 5, 9], "karakas": ["Mercury", "Jupiter"]},
    "CHILDREN": {"houses": [5, 9, 11], "karakas": ["Jupiter"]},
    "FOREIGN": {"houses": [9, 12, 3, 4], "karakas": ["Rahu", "Moon"]},
    "HEALTH": {"houses": [1, 6, 8], "karakas": ["Sun", "Mars"]},
    "SPIRITUALITY": {"houses": [9, 12, 5], "karakas": ["Jupiter", "Ketu"]},
    "BUSINESS": {"houses": [7, 10, 11, 2], "karakas": ["Mercury", "Saturn"]},
    "FAME": {"houses": [1, 5, 9, 10], "karakas": ["Sun", "Jupiter"]}
}

def evaluate_natal_promise(chart_obj, domain: str, event_type: str = "general") -> Dict[str, Any]:
    """
    V5.3/P0.3 Event-Specific Natal Promise Engine: Answers 'Does the natal chart contain
    a meaningful structural promise for THIS SPECIFIC EVENT?' using strict deterministic chart facts.
    Returns structured analysis with promise_level, score, positive/negative evidence, and provenance.
    """
    if not chart_obj or not hasattr(chart_obj, 'planets') or not chart_obj.planets:
        return {
            "domain": domain,
            "event_type": event_type,
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": ["Missing or unverified chart planetary data."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "engine_version": "V5.3-EVENT-SPECIFIC"
        }

    dom_spec = DOMAIN_HOUSE_MAP.get(domain.upper(), {"houses": [1, 10], "karakas": ["Sun"]})
    target_houses = dom_spec["houses"]
    target_karakas = dom_spec["karakas"]

    positive_evidence = []
    negative_evidence = []
    independence_groups = set()

    # 1. Inspect house occupants and lords
    planets = chart_obj.planets
    house_lords = getattr(chart_obj, 'house_lords', {})
    asc_rashi = getattr(chart_obj, 'asc_rashi', 0)

    score = 0.4 # Baseline structural potential

    # Evaluate Karakas
    for k in target_karakas:
        if k in planets:
            pdata = planets[k]
            dignity = getattr(pdata, 'dignity', 'Neutral')
            house = getattr(pdata, 'house', 1)
            is_combust = getattr(pdata, 'is_combust', False)
            is_retro = getattr(pdata, 'is_retrograde', False)

            if dignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                score += 0.15
                positive_evidence.append(f"Karaka {k} is strongly dignified ({dignity}) in House {house}.")
                independence_groups.add("SIGNIFICATOR_STRENGTH")
            elif dignity in ["Debilitated"]:
                score -= 0.15
                negative_evidence.append(f"Karaka {k} is debilitated in House {house}.")
                independence_groups.add("SIGNIFICATOR_STRENGTH")
            else:
                positive_evidence.append(f"Karaka {k} is neutral in House {house}.")

            if is_combust:
                score -= 0.10
                negative_evidence.append(f"Karaka {k} is combust by Sun.")
                independence_groups.add("PLANETARY_CONDITION")

    # Evaluate Relevant Houses & House Lords
    for h in target_houses:
        lord = house_lords.get(h)
        if lord and lord in planets:
            lp = planets[lord]
            ldignity = getattr(lp, 'dignity', 'Neutral')
            lhouse = getattr(lp, 'house', 1)

            if ldignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                score += 0.12
                positive_evidence.append(f"House {h} lord ({lord}) is dignified ({ldignity}) in House {lhouse}.")
                independence_groups.add("LORD_PLACEMENT")
            elif ldignity in ["Debilitated"]:
                score -= 0.12
                negative_evidence.append(f"House {h} lord ({lord}) is debilitated in House {lhouse}.")
                independence_groups.add("LORD_PLACEMENT")

        # Check occupants in target house
        occupants = [pname for pname, pinfo in planets.items() if getattr(pinfo, 'house', 0) == h]
        if occupants:
            positive_evidence.append(f"House {h} is tenanted by active planets: {', '.join(occupants)}.")
            independence_groups.add("HOUSE_STRUCTURE")

    # Clamp score between 0.0 and 1.0
    final_score = max(0.0, min(1.0, score))

    if final_score >= 0.75 and len(negative_evidence) <= 1:
        level = "STRONG_PROMISE"
    elif final_score >= 0.60:
        level = "MODERATE_PROMISE"
    elif final_score >= 0.45:
        level = "CONDITIONAL_PROMISE"
    elif final_score >= 0.30:
        level = "WEAK_PROMISE"
    else:
        level = "WITHHELD"

    return {
        "domain": domain.upper(),
        "event_type": event_type,
        "promise_level": level,
        "promise_score": round(final_score, 2),
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "relevant_houses": target_houses,
        "relevant_house_lords": [house_lords.get(h) for h in target_houses if h in house_lords],
        "relevant_planets": target_karakas,
        "evidence_groups": list(independence_groups),
        "independence_count": len(independence_groups),
        "engine_version": "V5.3-EVENT-SPECIFIC"
    }
