from typing import Dict, Any, List, Optional

EVENT_RULES = {
    "PROMOTION": {
        "domain": "CAREER",
        "primary_houses": [10, 1, 11],
        "supporting_houses": [6, 9],
        "karakas": ["Sun", "Jupiter"],
        "lord_focus": [10, 1],
        "required_min_score": 0.45
    },
    "JOB_CHANGE": {
        "domain": "CAREER",
        "primary_houses": [6, 10, 12],
        "supporting_houses": [3, 8],
        "karakas": ["Saturn", "Mars"],
        "lord_focus": [6, 12],
        "required_min_score": 0.40
    },
    "LEADERSHIP_APPOINTMENT": {
        "domain": "CAREER",
        "primary_houses": [1, 10],
        "supporting_houses": [5, 9, 11],
        "karakas": ["Sun", "Mars"],
        "lord_focus": [1, 10],
        "required_min_score": 0.55
    },
    "MARRIAGE": {
        "domain": "MARRIAGE",
        "primary_houses": [7, 2, 11],
        "supporting_houses": [5, 9],
        "karakas": ["Venus", "Jupiter"],
        "lord_focus": [7, 2],
        "required_min_score": 0.45
    },
    "SEPARATION_OR_DIVORCE": {
        "domain": "MARRIAGE",
        "primary_houses": [6, 8, 12],
        "supporting_houses": [7],
        "karakas": ["Saturn", "Mars", "Rahu"],
        "lord_focus": [6, 8, 12],
        "required_min_score": 0.40
    },
    "INCOME_EXPANSION": {
        "domain": "FINANCE",
        "primary_houses": [11, 2, 10],
        "supporting_houses": [5, 9],
        "karakas": ["Jupiter", "Mercury"],
        "lord_focus": [11, 2],
        "required_min_score": 0.45
    },
    "FINANCIAL_PRESSURE": {
        "domain": "FINANCE",
        "primary_houses": [6, 8, 12],
        "supporting_houses": [2],
        "karakas": ["Saturn", "Mars"],
        "lord_focus": [6, 8, 12],
        "required_min_score": 0.40
    },
    "PROPERTY_PURCHASE": {
        "domain": "PROPERTY",
        "primary_houses": [4, 2, 11],
        "supporting_houses": [9],
        "karakas": ["Mars", "Venus"],
        "lord_focus": [4, 2],
        "required_min_score": 0.45
    },
    "PROPERTY_SALE": {
        "domain": "PROPERTY",
        "primary_houses": [3, 10, 12],
        "supporting_houses": [4],
        "karakas": ["Mars", "Mercury"],
        "lord_focus": [3, 12],
        "required_min_score": 0.40
    },
    "ACADEMIC_ENROLLMENT": {
        "domain": "EDUCATION",
        "primary_houses": [4, 5, 9],
        "supporting_houses": [2],
        "karakas": ["Mercury", "Jupiter"],
        "lord_focus": [4, 5, 9],
        "required_min_score": 0.42
    },
    "CHILD_BIRTH": {
        "domain": "CHILDREN",
        "primary_houses": [5, 9, 11],
        "supporting_houses": [2],
        "karakas": ["Jupiter"],
        "lord_focus": [5, 9],
        "required_min_score": 0.45
    },
    "FOREIGN_SETTLEMENT": {
        "domain": "FOREIGN",
        "primary_houses": [9, 12, 3, 4],
        "supporting_houses": [7],
        "karakas": ["Rahu", "Moon"],
        "lord_focus": [9, 12],
        "required_min_score": 0.45
    },
    "HEALTH_VITALITY": {
        "domain": "HEALTH",
        "primary_houses": [1, 6],
        "supporting_houses": [8, 12],
        "karakas": ["Sun", "Mars"],
        "lord_focus": [1, 6],
        "required_min_score": 0.40
    },
    "SPIRITUAL_INITIATION": {
        "domain": "SPIRITUALITY",
        "primary_houses": [9, 12, 5],
        "supporting_houses": [8],
        "karakas": ["Jupiter", "Ketu"],
        "lord_focus": [9, 12],
        "required_min_score": 0.45
    }
}

