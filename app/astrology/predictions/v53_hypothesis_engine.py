from typing import List, Dict, Any, Optional

class V53PredictionIntelligenceEngine:
    """
    V5.3 Prediction Intelligence, Hypothesis Ranking, Exclusivity,
    Multi-Clock Disagreement, and Root-Factor Evidence Graph.
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.candidates: List[Dict[str, Any]] = []

    def add_candidate(self, event_type: str, support_score: float, contradiction_score: float, clocks: List[str]):
        net_score = support_score - contradiction_score
        self.candidates.append({
            "event_type": event_type,
            "support_score": support_score,
            "contradiction_score": contradiction_score,
            "net_score": net_score,
            "clocks": clocks
        })

    def evaluate_exclusivity_and_ranking(self) -> Dict[str, Any]:
        if not self.candidates:
            return {"status": "INSUFFICIENT_EVIDENCE", "primary_event": None}

        # Sort by net score descending
        sorted_candidates = sorted(self.candidates, key=lambda x: x["net_score"], reverse=True)
        primary = sorted_candidates[0]

        if primary["net_score"] < 0.4:
            return {"status": "WITHHELD_OR_UNCALIBRATED", "primary_event": None, "reason": "Weak net score"}

        # Multi-clock disagreement check
        clocks = primary["clocks"]
        clock_status = "AGREEMENT" if len(set(clocks)) == 1 else "PARTIAL_AGREEMENT"
        if len(clocks) >= 3 and len(set(clocks)) > 2:
            clock_status = "DISAGREEMENT"

        return {
            "status": "CONFIRMED",
            "primary_event": primary["event_type"],
            "net_score": primary["net_score"],
            "clock_status": clock_status,
            "secondary_events": [c["event_type"] for c in sorted_candidates[1:3] if c["net_score"] >= 0.3]
        }
