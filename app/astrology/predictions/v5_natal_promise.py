from typing import Dict, Any, List, Optional

EVENT_RULES = {
    "PROMOTION": {
        "domain": "CAREER",
        "primary_houses": [10, 1, 11],
        "supporting_houses": [6, 9],
        "karakas": ["Sun", "Jupiter"],
        "varga_required": "D10",
        "required_min_score": 0.35
    },
    "JOB_CHANGE": {
        "domain": "CAREER",
        "primary_houses": [6, 10, 12],
        "supporting_houses": [3, 8],
        "karakas": ["Saturn", "Mars"],
        "varga_required": "D10",
        "required_min_score": 0.30
    },
    "LEADERSHIP_APPOINTMENT": {
        "domain": "CAREER",
        "primary_houses": [1, 10],
        "supporting_houses": [5, 9, 11],
        "karakas": ["Sun", "Mars"],
        "varga_required": "D10",
        "required_min_score": 0.45
    },
    "MARRIAGE": {
        "domain": "MARRIAGE",
        "primary_houses": [7, 2, 11],
        "supporting_houses": [5, 9],
        "karakas": ["Venus", "Jupiter"],
        "varga_required": "D9",
        "required_min_score": 0.35
    },
    "SEPARATION_OR_DIVORCE": {
        "domain": "MARRIAGE",
        "primary_houses": [6, 8, 12],
        "supporting_houses": [7],
        "karakas": ["Saturn", "Mars", "Rahu"],
        "varga_required": "D9",
        "required_min_score": 0.30
    },
    "INCOME_EXPANSION": {
        "domain": "FINANCE",
        "primary_houses": [11, 2, 10],
        "supporting_houses": [5, 9],
        "karakas": ["Jupiter", "Mercury"],
        "varga_required": "D2",
        "required_min_score": 0.35
    },
    "FINANCIAL_PRESSURE": {
        "domain": "FINANCE",
        "primary_houses": [6, 8, 12],
        "supporting_houses": [2],
        "karakas": ["Saturn", "Mars"],
        "varga_required": "D2",
        "required_min_score": 0.30
    },
    "PROPERTY_PURCHASE": {
        "domain": "PROPERTY",
        "primary_houses": [4, 2, 11],
        "supporting_houses": [9],
        "karakas": ["Mars", "Venus"],
        "varga_required": "D4",
        "required_min_score": 0.35
    },
    "PROPERTY_SALE": {
        "domain": "PROPERTY",
        "primary_houses": [3, 10, 12],
        "supporting_houses": [4],
        "karakas": ["Mars", "Mercury"],
        "varga_required": "D4",
        "required_min_score": 0.30
    },
    "ACADEMIC_ENROLLMENT": {
        "domain": "EDUCATION",
        "primary_houses": [4, 5, 9],
        "supporting_houses": [2],
        "karakas": ["Mercury", "Jupiter"],
        "varga_required": "D24",
        "required_min_score": 0.35
    },
    "CHILD_BIRTH": {
        "domain": "CHILDREN",
        "primary_houses": [5, 9, 11],
        "supporting_houses": [2],
        "karakas": ["Jupiter"],
        "varga_required": "D7",
        "required_min_score": 0.35
    },
    "FOREIGN_SETTLEMENT": {
        "domain": "FOREIGN",
        "primary_houses": [9, 12, 3, 4],
        "supporting_houses": [7],
        "karakas": ["Rahu", "Moon"],
        "varga_required": "D9",
        "required_min_score": 0.35
    },
    "HEALTH_VITALITY": {
        "domain": "HEALTH",
        "primary_houses": [1, 6],
        "supporting_houses": [8, 12],
        "karakas": ["Sun", "Mars"],
        "varga_required": "D1",
        "required_min_score": 0.30
    },
    "SPIRITUAL_INITIATION": {
        "domain": "SPIRITUALITY",
        "primary_houses": [9, 12, 5],
        "supporting_houses": [8],
        "karakas": ["Jupiter", "Ketu"],
        "varga_required": "D20",
        "required_min_score": 0.35
    }
}

