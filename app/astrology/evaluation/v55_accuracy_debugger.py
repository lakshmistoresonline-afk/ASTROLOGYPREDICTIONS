from typing import Dict, Any

def debug_false_prediction(prediction_snapshot: Dict[str, Any], actual_outcome: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "predicted_event": prediction_snapshot.get("event_type"),
        "actual_event": actual_outcome.get("event_type"),
        "failure_class": "FALSE_POSITIVE_MINOR_TRIGGER",
        "reason": "Transit trigger activated without sufficient topical Varga confirmation."
    }
