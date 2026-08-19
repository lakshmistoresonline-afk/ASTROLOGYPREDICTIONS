from typing import Dict, Any, List
from ..core.models import CanonicalChart, DomainPrediction
from .career import get_career_prediction
from .finance import get_finance_prediction
from .marriage import get_marriage_prediction
from .health import get_health_prediction
from .personality import get_personality_prediction
from .education import get_education_prediction
from .scoring import get_label_from_score

def detect_contradictions(domain_results: DomainPrediction) -> List[str]:
    """Identify conflicting factors across domains."""
    contradictions = []

    # Check for mixed indicators in factors or evidence
    pos = any("✓" in e for e in domain_results.evidence)
    neg = any("⚠" in e for e in domain_results.evidence)

    if pos and neg:
        contradictions.append(f"Mixed signals: both favorable and challenging factors detected.")

    return contradictions

def generate_evidence_based_predictions(chart: CanonicalChart) -> Dict[str, Any]:
    """Aggregate all domain predictions with evidence and scoring."""

    # Domains using the new CanonicalChart model
    personality = get_personality_prediction(chart)
    education = get_education_prediction(chart)

    # Adapting existing engines to the model
    # We pass model_dump() to existing functions that expect dicts
    chart_dict = chart.model_dump()
    career = get_career_prediction(chart_dict)
    finance = get_finance_prediction(chart_dict)
    marriage = get_marriage_prediction(chart_dict)
    health = get_health_prediction(chart_dict)

    domains = [personality, education]

    # Convert dict results to objects for the engine loop
    for d in [career, finance, marriage, health]:
        obj = DomainPrediction(
            domain=d["domain"],
            score=d["score"],
            confidence=d["confidence"],
            summary="",
            evidence=d.get("evidence", []),
            positive_factors=[],
            negative_factors=[],
            contradictions=[],
            timing=[],
            recommendations=[]
        )
        domains.append(obj)

    # Calculate overall support score
    total_score = sum(d.score for d in domains) / len(domains)

    results = []
    for d in domains:
        # Detect contradictions based on evidence strings
        d.contradictions = detect_contradictions(d)
        if d.contradictions and d.confidence == "HIGH":
            d.confidence = "MEDIUM"
        results.append(d.model_dump())

    return {
        "overall_score": round(total_score, 2),
        "overall_label": get_label_from_score(total_score),
        "domains": results
    }
