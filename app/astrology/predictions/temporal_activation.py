import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..core.models import CanonicalChart
from ..dasha import calculate_vimshottari
from ..core.datetime import datetime_to_jd
from ..core import ephemeris
from ..core.swe_proxy import swe
from .evidence import EvidenceNode, EvidenceEdge, EvidenceGraph, calculate_score_from_evidence, generate_deterministic_evidence_id
from .temporal_rules import TEMPORAL_EVENT_RULES, TEMPORAL_RULE_REGISTRY_VERSION
from .v5_natal_promise import evaluate_natal_promise

ASPECT_RULES = {
    "CONJUNCTION": {"angle": 0.0, "max_orb": 6.0, "magnitude": 0.15, "polarity": "POSITIVE"},
    "OPPOSITION": {"angle": 180.0, "max_orb": 6.0, "magnitude": 0.12, "polarity": "NEGATIVE"},
    "TRINE": {"angle": 120.0, "max_orb": 5.0, "magnitude": 0.15, "polarity": "POSITIVE"},
    "SQUARE": {"angle": 90.0, "max_orb": 5.0, "magnitude": -0.12, "polarity": "NEGATIVE"},
    "SEXTILE": {"angle": 60.0, "max_orb": 4.0, "magnitude": 0.10, "polarity": "POSITIVE"}
}

class TemporalActivationResult:
    def __init__(
        self,
        target_datetime: datetime,
        timezone: str,
        dasha_data: Dict[str, Any],
        transit_positions: Dict[str, float],
        activation_score: float,
        confluence_state: str,
        temporal_evidence: List[Dict[str, Any]],
        evidence_graph: Dict[str, Any],
        provenance: Dict[str, str],
        engine_version: str = "P0.3-R39"
    ):
        self.target_datetime = target_datetime
        self.timezone = timezone
        self.dasha_data = dasha_data
        self.transit_positions = transit_positions
        self.activation_score = activation_score
        self.confluence_state = confluence_state
        self.temporal_evidence = temporal_evidence
        self.evidence_graph = evidence_graph
        self.provenance = provenance
        self.engine_version = engine_version

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_datetime": self.target_datetime.isoformat(),
            "timezone": self.timezone,
            "dasha_data": self.dasha_data,
            "transit_positions": self.transit_positions,
            "activation_score": self.activation_score,
            "confluence_state": self.confluence_state,
            "temporal_evidence": self.temporal_evidence,
            "evidence_graph": self.evidence_graph,
            "provenance": self.provenance,
            "engine_version": self.engine_version
        }

