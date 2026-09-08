from typing import List, Dict, Any

def calculate_domain_metrics(predictions: List[Dict[str, Any]], outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    V4 Domain-Specific Metric Calculator.
    Calculates precision, recall, F1, coverage, and abstention rate.
    """
    total = len(predictions)
    if total == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0, "coverage": 0.0, "abstention_rate": 0.0}

    abstentions = sum(1 for p in predictions if p.get("status") in ["INSUFFICIENT EVIDENCE", "CONFLICTING SIGNALS"])
    active_predictions = total - abstentions
    abstention_rate = round((abstentions / total) * 100, 2)
    coverage = round((active_predictions / total) * 100, 2)

    true_positives = sum(1 for m in outcomes if m.get("match_status") == "EXACT MATCH")
    false_positives = sum(1 for m in outcomes if m.get("match_status") in ["NO MATCH", "CONTRADICTORY EVENT"])
    false_negatives = max(0, active_predictions - true_positives)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "total_predictions": total,
        "active_predictions": active_predictions,
        "abstentions": abstentions,
        "abstention_rate": abstention_rate,
        "coverage": coverage,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3)
    }
