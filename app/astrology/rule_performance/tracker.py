from typing import Dict, Any, List

class RulePerformanceTracker:
    """
    V4 Rule Performance Engine.
    Tracks success count, precision, recall, and timing error for every prediction rule.
    """
    def __init__(self):
        self.registry: Dict[str, Dict[str, Any]] = {}

    def record_rule_result(self, rule_id: str, domain: str, evidence_family: str, success: bool, timing_error_days: int = None):
        if rule_id not in self.registry:
            self.registry[rule_id] = {
                "rule_id": rule_id,
                "domain": domain,
                "evidence_family": evidence_family,
                "sample_size": 0,
                "successes": 0,
                "failures": 0,
                "total_timing_error": 0
            }

        entry = self.registry[rule_id]
        entry["sample_size"] += 1
        if success:
            entry["successes"] += 1
        else:
            entry["failures"] += 1

        if timing_error_days is not None:
            entry["total_timing_error"] += timing_error_days

    def get_rule_stats(self, rule_id: str) -> Dict[str, Any]:
        entry = self.registry.get(rule_id)
        if not entry or entry["sample_size"] == 0:
            return {"precision": 0.0, "sample_size": 0, "status": "NO DATA"}

        precision = entry["successes"] / entry["sample_size"]
        avg_timing_error = entry["total_timing_error"] / entry["sample_size"] if entry["sample_size"] > 0 else 0

        return {
            "rule_id": rule_id,
            "sample_size": entry["sample_size"],
            "precision": round(precision, 3),
            "avg_timing_error_days": round(avg_timing_error, 1),
            "status": "MEASURED"
        }

rule_tracker = RulePerformanceTracker()
