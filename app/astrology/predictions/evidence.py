import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from .scoring_registry import SCORING_RULES, SCORING_REGISTRY_VERSION

EVIDENCE_SCORING_RULES = SCORING_RULES

EVIDENCE_INDEPENDENCE_POLICY = {
    "max_group_contribution": 0.35,
    "aggregation_rule": "SUM_WITH_CAPPING",
    "duplicate_handling": "DEDUPLICATE_BY_INDEPENDENCE_KEY",
    "conflict_handling": "NET_POSITIVE_NEGATIVE"
}

@dataclass(frozen=True)
class EvidenceNode:
    evidence_id: str
    event_type: str
    domain: str
    evidence_group: str
    independence_key: str
    polarity: str # POSITIVE | NEGATIVE | NEUTRAL
    classification: str # FACT | RULE_APPLICATION | SCORING_CONTRIBUTION
    source_type: str
    source_path: str
    source_fact: str
    observed_value: Any
    operator: str
    expected_condition: str
    magnitude: float
    rationale: str
    provenance: Dict[str, str]
    engine_version: str = "P0.3-R41"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class EvidenceEdge:
    source_id: str
    target_id: str
    relation: str # DERIVED_FROM | SUPPORTS | WEAKENS | CORROBORATES | QUALIFIES | CONFLICTS_WITH
    provenance: Dict[str, str]

class EvidenceGraph:
    def __init__(self, nodes: List[EvidenceNode] = None, edges: List[EvidenceEdge] = None):
        self.nodes: List[EvidenceNode] = nodes or []
        self.edges: List[EvidenceEdge] = edges or []

    def add_node(self, node: EvidenceNode):
        self.nodes.append(node)

    def add_edge(self, edge: EvidenceEdge):
        self.edges.append(edge)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [asdict(e) for e in self.edges]
        }

def generate_deterministic_evidence_id(node_dict: Dict[str, Any]) -> str:
    canonical = {
        "event_type": node_dict.get("event_type"),
        "domain": node_dict.get("domain"),
        "independence_key": node_dict.get("independence_key"),
        "source_type": node_dict.get("source_type"),
        "source_fact": node_dict.get("source_fact")
    }
    raw = json.dumps(canonical, sort_keys=True, default=str)
    return "ev_" + hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]

def validate_evidence_graph(graph: EvidenceGraph) -> bool:
    """
    R41 Graph Validation:
    - No edge references missing node IDs.
    """
    node_ids = {n.evidence_id for n in graph.nodes}
    for edge in graph.edges:
        if edge.source_id not in node_ids or edge.target_id not in node_ids:
            raise ValueError(f"INVALID_EVIDENCE_GRAPH: Edge references missing node ID (source: {edge.source_id}, target: {edge.target_id})")
    return True

def calculate_score_from_graph(graph: EvidenceGraph) -> float:
    """
    Authoritative deterministic score reconstruction from EvidenceGraph.
    Validates graph structure and enforces independence key capping according to EVIDENCE_INDEPENDENCE_POLICY.
    """
    validate_evidence_graph(graph)
    items = [n.to_dict() for n in graph.nodes]

    group_totals: Dict[str, float] = {}
    seen_keys = set()
    max_cap = EVIDENCE_INDEPENDENCE_POLICY["max_group_contribution"]

    for item in items:
        if item.get("classification") == "FACT":
            continue
        key = item.get("independence_key", item.get("evidence_group", "GENERAL"))
        if key in seen_keys:
            continue
        seen_keys.add(key)

        mag = float(item.get("magnitude", 0.0))
        g = item.get("evidence_group", "GENERAL")
        current = group_totals.get(g, 0.0)
        group_totals[g] = max(-max_cap, min(max_cap, current + mag))

    final = sum(group_totals.values())
    return round(max(0.0, min(1.0, final)), 2)

def calculate_score_from_evidence(evidence_graph_or_items: Any) -> float:
    """
    Authoritative score reconstruction supporting EvidenceGraph, EvidenceNode list, or raw legacy dict list.
    """
    if isinstance(evidence_graph_or_items, EvidenceGraph):
        return calculate_score_from_graph(evidence_graph_or_items)
    elif isinstance(evidence_graph_or_items, list):
        items = []
        for i in evidence_graph_or_items:
            if hasattr(i, 'to_dict'):
                items.append(i.to_dict())
            elif isinstance(i, dict):
                items.append(i)
            else:
                items.append({"magnitude": float(i)})

        group_totals: Dict[str, float] = {}
        seen_keys = set()
        max_cap = EVIDENCE_INDEPENDENCE_POLICY["max_group_contribution"]

        for item in items:
            key = item.get("independence_key", item.get("evidence_group", "GENERAL"))
            if key in seen_keys:
                continue
            seen_keys.add(key)

            mag = float(item.get("magnitude", 0.0))
            g = item.get("evidence_group", "GENERAL")
            current = group_totals.get(g, 0.0)
            group_totals[g] = max(-max_cap, min(max_cap, current + mag))

        final = sum(group_totals.values())
        return round(max(0.0, min(1.0, final)), 2)
    return 0.0
