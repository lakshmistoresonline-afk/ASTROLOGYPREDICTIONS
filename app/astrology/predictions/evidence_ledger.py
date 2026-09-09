from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

VALID_EVIDENCE_FAMILIES = {
    "NATAL",
    "DASHA",
    "TRANSIT",
    "VARGA",
    "YOGA",
    "SHADBALA",
    "ASHTAKAVARGA",
    "JAIMINI",
    "KP",
    "BIRTH_TIME_STABILITY",
    "CALCULATION_CONSENSUS",
    "TIMING_CONVERGENCE"
}

VALID_CORRELATION_TYPES = {
    "INDEPENDENT",
    "DERIVED",
    "CORRELATED",
    "DUPLICATE"
}

@dataclass
class EvidenceItem:
    evidence_id: str
    domain: str
    source_family: str
    rule_id: str
    description: str
    support_score: float = 0.0
    contradiction_score: float = 0.0
    strength: str = "MODERATE"
    confidence: float = 0.8
    correlation_type: str = "INDEPENDENT"  # Track A2: INDEPENDENT, DERIVED, CORRELATED, DUPLICATE
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.source_family not in VALID_EVIDENCE_FAMILIES:
            raise ValueError(f"Invalid evidence family: {self.source_family}")
        if self.correlation_type not in VALID_CORRELATION_TYPES:
            raise ValueError(f"Invalid correlation type: {self.correlation_type}")

class EvidenceLedger:
    """
    V4.3 Machine-Readable Evidence Ledger & Contradiction Engine with Double-Counting Elimination.
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

        # Track A2: Apply correlation weights to eliminate double counting
        total_support = 0.0
        total_contradiction = 0.0

        for item in self.items:
            weight = 1.0
            if item.correlation_type == "DUPLICATE":
                weight = 0.0
            elif item.correlation_type == "CORRELATED":
                weight = 0.5
            elif item.correlation_type == "DERIVED":
                weight = 0.8

            total_support += item.support_score * weight
            total_contradiction += item.contradiction_score * weight

        net_score = total_support - total_contradiction

        # Confirmation Gate: Requires at least 2 independent families
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
