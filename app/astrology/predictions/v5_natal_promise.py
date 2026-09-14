from typing import Dict, Any, List, Optional
from .evidence import EvidenceNode, EvidenceEdge, EvidenceGraph, calculate_score_from_evidence, generate_deterministic_evidence_id, EVIDENCE_SCORING_RULES

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
    P0.3-R27 Authoritative Evidence Graph Natal Promise Engine.
    Strict domain/event validation, zero baseline score, structured EvidenceGraph provenance with edges,
    and exact score reconstruction.
    """
    if not event_type:
        return {
            "domain": domain.upper() if domain else "UNKNOWN",
            "event_type": "UNKNOWN",
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": ["Missing event_type."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "evidence_items": [],
            "evidence_graph": {"nodes": [], "edges": []},
            "independence_count": 0,
            "engine_version": "V5.3-EVIDENCE-GRAPH-R27"
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
            "negative_evidence": [f"unsupported_event: '{event_type}' has no registered rule."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "evidence_items": [],
            "evidence_graph": {"nodes": [], "edges": []},
            "independence_count": 0,
            "engine_version": "V5.3-EVIDENCE-GRAPH-R27"
        }

    # Strict domain validation
    if domain and domain.upper() != rule["domain"]:
        return {
            "domain": domain.upper(),
            "event_type": ev_key,
            "promise_level": "INSUFFICIENT_EVIDENCE",
            "promise_score": 0.0,
            "positive_evidence": [],
            "negative_evidence": [f"event_domain_mismatch: event '{ev_key}' belongs to domain '{rule['domain']}', not requested domain '{domain.upper()}'."],
            "relevant_houses": [],
            "relevant_house_lords": [],
            "relevant_planets": [],
            "evidence_items": [],
            "evidence_graph": {"nodes": [], "edges": []},
            "independence_count": 0,
            "engine_version": "V5.3-EVIDENCE-GRAPH-R27"
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
            "evidence_graph": {"nodes": [], "edges": []},
            "independence_count": 0,
            "engine_version": "V5.3-EVIDENCE-GRAPH-R27"
        }

    graph = EvidenceGraph()
    planets = chart_obj.planets
    house_lords = getattr(chart_obj, 'house_lords', {})
    div_charts = getattr(chart_obj, 'divisional_charts', {})
    yogas = getattr(chart_obj, 'yogas', [])

    primary_node_ids = []

    # 1. Evaluate Karakas (Group: SIGNIFICATOR_STRENGTH)
    for idx, k in enumerate(rule["karakas"]):
        if k in planets:
            pdata = planets[k]
            dignity = getattr(pdata, 'dignity', 'Neutral')
            house = getattr(pdata, 'house', 1)
            is_combust = getattr(pdata, 'is_combust', False)
            shadbala = getattr(pdata, 'shadbala_score', None)

            if dignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                val = EVIDENCE_SCORING_RULES["KARAKA_STRONG"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "SIGNIFICATOR_STRENGTH",
                    "independence_key": f"sig_strength_{k}",
                    "polarity": "POSITIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "PLANET_DIGNITY",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"{k} in House {house} ({dignity})",
                    "observed_value": dignity,
                    "operator": "IN",
                    "expected_condition": "Exalted, Moolatrikona, Own Sign",
                    "magnitude": val,
                    "rationale": f"Event significator {k} has strong dignity ({dignity}).",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)
                primary_node_ids.append(node.evidence_id)
            elif dignity in ["Debilitated"]:
                val = EVIDENCE_SCORING_RULES["KARAKA_WEAK"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "SIGNIFICATOR_STRENGTH",
                    "independence_key": f"sig_strength_{k}",
                    "polarity": "NEGATIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "PLANET_DIGNITY",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"{k} in House {house} (Debilitated)",
                    "observed_value": dignity,
                    "operator": "EQ",
                    "expected_condition": "Not Debilitated",
                    "magnitude": val,
                    "rationale": f"Event significator {k} is debilitated.",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)
                primary_node_ids.append(node.evidence_id)

            if is_combust:
                val = EVIDENCE_SCORING_RULES["KARAKA_COMBUST"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "PLANETARY_CONDITION",
                    "independence_key": f"combust_{k}",
                    "polarity": "NEGATIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "COMBUSTION",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"{k} combust by Sun",
                    "observed_value": True,
                    "operator": "EQ",
                    "expected_condition": "Not Combust",
                    "magnitude": val,
                    "rationale": f"Event significator {k} is combust.",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)
                primary_node_ids.append(node.evidence_id)

            if shadbala is not None:
                val = EVIDENCE_SCORING_RULES["SHADBALA_FACTUAL"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "SHADBALA_MODIFIER",
                    "independence_key": f"shadbala_{k}",
                    "polarity": "NEUTRAL",
                    "classification": "FACT",
                    "source_type": "SHADBALA",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"{k} shadbala score {shadbala:.2f}",
                    "observed_value": shadbala,
                    "operator": "FACTUAL",
                    "expected_condition": "Factual Exposure",
                    "magnitude": val,
                    "rationale": f"Event significator {k} raw Shadbala score is {shadbala:.2f}.",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)

    # 2. Evaluate Primary Houses & Lords (Group: LORD_PLACEMENT & HOUSE_STRUCTURE)
    for idx, h in enumerate(rule["primary_houses"]):
        lord = house_lords.get(h)
        if lord and lord in planets:
            lp = planets[lord]
            ldignity = getattr(lp, 'dignity', 'Neutral')
            lhouse = getattr(lp, 'house', 1)

            if ldignity in ["Exalted", "Moolatrikona", "Own Sign"]:
                val = EVIDENCE_SCORING_RULES["LORD_STRONG"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "LORD_PLACEMENT",
                    "independence_key": f"lord_place_{h}_{lord}",
                    "polarity": "POSITIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "HOUSE_LORD",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"House {h} lord {lord} in House {lhouse} ({ldignity})",
                    "observed_value": ldignity,
                    "operator": "IN",
                    "expected_condition": "Strong Dignity",
                    "magnitude": val,
                    "rationale": f"Primary house {h} lord ({lord}) is strong ({ldignity}).",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)
                primary_node_ids.append(node.evidence_id)
            elif ldignity in ["Debilitated"]:
                val = EVIDENCE_SCORING_RULES["LORD_WEAK"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "LORD_PLACEMENT",
                    "independence_key": f"lord_place_{h}_{lord}",
                    "polarity": "NEGATIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "HOUSE_LORD",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"House {h} lord {lord} in House {lhouse} (Debilitated)",
                    "observed_value": ldignity,
                    "operator": "EQ",
                    "expected_condition": "Not Debilitated",
                    "magnitude": val,
                    "rationale": f"Primary house {h} lord ({lord}) is debilitated.",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)
                primary_node_ids.append(node.evidence_id)

        occupants = [pname for pname, pinfo in planets.items() if getattr(pinfo, 'house', 0) == h]
        if occupants and (lord in rule["karakas"] or any(occ in rule["karakas"] for occ in occupants)):
            val = EVIDENCE_SCORING_RULES["HOUSE_OCCUPANCY"]["magnitude"]
            n_dict = {
                "evidence_id": "",
                "event_type": ev_key,
                "domain": rule["domain"],
                "evidence_group": "HOUSE_STRUCTURE",
                "independence_key": f"house_occupancy_{h}",
                "polarity": "POSITIVE",
                "classification": "SCORING_CONTRIBUTION",
                "source_type": "HOUSE_OCCUPANTS",
                "source_path": "app.astrology.predictions.v5_natal_promise",
                "source_fact": f"House {h} tenanted by corroborating {', '.join(occupants)}",
                "observed_value": occupants,
                "operator": "IN",
                "expected_condition": "Event-Relevant Occupants",
                "magnitude": val,
                "rationale": f"Primary house {h} is tenanted by event-relevant factors.",
                "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
            }
            n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
            node = EvidenceNode(**n_dict)
            graph.add_node(node)
            primary_node_ids.append(node.evidence_id)
        elif occupants:
            n_dict = {
                "evidence_id": "",
                "event_type": ev_key,
                "domain": rule["domain"],
                "evidence_group": "HOUSE_STRUCTURE",
                "independence_key": f"house_occupancy_fact_{h}",
                "polarity": "POSITIVE",
                "classification": "FACT",
                "source_type": "HOUSE_OCCUPANTS",
                "source_path": "app.astrology.predictions.v5_natal_promise",
                "source_fact": f"House {h} tenanted by {', '.join(occupants)}",
                "observed_value": occupants,
                "operator": "FACTUAL",
                "expected_condition": "Factual Occupancy",
                "magnitude": 0.0,
                "rationale": f"Primary house {h} is occupied by {', '.join(occupants)}.",
                "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
            }
            n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
            node = EvidenceNode(**n_dict)
            graph.add_node(node)

    # 3. Evaluate Yogas
    if yogas:
        for idx, y in enumerate(yogas):
            y_name = y.get("name", "") if isinstance(y, dict) else getattr(y, 'name', '')
            y_planets = y.get("planets", []) if isinstance(y, dict) else getattr(y, 'planets', [])
            if y_name and any(k in y_planets for k in rule["karakas"]):
                val = EVIDENCE_SCORING_RULES["YOGA_SUPPORT"]["magnitude"]
                n_dict = {
                    "evidence_id": "",
                    "event_type": ev_key,
                    "domain": rule["domain"],
                    "evidence_group": "YOGA_SUPPORT",
                    "independence_key": f"yoga_{y_name}",
                    "polarity": "POSITIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "YOGA",
                    "source_path": "app.astrology.predictions.v5_natal_promise",
                    "source_fact": f"Active event-relevant Yoga: {y_name}",
                    "observed_value": y_name,
                    "operator": "IN",
                    "expected_condition": "Active Formation",
                    "magnitude": val,
                    "rationale": f"Chart exhibits Yoga formation involving event karakas: {y_name}.",
                    "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
                }
                n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
                node = EvidenceNode(**n_dict)
                graph.add_node(node)
                primary_node_ids.append(node.evidence_id)

    # 4. Evaluate Varga Confirmation (Content-based check)
    varga_req = rule.get("varga_required")
    if varga_req and varga_req in div_charts:
        v_data = div_charts[varga_req]
        # Check if varga has actual meaningful content
        if v_data and len(v_data) > 0:
            val = EVIDENCE_SCORING_RULES["VARGA_CONFIRMATION"]["magnitude"]
            n_dict = {
                "evidence_id": "",
                "event_type": ev_key,
                "domain": rule["domain"],
                "evidence_group": "DIVISIONAL_CONFIRMATION",
                "independence_key": f"varga_{varga_req}",
                "polarity": "POSITIVE",
                "classification": "SCORING_CONTRIBUTION",
                "source_type": "DIVISIONAL_CHART",
                "source_path": "app.astrology.predictions.v5_natal_promise",
                "source_fact": f"Divisional chart {varga_req} content verified and aligned",
                "observed_value": varga_req,
                "operator": "EXISTS",
                "expected_condition": "Computed Chart Content",
                "magnitude": val,
                "rationale": f"Divisional chart {varga_req} content corroborates structural baseline.",
                "provenance": {"module": "app.astrology.predictions.v5_natal_promise", "function": "evaluate_natal_promise"}
            }
            n_dict["evidence_id"] = generate_deterministic_evidence_id(n_dict)
            node = EvidenceNode(**n_dict)
            graph.add_node(node)
            primary_node_ids.append(node.evidence_id)

    # Add meaningful causal EvidenceEdges connecting primary contributing nodes
    if len(primary_node_ids) >= 2:
        for i in range(len(primary_node_ids) - 1):
            edge = EvidenceEdge(
                source_id=primary_node_ids[i],
                target_id=primary_node_ids[i+1],
                relation="CORROBORATES",
                provenance={"module": "app.astrology.predictions.v5_natal_promise", "rule": "multifact_confluence"}
            )
            graph.add_edge(edge)

    evidence_items = [n.to_dict() for n in graph.nodes]
    final_score = calculate_score_from_evidence(graph)
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
        "promise_score": final_score,
        "positive_evidence": positive_evidence,
        "negative_evidence": negative_evidence,
        "relevant_houses": rule["primary_houses"],
        "relevant_house_lords": [house_lords.get(h) for h in rule["primary_houses"] if h in house_lords],
        "relevant_planets": rule["karakas"],
        "evidence_items": evidence_items,
        "evidence_graph": graph.to_dict(),
        "independence_count": len(set(i["independence_key"] for i in evidence_items)),
        "engine_version": "V5.3-EVIDENCE-GRAPH-R27"
    }
