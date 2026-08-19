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
    from ..dasha import calculate_vimshottari

    # 1. Calculate current Dasha for timing influence
    moon_lon = chart.planets["Moon"].longitude
    dasha_data = calculate_vimshottari(moon_lon, chart.birth_datetime)

    current_maha = dasha_data.get("current_maha", {}).get("lord")
    current_antar = dasha_data.get("current_antar", {}).get("lord")

    # 2. Comprehensive Domain predictions
    from .comprehensive import get_comprehensive_predictions
    domains = get_comprehensive_predictions(chart, active_yogas=chart.yogas, current_dasha=current_maha)

    # 3. Apply Dasha Influence
    # If a domain lord is the current Dasha lord, its impact is amplified
    for d in domains:
        # Simplified: if dasha lord is favorable/unfavorable to the domain
        # This can be expanded with lord relationships
        if current_maha:
            d.evidence.append(f"⏳ Current Mahadasha Lord: {current_maha}")
            d.timing.append({"period": f"{current_maha} Mahadasha", "impact": "Dominant theme"})

    # 4. Calculate overall support score
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