def evaluate_natal_promise(chart_obj, domain: str, event_type: str = "GENERAL") -> Dict[str, Any]:
    """
    P0.3-R1 Event-Specific Natal Promise Engine.
    Evaluates whether the natal chart structurally promises a specific event type.
    NO future leakage, NO Dasha/transit dependencies, strict event-rule mapping.
    """
    ev_key = event_type.upper().replace(" ", "_")
    rule = EVENT_RULES.get(ev_key)

    if not rule and domain:
        dom_key = domain.upper()
        for k, r in EVENT_RULES.items():
            if r["domain"] == dom_key:
                rule = r
                break

    if not rule or not chart_obj or not hasattr(chart_obj, 'planets') or not chart_obj.planets:
        return {
            "domain": domain.upper(),
            "event_type": event_type,
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": ["No matching event-specific deterministic rule or chart data found."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "evidence_groups": [],
            "independence_count": 0,
            "engine_version": "V5.3-EVENT-SPECIFIC"
        }

    positive_evidence = []
    negative_evidence = []
    independence_groups = set()

    planets = chart_obj.planets
    house_lords = getattr(chart_obj, 'house_lords', {})

    score = 0.25 # Base structural weight

    for k in rule["karakas"]:
        if k in planets:
            pdata = planets[k]
            dignity = getattr(pdata, 'dignity', 'Neutral')
            house = getattr(pdata, 'house', 1)
            is_combust = getattr(pdata, 'is_combust', False)

            if dignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                score += 0.20
                positive_evidence.append(f"Event Karaka {k} is dignified ({dignity}) in House {house}.")
                independence_groups.add("SIGNIFICATOR_STRENGTH")
            elif dignity in ["Debilitated"]:
                score -= 0.15
                negative_evidence.append(f"Event Karaka {k} is debilitated in House {house}.")
                independence_groups.add("SIGNIFICATOR_STRENGTH")
            else:
                positive_evidence.append(f"Event Karaka {k} is moderately placed in House {house}.")

            if is_combust:
                score -= 0.10
                negative_evidence.append(f"Event Karaka {k} is combust by Sun.")
                independence_groups.add("PLANETARY_CONDITION")

    for h in rule["primary_houses"]:
        lord = house_lords.get(h)
        if lord and lord in planets:
            lp = planets[lord]
            ldignity = getattr(lp, 'dignity', 'Neutral')
            lhouse = getattr(lp, 'house', 1)

            if ldignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                score += 0.18
                positive_evidence.append(f"Primary House {h} lord ({lord}) is strong ({ldignity}) in House {lhouse}.")
                independence_groups.add("LORD_PLACEMENT")
            elif ldignity in ["Debilitated"]:
                score -= 0.15
                negative_evidence.append(f"Primary House {h} lord ({lord}) is debilitated in House {lhouse}.")
                independence_groups.add("LORD_PLACEMENT")

        occupants = [pname for pname, pinfo in planets.items() if getattr(pinfo, 'house', 0) == h]
        if occupants:
            positive_evidence.append(f"Primary House {h} is tenanted by: {', '.join(occupants)}.")
            independence_groups.add("HOUSE_STRUCTURE")

    final_score = max(0.0, min(1.0, score))
    min_req = rule.get("required_min_score", 0.40)

    if final_score < min_req:
        level = "WITHHELD"
    elif final_score >= 0.75 and len(negative_evidence) <= 1:
        level = "STRONG_PROMISE"
    elif final_score >= 0.60:
        level = "MODERATE_PROMISE"
    elif final_score >= 0.45:
        level = "CONDITIONAL_PROMISE"
    else:
        level = "WEAK_PROMISE"

    return {
        "domain": rule["domain"],
        "event_type": event_type.upper(),
        "promise_level": level,
        "promise_score": round(final_score, 2),
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "relevant_houses": rule["primary_houses"],
        "relevant_house_lords": [house_lords.get(h) for h in rule["primary_houses"] if h in house_lords],
        "relevant_planets": rule["karakas"],
        "evidence_groups": list(independence_groups),
        "independence_count": len(independence_groups),
        "engine_version": "V5.3-EVENT-SPECIFIC"
    }
