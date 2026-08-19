from typing import Dict, Any, List
from .career import get_career_prediction
from .scoring import get_label_from_score

def generate_evidence_based_predictions(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate all domain predictions with evidence and scoring."""
    career = get_career_prediction(chart)

    # Add more domains as they are implemented
    domains = [career]

    # Calculate overall support score
    total_score = sum(d["score"] for d in domains) / len(domains)

    return {
        "overall_score": total_score,
        "overall_label": get_label_from_score(total_score),
        "domains": domains
    }