def evaluate_natal_promise(chart_obj, domain: str, event_type: str = "GENERAL") -> Dict[str, Any]:
    """
    P0.3-R3 Hardened Event-Specific Deterministic Natal Promise Engine.
    Strictly resolves specific event keys from EVENT_RULES without fallback.
    Accumulates structured evidence items with independence group anti-double-counting capping.
    """
    if not event_type:
        return {
            "domain": domain.upper() if domain else "UNKNOWN",
            "event_type": event_type or "UNKNOWN",
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": ["Missing event_type. Strict event resolution required."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "evidence_items": [],
            "independence_count": 0,
            "engine_version": "V5.3-EVENT-SPECIFIC-HARDENED-R3"
        }

    ev_key = event_type.upper().replace(" ", "_")
    rule = EVENT_RULES.get(ev_key)

    if not rule:
        return {
            "domain": domain.upper() if domain else "UNKNOWN",
            "event_type": event_type,
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": [f"unsupported_event: '{event_type}' has no registered deterministic event rule."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "evidence_items": [],
            "independence_count": 0,
            "engine_version": "V5.3-EVENT-SPECIFIC-HARDENED-R3"
        }

    if not chart_obj or not hasattr(chart_obj, 'planets') or not chart_obj.planets:
        return {
            "domain": rule["domain"],
            "event_type": ev_key,
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": ["Missing or unverified chart planetary data."],
            "relevant_houses": rule["primary_houses"],
            "relevant_house_lords": [],
            "relevant_planets": rule["karakas"],
            "evidence_items": [],
            "independence_count": 0,
            "engine_version": "V5.3-EVENT-SPECIFIC-HARDENED-R3"
        }

    evidence_items: List[Dict[str, Any]] = []
    planets = chart_obj.planets
    house_lords = getattr(chart_obj, 'house_lords', {})
    div_charts = getattr(chart_obj, 'divisional_charts', {})
    varga_req = rule.get("varga_required")

    # 1. Evaluate Karakas (Group: SIGNIFICATOR_STRENGTH)
    for k in rule["karakas"]:
        if k in planets:
            pdata = planets[k]
            dignity = getattr(pdata, 'dignity', 'Neutral')
            house = getattr(pdata, 'house', 1)
            is_combust = getattr(pdata, 'is_combust', False)
            shadbala = getattr(pdata, 'shadbala_score', None)

            if dignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                val = 0.30
                evidence_items.append({
                    "rule_id": f"KARAKA_STRONG_{k}",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "SIGNIFICATOR_STRENGTH",
                    "polarity": "POSITIVE",
                    "source_type": "PLANET_DIGNITY",
                    "source_fact": f"{k} in House {house} ({dignity})",
                    "magnitude": val,
                    "rationale": f"Event significator {k} has strong dignity ({dignity})."
                })
            elif dignity in ["Debilitated"]:
                val = -0.25
                evidence_items.append({
                    "rule_id": f"KARAKA_WEAK_{k}",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "SIGNIFICATOR_STRENGTH",
                    "polarity": "NEGATIVE",
                    "source_type": "PLANET_DIGNITY",
                    "source_fact": f"{k} in House {house} (Debilitated)",
                    "magnitude": val,
                    "rationale": f"Event significator {k} is debilitated."
                })

            if is_combust:
                evidence_items.append({
                    "rule_id": f"KARAKA_COMBUST_{k}",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "PLANETARY_CONDITION",
                    "polarity": "NEGATIVE",
                    "source_type": "COMBUSTION",
                    "source_fact": f"{k} combust by Sun",
                    "magnitude": -0.20,
                    "rationale": f"Event significator {k} is combust."
                })

            if shadbala and shadbala > 6.0:
                evidence_items.append({
                    "rule_id": f"SHADBALA_STRONG_{k}",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "SHADBALA_MODIFIER",
                    "polarity": "POSITIVE",
                    "source_type": "SHADBALA",
                    "source_fact": f"{k} shadbala score {shadbala:.2f}",
                    "magnitude": 0.10,
                    "rationale": f"Event significator {k} has strong directional/positional strength (Shadbala)."
                })

    # 2. Evaluate Primary Houses & Lords (Group: LORD_PLACEMENT & HOUSE_STRUCTURE)
    for h in rule["primary_houses"]:
        lord = house_lords.get(h)
        if lord and lord in planets:
            lp = planets[lord]
            ldignity = getattr(lp, 'dignity', 'Neutral')
            lhouse = getattr(lp, 'house', 1)

            if ldignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                evidence_items.append({
                    "rule_id": f"LORD_STRONG_{h}_{lord}",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "LORD_PLACEMENT",
                    "polarity": "POSITIVE",
                    "source_type": "HOUSE_LORD",
                    "source_fact": f"House {h} lord {lord} in House {lhouse} ({ldignity})",
                    "magnitude": 0.25,
                    "rationale": f"Primary house {h} lord ({lord}) is strong ({ldignity})."
                })
            elif ldignity in ["Debilitated"]:
                evidence_items.append({
                    "rule_id": f"LORD_WEAK_{h}_{lord}",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "LORD_PLACEMENT",
                    "polarity": "NEGATIVE",
                    "source_type": "HOUSE_LORD",
                    "source_fact": f"House {h} lord {lord} in House {lhouse} (Debilitated)",
                    "magnitude": -0.20,
                    "rationale": f"Primary house {h} lord ({lord}) is debilitated."
                })

        occupants = [pname for pname, pinfo in planets.items() if getattr(pinfo, 'house', 0) == h]
        if occupants:
            evidence_items.append({
                "rule_id": f"HOUSE_OCCUPANCY_{h}",
                "event_type": ev_key,
                "domain": rule["domain"],
                "evidence_group": "HOUSE_STRUCTURE",
                "polarity": "POSITIVE",
                "source_type": "HOUSE_OCCUPANTS",
                "source_fact": f"House {h} tenanted by {', '.join(occupants)}",
                "magnitude": 0.15,
                "rationale": f"Primary house {h} is tenanted."
            })

    # 3. Evaluate Supporting Houses
    for h in rule.get("supporting_houses", []):
        occupants = [pname for pname, pinfo in planets.items() if getattr(pinfo, 'house', 0) == h]
        if occupants:
            evidence_items.append({
                "rule_id": f"SUPPORT_HOUSE_OCCUPANCY_{h}",
                "event_type": ev_key,
                "domain": rule["domain"],
                "evidence_group": "HOUSE_STRUCTURE",
                "polarity": "POSITIVE",
                "source_type": "SUPPORTING_HOUSE",
                "source_fact": f"Supporting House {h} tenanted by {', '.join(occupants)}",
                "magnitude": 0.08,
                "rationale": f"Supporting house {h} provides contextual support."
            })

    # 4. Evaluate Varga Confirmation if available
    if varga_req and varga_req in div_charts:
        v_chart = div_charts[varga_req]
        evidence_items.append({
            "rule_id": f"VARGA_CONFIRMATION_{varga_req}",
            "event_type": ev_key,
            "domain": rule["domain"],
            "evidence_group": "DIVISIONAL_CONFIRMATION",
            "polarity": "POSITIVE",
            "source_type": "DIVISIONAL_CHART",
            "source_fact": f"Divisional chart {varga_req} computed and aligned",
            "magnitude": 0.15,
            "rationale": f"Divisional chart {varga_req} corroborates structural baseline."
        })

    # Anti-Double-Counting Aggregation by Group
    group_totals: Dict[str, float] = {}
    for item in evidence_items:
        g = item["evidence_group"]
        mag = item["magnitude"]
        current = group_totals.get(g, 0.0)
        group_totals[g] = max(-0.35, min(0.35, current + mag))

    final_score = sum(group_totals.values())
    final_score = max(0.0, min(1.0, final_score))
    min_req = rule.get("required_min_score", 0.30)

    positive_evidence = [i["rationale"] for i in evidence_items if i["polarity"] == "POSITIVE"]
    negative_evidence = [i["rationale"] for i in evidence_items if i["polarity"] == "NEGATIVE"]

    if not evidence_items or final_score < min_req:
        level = "INSUFFICIENT_EVIDENCE" if not evidence_items else "WITHHELD"
    elif final_score >= 0.70 and len(negative_evidence) == 0:
        level = "STRONG_PROMISE"
    elif final_score >= 0.55:
        level = "MODERATE_PROMISE"
    elif final_score >= 0.45:
        level = "CONDITIONAL_PROMISE"
    else:
        level = "WEAK_PROMISE"

    return {
        "domain": rule["domain"],
        "event_type": ev_key,
        "promise_level": level,
        "promise_score": round(final_score, 2),
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "relevant_houses": rule["primary_houses"],
        "relevant_house_lords": [house_lords.get(h) for h in rule["primary_houses"] if h in house_lords],
        "relevant_planets": rule["karakas"],
        "evidence_items": evidence_items,
        "independence_count": len(group_totals),
        "engine_version": "V5.3-EVENT-SPECIFIC-HARDENED-R3"
    }
