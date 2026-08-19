from typing import List, Dict, Any

def calculate_weighted_score(factors: List[Dict[str, Any]]) -> float:
    """
    Calculate a score from 0-100 based on weighted factors.
    Each factor: {"weight": 0.1, "score": 80, "label": "Text"}
    """
    total_weight = sum(f["weight"] for f in factors)
    if total_weight == 0:
        return 50.0

    weighted_sum = sum(f["weight"] * f["score"] for f in factors)
    return weighted_sum / total_weight

def get_label_from_score(score: float) -> str:
    """Map a 0-100 score to a qualitative label."""
    if score >= 91: return "Exceptional"
    if score >= 76: return "Strong"
    if score >= 61: return "Good"
    if score >= 41: return "Moderate"
    if score >= 21: return "Weak"
    return "Very Weak"
