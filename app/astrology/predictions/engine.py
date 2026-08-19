from typing import Dict, Any, List
from .career import get_career_prediction
from .finance import get_finance_prediction
from .marriage import get_marriage_prediction
from .health import get_health_prediction
from .scoring import get_label_from_score

def detect_contradictions(domain_results: Dict[str, Any]) -> List[str]:
    """Identify conflicting factors across domains."""
    contradictions = []
    evidence = domain_results.get("evidence", [])

    # Example: Positive house lord but negative occupant
    positives = [e for e in evidence if "✓" in e]
    negatives = [e for e in evidence if "⚠" in e]

    if positives and negatives:
        contradictions.append(f"Mixed indicators found in {domain_results['domain']}.")

    return contradictions

def generate_evidence_based_predictions(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate all domain predictions with evidence and scoring."""
    career = get_career_prediction(chart)
    finance = get_finance_prediction(chart)
    marriage = get_marriage_prediction(chart)
    health = get_health_prediction(chart)

    domains = [career, finance, marriage, health]

    # Calculate overall support score
    total_score = sum(d["score"] for d in domains) / len(domains)

    # Apply contradiction penalties/notes
    for d in domains:
        d["contradictions"] = detect_contradictions(d)
        if d["contradictions"]:
            # Reduce confidence if contradictions exist
            if d["confidence"] == "HIGH": d["confidence"] = "MEDIUM"
            elif d["confidence"] == "MEDIUM": d["confidence"] = "LOW"

    return {
        "overall_score": round(total_score, 2),
        "overall_label": get_label_from_score(total_score),
        "domains": domains
    }