def evaluate_temporal_activation(chart: CanonicalChart, selected_date: datetime, domain: str = "GENERAL", event_type: str = "GENERAL") -> TemporalActivationResult:
    """
    P0.3-R39 Authoritative Event-Specific Temporal Activation & Confluence Engine.
    Enforces true natal promise gate, Dasha rule evaluation, Swiss Ephemeris transit aspects,
    and exact score reconstruction.
    """
    if selected_date is None:
        raise ValueError("INVALID_REQUEST: selected_date is required for temporal activation.")

    if not chart or not hasattr(chart, 'planets') or not chart.planets:
        raise ValueError("MISSING_CHART_PROVENANCE: Chart planetary data required for temporal activation.")

    tz_str = getattr(chart, 'timezone', 'UTC')
    ev_key = event_type.upper().replace(" ", "_")
    dom_key = domain.upper()

    t_rule = TEMPORAL_EVENT_RULES.get(ev_key, {
        "karakas": [],
        "dasha_lords": [],
        "transit_planets": [],
        "permitted_aspects": ["CONJUNCTION"],
        "max_orb": 6.0,
        "rule_id": "R39-DEFAULT-01",
        "domain": dom_key
    })

    # 1. Authoritative Natal Promise Gate
    natal_res = evaluate_natal_promise(chart, t_rule.get("domain", dom_key), ev_key)
    natal_score = float(natal_res.get("promise_score", 0.0))
    natal_supported = natal_score >= 0.30

    # 2. Dasha Calculation
    moon_lon = chart.planets["Moon"].longitude
    dasha = calculate_vimshottari(moon_lon, chart.birth_datetime, calculation_date=selected_date)

    # 3. Transit Calculation via Swiss Ephemeris (FAIL CLOSED ON ERROR - NO NATAL FALLBACK)
    transits = {}
    try:
        jd_ut = datetime_to_jd(selected_date, tz_str)
        planet_map = {
            "Sun": swe.SUN,
            "Moon": swe.MOON,
            "Mars": swe.MARS,
            "Mercury": swe.MERCURY,
            "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS,
            "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE
        }
        for name, pid in planet_map.items():
            p_info = ephemeris.get_planet_position(jd_ut, pid)
            transits[name] = p_info["longitude"]
        transits["Ketu"] = (transits.get("Rahu", 0.0) + 180.0) % 360.0

        if not transits:
            raise RuntimeError("Swiss Ephemeris returned empty transit positions.")
    except Exception as e:
        raise RuntimeError(f"CALCULATION_ENGINE_UNAVAILABLE: Failed to calculate Swiss Ephemeris transits for target date {selected_date}: {e}")

    graph = EvidenceGraph()
    primary_node_ids = []

    maha = dasha.get("current_maha", {}).get("lord", "Unknown")
    antar = dasha.get("current_antar", {}).get("lord", "Unknown")

    # Dasha Fact Node
    dasha_fact_dict = {
        "evidence_id": "",
        "event_type": ev_key,
        "domain": t_rule.get("domain", dom_key),
        "evidence_group": "DASHA_ACTIVATION",
        "independence_key": f"dasha_{maha}_{antar}",
        "polarity": "NEUTRAL",
        "classification": "FACT",
        "source_type": "DASHA",
        "source_path": "app.astrology.dasha",
        "source_fact": f"Active Mahadasha: {maha}, Antardasha: {antar}",
        "observed_value": {"mahadasha": maha, "antardasha": antar},
        "operator": "EQ",
        "expected_condition": "Active Period",
        "magnitude": 0.0,
        "rationale": f"Current life period is ruled by Mahadasha {maha} and Antardasha {antar}.",
        "provenance": {"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"}
    }
    dasha_fact_dict["evidence_id"] = generate_deterministic_evidence_id(dasha_fact_dict)
    node_dasha_fact = EvidenceNode(**dasha_fact_dict)
    graph.add_node(node_dasha_fact)
    primary_node_ids.append(node_dasha_fact.evidence_id)

    # Event-Specific Dasha Rule Application
    allowed_dasha_lords = t_rule.get("dasha_lords", []) + t_rule.get("karakas", [])
    is_dasha_activated = (maha in allowed_dasha_lords or antar in allowed_dasha_lords)
    if is_dasha_activated:
        dasha_rule_dict = {
            "evidence_id": "",
            "event_type": ev_key,
            "domain": t_rule.get("domain", dom_key),
            "evidence_group": "DASHA_ACTIVATION",
            "independence_key": f"dasha_rule_{dom_key}_{ev_key}",
            "polarity": "POSITIVE",
            "classification": "RULE_APPLICATION",
            "source_type": "TEMPORAL_RULE",
            "source_path": "app.astrology.predictions.temporal_activation",
            "source_fact": f"Dasha lords ({maha}/{antar}) match event rule {t_rule['rule_id']}",
            "observed_value": [maha, antar],
            "operator": "IN",
            "expected_condition": "Event-Relevant Period Lord",
            "magnitude": 0.15,
            "rationale": f"Active period lords ({maha}/{antar}) activate temporal rule {t_rule['rule_id']} for {ev_key}.",
            "provenance": {"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"}
        }
        dasha_rule_dict["evidence_id"] = generate_deterministic_evidence_id(dasha_rule_dict)
        node_dasha_rule = EvidenceNode(**dasha_rule_dict)
        graph.add_node(node_dasha_rule)
        primary_node_ids.append(node_dasha_rule.evidence_id)

        graph.add_edge(EvidenceEdge(
            source_id=node_dasha_fact.evidence_id,
            target_id=node_dasha_rule.evidence_id,
            relation="DERIVED_FROM",
            provenance={"module": "app.astrology.predictions.temporal_activation", "rule": "dasha_derivation"}
        ))

    # Transit Fact Node
    transit_fact_dict = {
        "evidence_id": "",
        "event_type": ev_key,
        "domain": t_rule.get("domain", dom_key),
        "evidence_group": "TRANSIT_ACTIVATION",
        "independence_key": "swiss_ephemeris_transits",
        "polarity": "NEUTRAL",
        "classification": "FACT",
        "source_type": "SWISS_EPHEMERIS",
        "source_path": "app.astrology.core.ephemeris",
        "source_fact": f"Calculated {len(transits)} transit longitudes for target date {selected_date.isoformat()}",
        "observed_value": len(transits),
        "operator": "GT",
        "expected_condition": "Non-empty Ephemeris Calculation",
        "magnitude": 0.0,
        "rationale": f"Swiss Ephemeris successfully computed precise planetary transits for target datetime {selected_date.isoformat()}.",
        "provenance": {"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"}
    }
    transit_fact_dict["evidence_id"] = generate_deterministic_evidence_id(transit_fact_dict)
    node_transit_fact = EvidenceNode(**transit_fact_dict)
    graph.add_node(node_transit_fact)

    # Check Transit Aspects using ASPECT_RULES and event-specific permitted transit planets / aspects
    permitted_transits = t_rule.get("transit_planets", [])
    permitted_aspects = t_rule.get("permitted_aspects", ["CONJUNCTION"])
    max_orb = t_rule.get("max_orb", 6.0)

    transit_activated = False
    for t_planet, t_lon in transits.items():
        if permitted_transits and t_planet not in permitted_transits:
            continue
        for k in t_rule.get("karakas", []):
            if k in chart.planets:
                n_lon = chart.planets[k].longitude
                diff = abs(t_lon - n_lon) % 360.0
                if diff > 180: diff = 360 - diff

                for asp_name, asp_spec in ASPECT_RULES.items():
                    if asp_name not in permitted_aspects:
                        continue
                    target_angle = asp_spec["angle"]
                    orb_limit = min(max_orb, asp_spec["max_orb"])
                    if abs(diff - target_angle) <= orb_limit:
                        transit_activated = True
                        t_rule_dict = {
                            "evidence_id": "",
                            "event_type": ev_key,
                            "domain": t_rule.get("domain", dom_key),
                            "evidence_group": "TRANSIT_ACTIVATION",
                            "independence_key": f"transit_{asp_name.lower()}_{t_planet}_{k}",
                            "polarity": asp_spec["polarity"],
                            "classification": "RULE_APPLICATION",
                            "source_type": "TRANSIT_ASPECT",
                            "source_path": "app.astrology.predictions.temporal_activation",
                            "source_fact": f"Transit {t_planet} {asp_name.lower()} natal {k} within {abs(diff - target_angle):.2f} deg orb",
                            "observed_value": diff,
                            "operator": "LTE",
                            "expected_condition": f"Aspect {target_angle} +/- {orb_limit}",
                            "magnitude": asp_spec["magnitude"],
                            "rationale": f"Transit {t_planet} forms {asp_name} to natal {k} under rule {t_rule['rule_id']}, triggering temporal activation for {ev_key}.",
                            "provenance": {"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"}
                        }
                        t_rule_dict["evidence_id"] = generate_deterministic_evidence_id(t_rule_dict)
                        node_t_rule = EvidenceNode(**t_rule_dict)
                        graph.add_node(node_t_rule)
                        primary_node_ids.append(node_t_rule.evidence_id)

                        graph.add_edge(EvidenceEdge(
                            source_id=node_transit_fact.evidence_id,
                            target_id=node_t_rule.evidence_id,
                            relation="CORROBORATES",
                            provenance={"module": "app.astrology.predictions.temporal_activation", "rule": "aspect_confluence"}
                        ))

    # Confluence State Determination
    if not natal_supported:
        confluence_state = "NATAL_NOT_SUPPORTED"
    elif is_dasha_activated and transit_activated:
        confluence_state = "NATAL_AND_TEMPORAL_CONFLUENCE"
    elif is_dasha_activated:
        confluence_state = "DASHA_ACTIVE_ONLY"
    elif transit_activated:
        confluence_state = "TRANSIT_ACTIVE_ONLY"
    else:
        confluence_state = "NATAL_SUPPORTED_TEMPORAL_INACTIVE"

    evidence_items = [n.to_dict() for n in graph.nodes]
    activation_score = calculate_score_from_evidence(graph)

    return TemporalActivationResult(
        target_datetime=selected_date,
        timezone=tz_str,
        dasha_data=dasha,
        transit_positions=transits,
        activation_score=activation_score,
        confluence_state=confluence_state,
        temporal_evidence=evidence_items,
        evidence_graph=graph.to_dict(),
        provenance={"module": "app.astrology.predictions.temporal_activation", "function": "evaluate_temporal_activation"},
        engine_version="P0.3-R39"
    )
