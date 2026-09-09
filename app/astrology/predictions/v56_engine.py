from typing import List, Dict, Any, Optional

class V56MasterIntelligenceEngine:
    """
    V5.6 Unified Prediction Intelligence Engine.
    Integrates Event Hypothesis, Negative Evidence, Evidence Graph 2.0,
    Multi-Clock Disagreement, Event Competition, and Birth-Time Stability 2.0.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.candidates: List[Dict[str, Any]] = []

    def add_candidate(self, event_type: str, support_score: float, contradiction_score: float, clocks: List[str], stability_score: float = 0.9):
        # Negative evidence suppression if contradiction or instability is high
        effective_support = support_score
        if contradiction_score > 0.4:
            effective_support -= 0.3
        if stability_score < 0.6:
            effective_support -= 0.2

        net_score = max(0.0, effective_support - contradiction_score)

        self.candidates.append({
            "event_type": event_type,
            "net_score": round(net_score, 3),
            "clocks": clocks,
            "stability_score": stability_score,
            "status": "PRIMARY" if net_score >= 0.7 else ("SECONDARY" if net_score >= 0.4 else "WITHHELD")
        })

    def run_competition(self) -> Dict[str, Any]:
        if not self.candidates:
            return {"status": "INSUFFICIENT_EVIDENCE", "primary": None, "candidates": []}

        sorted_cands = sorted(self.candidates, key=lambda x: x["net_score"], reverse=True)
        primary = sorted_cands[0]

        if primary["status"] == "WITHHELD":
            return {"status": "WITHHELD", "primary": None, "candidates": sorted_cands}

        return {
            "status": "CONFIRMED",
            "primary": primary,
            "candidates": sorted_cands
        }
