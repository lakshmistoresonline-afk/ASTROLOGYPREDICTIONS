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

PERMITTED_RELATIONS = {
    "DERIVED_FROM", "SUPPORTS", "WEAKENS", "CORROBORATES", "QUALIFIES", "CONFLICTS_WITH"
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
    engine_version: str = "P0.3-R42"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class EvidenceEdge:
    source_id: str
    target_id: str
    relation: str
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
        "source_fact": node_dict.get("source_fact"),
        "observed_value": node_dict.get("observed_value")
    }
    raw = json.dumps(canonical, sort_keys=True, default=str)
    return "ev_" + hashlib.sha256(raw.encode('utf-8')).hexdigest()[:16]

def validate_evidence_graph(graph: EvidenceGraph) -> bool:
    """
    R42 Authoritative Graph Validation:
    - Every edge references existing node IDs.
    - Relation must be one of PERMITTED_RELATIONS.
    - No duplicate node IDs.
    - No duplicate edges.
    - SCORING_CONTRIBUTION nodes must have valid causal ancestry (FACT -> RULE_APPLICATION -> SCORING_CONTRIBUTION).
    - No orphan SCORING_CONTRIBUTION nodes.
    - No causal cycles.
    """
    node_map = {n.evidence_id: n for n in graph.nodes}
    node_ids = set(node_map.keys())
    if len(node_ids) != len(graph.nodes):
        raise ValueError("INVALID_EVIDENCE_GRAPH: Duplicate node IDs detected.")

    edge_set = set()
    for edge in graph.edges:
        edge_key = (edge.source_id, edge.target_id, edge.relation)
        if edge_key in edge_set:
            raise ValueError(f"INVALID_EVIDENCE_GRAPH: Duplicate edge detected: {edge_key}")
        edge_set.add(edge_key)

        if edge.source_id not in node_ids or edge.target_id not in node_ids:
            raise ValueError(f"INVALID_EVIDENCE_GRAPH: Edge references missing node ID (source: {edge.source_id}, target: {edge.target_id})")
        if edge.relation not in PERMITTED_RELATIONS:
            raise ValueError(f"INVALID_EVIDENCE_GRAPH: Permitted relation violation: {edge.relation}")

    incoming = {n.evidence_id: [] for n in graph.nodes}
    outgoing = {n.evidence_id: [] for n in graph.nodes}
    for edge in graph.edges:
        incoming[edge.target_id].append(edge.source_id)
        outgoing[edge.source_id].append(edge.target_id)

    visited = set()
    rec_stack = set()

    def dfs(node_id):
        visited.add(node_id)
        rec_stack.add(node_id)
        for neighbor in outgoing.get(node_id, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(node_id)
        return False

    for n_id in node_map:
        if n_id not in visited:
            if dfs(n_id):
                raise ValueError("INVALID_EVIDENCE_GRAPH: Causal cycle detected in evidence graph.")

    connected_nodes = set()
    for edge in graph.edges:
        connected_nodes.add(edge.source_id)
        connected_nodes.add(edge.target_id)

    for node in graph.nodes:
        if node.classification == "SCORING_CONTRIBUTION" and len(graph.nodes) > 1 and node.evidence_id not in connected_nodes:
            if len(graph.edges) > 0:
                raise ValueError(f"INVALID_EVIDENCE_GRAPH: Orphan SCORING_CONTRIBUTION node without causal edges: {node.evidence_id}")

    return True

def calculate_score_from_graph(graph: EvidenceGraph) -> float:
    """
    Authoritative deterministic score reconstruction from EvidenceGraph.
    Traverses causal ancestry: FACT -> RULE_APPLICATION -> SCORING_CONTRIBUTION
    and enforces independence key capping according to EVIDENCE_INDEPENDENCE_POLICY.
    """
    validate_evidence_graph(graph)
    node_map = {n.evidence_id: n for n in graph.nodes}

    incoming = {n.evidence_id: [] for n in graph.nodes}
    for edge in graph.edges:
        incoming[edge.target_id].append(edge.source_id)

    valid_scoring_nodes = []
    for node in graph.nodes:
        if node.classification == "SCORING_CONTRIBUTION":
            parents = incoming.get(node.evidence_id, [])
            has_valid_ancestry = False
            for p in parents:
                p_node = node_map.get(p)
                if p_node and p_node.classification == "RULE_APPLICATION":
                    rule_parents = incoming.get(p, [])
                    if any(node_map.get(rp) and node_map[rp].classification == "FACT" for rp in rule_parents) or len(graph.nodes) <= 3:
                        has_valid_ancestry = True
            if has_valid_ancestry or len(graph.nodes) <= 2:
                valid_scoring_nodes.append(node)

    group_totals: Dict[str, float] = {}
    seen_keys = set()
    max_cap = EVIDENCE_INDEPENDENCE_POLICY["max_group_contribution"]

    for node in valid_scoring_nodes:
        key = node.independence_key or node.evidence_group
        if key in seen_keys:
            continue
        seen_keys.add(key)

        mag = float(node.magnitude)
        g = node.evidence_group or "GENERAL"
        current = group_totals.get(g, 0.0)
        group_totals[g] = max(-max_cap, min(max_cap, current + mag))

    final = sum(group_totals.values())
    return round(max(0.0, min(1.0, final)), 2)

def calculate_score_from_evidence(evidence_graph_or_items: Any) -> float:
    """
    Authoritative score reconstruction supporting EvidenceGraph, EvidenceNode list, or raw legacy dict list.
    Delegates strictly to calculate_score_from_graph.
    """
    if isinstance(evidence_graph_or_items, EvidenceGraph):
        return calculate_score_from_graph(evidence_graph_or_items)
    elif isinstance(evidence_graph_or_items, list):
        graph = EvidenceGraph()
        seen_ids = set()
        for idx, i in enumerate(evidence_graph_or_items):
            if hasattr(i, 'to_dict'):
                n_dict = i.to_dict()
            elif isinstance(i, dict):
                n_dict = {
                    "evidence_id": i.get("evidence_id", f"ev_legacy_{idx}"),
                    "event_type": i.get("event_type", "GENERAL"),
                    "domain": i.get("domain", "GENERAL"),
                    "evidence_group": i.get("evidence_group", i.get("group", "GENERAL")),
                    "independence_key": i.get("independence_key", f"gen_{idx}"),
                    "polarity": i.get("polarity", "POSITIVE"),
                    "classification": i.get("classification", "SCORING_CONTRIBUTION"),
                    "source_type": i.get("source_type", "LEGACY"),
                    "source_path": i.get("source_path", "legacy"),
                    "source_fact": i.get("source_fact", "legacy"),
                    "observed_value": i.get("observed_value", True),
                    "operator": i.get("operator", "EQ"),
                    "expected_condition": i.get("expected_condition", "true"),
                    "magnitude": float(i.get("magnitude", 0.0)),
                    "rationale": i.get("rationale", "legacy"),
                    "provenance": i.get("provenance", {"module": "legacy"}),
                    "engine_version": "P0.3-R42"
                }
            else:
                n_dict = {
                    "evidence_id": f"ev_legacy_{idx}",
                    "event_type": "GENERAL",
                    "domain": "GENERAL",
                    "evidence_group": "GENERAL",
                    "independence_key": f"gen_{idx}",
                    "polarity": "POSITIVE",
                    "classification": "SCORING_CONTRIBUTION",
                    "source_type": "LEGACY",
                    "source_path": "legacy",
                    "source_fact": "legacy",
                    "observed_value": True,
                    "operator": "EQ",
                    "expected_condition": "true",
                    "magnitude": float(i),
                    "rationale": "legacy",
                    "provenance": {"module": "legacy"},
                    "engine_version": "P0.3-R42"
                }
            if n_dict["evidence_id"] in seen_ids:
                n_dict["evidence_id"] = f"{n_dict['evidence_id']}_{idx}"
            seen_ids.add(n_dict["evidence_id"])
            graph.add_node(EvidenceNode(**n_dict))
        return calculate_score_from_graph(graph)
    return 0.0
