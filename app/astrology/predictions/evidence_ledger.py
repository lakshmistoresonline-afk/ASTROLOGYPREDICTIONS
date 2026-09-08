from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class EvidenceItem:
    evidence_id: str
    domain: str
    source_family: str  # NATAL, DASHA, TRANSIT, VARGA, YOGA, ASHTAKAVARGA, JAIMINI, KP
    rule_id: str
    description: str
    support_score: float = 0.0
    contradiction_score: float = 0.0
    strength: str = "MODERATE"
    confidence: float = 0.8
    metadata: Dict[str, Any] = field(default_factory=dict)

class EvidenceLedger:
    """
    V4 Machine-Readable Evidence Ledger & Contradiction Engine.
    Ensures independent evidence convergence and explicit contradiction weighting.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.items: List[EvidenceItem] = []

    def add_evidence(self, item: EvidenceItem):
        self.items.append(item)

    def evaluate_net_evidence(self) -> Dict[str, Any]:
        if not self.items:
            return {
                "status": "INSUFFICIENT EVIDENCE",
                "net_score": 0.0,
                "families_count": 0,
                "supported": False
            }

        families = set(item.source_family for item in self.items)
        total_support = sum(item.support_score for item in self.items)
        total_contradiction = sum(item.contradiction_score for item in self.items)
        net_score = total_support - total_contradiction

        # Confirmation Gate: Requires at least 2 independent families (e.g. Natal + Dasha or Transit)
        min_families_required = 2
        has_sufficient_families = len(families) >= min_families_required

        status = "WEAK SIGNAL"
        if net_score >= 0.7 and has_sufficient_families:
            status = "CONVERGENT (STRONG)"
        elif net_score >= 0.4:
            status = "MODERATE SIGNAL"
        elif total_contradiction > total_support:
            status = "CONFLICTING SIGNALS"
        else:
            status = "INSUFFICIENT EVIDENCE"

        return {
            "status": status,
            "net_score": round(net_score, 3),
            "total_support": round(total_support, 3),
            "total_contradiction": round(total_contradiction, 3),
            "independent_families": list(families),
            "families_count": len(families),
            "supported": net_score > 0.4 and has_sufficient_families
        }
