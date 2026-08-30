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
    V2 Pro Intelligence Engine.
    Implements Hierarchical Confluence, Contradiction Penalties, and Node-by-Node evidence.
    """

    WEIGHTS = {
        "NATAL_PROMISE": 0.35, # Inherent capacity
        "DASHA_ACTIVATION": 0.25, # Timing - Life period
        "TRANSIT_TRIGGER": 0.15, # Timing - Current sky
        "DIVISIONAL_CONFIRM": 0.10, # Soul/Action confirmation
        "YOGA_SUPPORT": 0.05, # Special combinations
        "ASPECT_SUPPORT": 0.05, # Influences
        "PLANETARY_STRENGTH": 0.05, # Shadbala
        "CONFLICTS": -0.40 # Limiting factors (Contradiction)
    }

    @staticmethod
    def create_evidence(level: str, description: str, score: float,
                        group: str = "PRIMARY", planet: str = None,
                        house: int = None, rationale: str = None) -> CorroborationEvidence:

        weight = CorroborationEngine.WEIGHTS.get(level, 0.0)
        # Score is 0-100, normalize to weighted impact
        weighted_score = (score / 100.0) * weight

        return CorroborationEvidence(
            source=level,
            level=group,
            planet_involved=planet,
            house_involved=house,
            strength_score=weighted_score,
            description=description,
            rationale=rationale
        )

    @staticmethod
    def synthesize(domain: str, promise_level: str, evidence: List[CorroborationEvidence],
                    summary_template: str, timing_window: Dict[str, Any] = None) -> DomainPrediction:

        # 1. Calculate Confluence (Positive factors)
        total_potential = sum(e.strength_score for e in evidence if e.strength_score > 0)

        # 2. Calculate Contradiction (Negative factors)
        total_friction = sum(e.strength_score for e in evidence if e.strength_score < 0)

        # 3. Final Composite Score
        composite_score = max(0, min(1, total_potential + total_friction))

        # 4. Determine Confidence Labels
        if total_friction <= -0.20:
             strength = "MIXED"
             confidence = "VARYING"
        elif composite_score >= 0.80:
            strength = "VERY STRONG"
            confidence = "EXTREME"
        elif composite_score >= 0.60:
            strength = "STRONG"
            confidence = "HIGH"
        elif composite_score >= 0.40:
            strength = "MODERATE"
            confidence = "MEDIUM"
        elif composite_score >= 0.20:
            strength = "CONDITIONAL"
            confidence = "VARYING"
        elif composite_score > 0:
            strength = "WEAK"
            confidence = "LOW"
        else:
            strength = "INSUFFICIENT DATA"
            confidence = "SCANNING"

        # 5. Extract Lists
        supporting = [e.description for e in evidence if e.strength_score > 0]
        conflicting = [e.description for e in evidence if e.strength_score < 0]

        from .data import DOMAIN_STATUS
        validation = DOMAIN_STATUS.get(domain, "UNDER REVIEW")

        # 6. Build Timing
        tw = timing_window or {"phase": "SCANNING", "description": "Analyzing triggers..."}

        return DomainPrediction(
            domain=domain,
            headline=f"{strength}: {domain} Trends",
            score=round(composite_score * 100, 2),
            confidence=confidence,
            prediction_strength=strength,
            validation_status=validation,
            summary=summary_template.format(score=int(composite_score*100), strength=strength, promise=promise_level),
            evidence_chain=evidence,
            supporting_signals=supporting,
            conflicting_signals=conflicting,
            timing_window=tw,
            practical_actions=["Evaluate current planetary peak before major shifts."]
        )
