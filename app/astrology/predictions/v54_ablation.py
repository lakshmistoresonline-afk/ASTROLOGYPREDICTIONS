from typing import Dict, Any, List

def run_counterfactual_ablation(prediction_context: Dict[str, Any], excluded_layers: List[str]) -> Dict[str, Any]:
    """
    V5.4 Counterfactual Ablation Engine.
    Evaluates prediction state when specified evidence families are removed.
    """
    base_score = prediction_context.get("score", 75.0)
    penalties = {
        "NATAL": 25.0,
        "DASHA": 20.0,
        "TRANSIT": 15.0,
        "VARGA": 10.0,
        "JAIMINI": 5.0,
        "KP": 5.0
    }

    effective_score = base_score
    for layer in excluded_layers:
        if layer in penalties:
            effective_score -= penalties[layer]

    effective_score = max(0.0, effective_score)

    state = "ACTIVE"
    if effective_score < 40.0:
        state = "WITHHELD"
    elif effective_score < 60.0:
        state = "WATCH"

    return {
        "excluded_layers": excluded_layers,
        "effective_score": round(effective_score, 1),
        "state": state,
        "reason": f"Ablation of {excluded_layers} reduced effective score to {effective_score}"
    }
