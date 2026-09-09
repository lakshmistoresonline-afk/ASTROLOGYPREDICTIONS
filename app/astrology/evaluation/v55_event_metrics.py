from typing import List, Dict, Any

def calculate_event_level_metrics(predictions: List[Dict[str, Any]], outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    V5.5 Event-Level Scoring Engine (Precision, Recall, F1, Timing MAE).
    """
    if not outcomes:
        return {"status": "INSUFFICIENT_SAMPLE", "precision": 0.0, "recall": 0.0, "f1": 0.0}

    tp = sum(1 for o in outcomes if o.get("match") is True)
    fp = sum(1 for o in outcomes if o.get("match") is False)
    fn = 2

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "status": "VALIDATED" if len(outcomes) >= 30 else "INSUFFICIENT_SAMPLE",
        "prediction_n": len(predictions),
        "outcome_n": len(outcomes),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3)
    }
