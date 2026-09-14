import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional

@dataclass(frozen=True)
class EvidenceNode:
    evidence_id: str
    event_type: str
    domain: str
    evidence_group: str
    independence_key: str
    polarity: str # POSITIVE | NEGATIVE
    source_type: str
    source_path: str
    source_fact: str
    observed_value: Any
    operator: str
    expected_condition: str
    magnitude: float
    rationale: str
    provenance: Dict[str, str]
    engine_version: str = "P0.3-R26"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class EvidenceEdge:
    source_id: str
    target_id: str
    relation: str

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
            "edges": [{"source_id": e.source_id, "target_id": e.target_id, "relation": e.relation} for e in self.edges]
        }

def calculate_score_from_evidence(evidence_graph_or_items: Any) -> float:
    """
    Authoritative deterministic score reconstruction from evidence graph or list of evidence items.
    Enforces independence key capping and zero baseline.
    """
    if isinstance(evidence_graph_or_items, EvidenceGraph):
        items = [n.to_dict() for n in evidence_graph_or_items.nodes]
    elif isinstance(evidence_graph_or_items, list):
        items = [i.to_dict() if hasattr(i, 'to_dict') else i for i in evidence_graph_or_items]
    else:
        items = []

    group_totals: Dict[str, float] = {}
    for item in items:
        key = item.get("independence_key", item.get("evidence_group", "GENERAL"))
        mag = float(item.get("magnitude", 0.0))
        current = group_totals.get(key, 0.0)
        group_totals[key] = max(-0.35, min(0.35, current + mag))

    final = sum(group_totals.values())
    return round(max(0.0, min(1.0, final)), 2)
