from typing import List, Dict, Any, Optional
from ..core.models import CorroborationEvidence, DomainPrediction, CanonicalChart

def are_associated(p1_name: str, p2_name: str, planets: Dict[str, Any]) -> bool:
    """Check if two planets are associated by conjunction (Requirement for Yoga Detector)."""
    p1 = planets.get(p1_name)
    p2 = planets.get(p2_name)
    if not p1 or not p2: return False
    return p1.rashi == p2.rashi

class CorroborationEngine:
    """
    Seven-Level Hierarchical Evidence Synthesis (Phase 4/5).
    Implements Dependency Groups and Engineering Weighting Models.
    """

    WEIGHTS = {
        "NATAL_PROMISE": 0.35,
        "DASHA_ACTIVATION": 0.30,
        "TRANSIT_TRIGGER": 0.15,
        "DIVISIONAL_CONFIRM": 0.10,
        "YOGA_SUPPORT": 0.05,
        "MODIFIERS": 0.05,
        "CONFLICTS": -0.40
    }

    @staticmethod
    def create_evidence(level: str, description: str, score: float,
                        group: str = None, planet: str = None, house: int = None) -> CorroborationEvidence:
        weight = CorroborationEngine.WEIGHTS.get(level, 0.0)
        weighted_score = (score / 100.0) * weight
        return CorroborationEvidence(
            source=level,
            planet_involved=planet,
            house_involved=house,
            strength_score=weighted_score,
            description=description
        )

    @staticmethod
    def synthesize(domain: str, promise_level: str, evidence: List[CorroborationEvidence],
                    summary_template: str, timing_window: Dict[str, Any] = None) -> DomainPrediction:

        total_potential = sum(e.strength_score for e in evidence if e.strength_score > 0)
        total_friction = sum(e.strength_score for e in evidence if e.strength_score < 0)

        if total_potential >= 0.75:
            strength = "VERY STRONG"
        elif total_potential >= 0.55:
            strength = "STRONG"
        elif total_potential >= 0.35:
            strength = "MODERATE"
        elif total_potential > 0:
            strength = "WEAK"
        else:
            strength = "INSUFFICIENT DATA"

        if total_friction <= -0.20:
            strength = "MIXED"

        # Production Validation Status (Requirement 20)
        from .data import DOMAIN_STATUS
        validation = DOMAIN_STATUS.get(domain, "NOT TESTED")

        return DomainPrediction(
            domain=domain,
            score=round((total_potential + total_friction) * 100.0, 2),
            confidence="HIGH" if len(evidence) >= 5 else "MEDIUM",
            prediction_strength=strength,
            validation_status=validation,
            summary=summary_template.format(score=total_potential*100, strength=strength, promise=promise_level),
            evidence_chain=evidence,
            supporting_signals=[e.description for e in evidence if e.strength_score > 0],
            conflicting_signals=[e.description for e in evidence if e.strength_score < 0],
            timing_window=timing_window or {"peak": None, "description": "Scanning..."},
            practical_guidance=["Maintain consistent efforts and observe contextual remedies."]
        )
