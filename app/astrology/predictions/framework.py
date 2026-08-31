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
        "NATAL_PROMISE": 0.25, # Inherent capacity
        "DASHA_ACTIVATION": 0.15, # Timing - Life period context
        "TRANSIT_TRIGGER": 0.40, # Timing - Immediate trigger
        "DIVISIONAL_CONFIRM": 0.15, # Soul/Action confirmation
        "YOGA_SUPPORT": 0.05, # Special combinations
        "ASPECT_SUPPORT": 0.05, # Influences
        "PLANETARY_STRENGTH": 0.05, # Shadbala
        "CONFLICTS": -0.60 # Limiting factors (Contradiction)
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

        # 1. Group evidence by source to prevent double-counting (V3.7 Hardening)
        source_contributions = {}
        for e in evidence:
            if e.source not in source_contributions:
                source_contributions[e.source] = []
            source_contributions[e.source].append(e.strength_score)

        # 2. Calculate Confluence (Positive factors)
        # Take the maximum contribution for each source type to prevent "Node Inflation"
        total_potential = 0.0
        for source, scores in source_contributions.items():
            if any(s > 0 for s in scores):
                total_potential += max(s for s in scores)

        # 3. Calculate Contradiction (Negative factors)
        total_friction = 0.0
        for source, scores in source_contributions.items():
            if any(s < 0 for s in scores):
                total_friction += min(s for s in scores) # Most negative

        # 4. Final Composite Score
        composite_score = total_potential + total_friction

        # 4. Evidence Diversity Bonus (V3.7)
        # Reward convergence of independent layers
        sources = {e.source for e in evidence if e.strength_score > 0}
        diversity_bonus = 0.0
        if "NATAL_PROMISE" in sources and "DASHA_ACTIVATION" in sources and "TRANSIT_TRIGGER" in sources:
            diversity_bonus = 0.05

        composite_score += diversity_bonus

        # 5. State Determination Model (V3.7 Hardened)
        tw = timing_window or {"phase": "SCANNING", "description": "Analyzing triggers..."}
        phase = tw.get("phase")

        is_peak = phase == "PEAK_MANIFESTATION"
        is_active = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]
        is_watch = phase == "BUILD_UP" or (is_active and composite_score < 0.48)

        # Quality Gate (V3.7 Hardened)
        # Factors: Evidence density + Confluence + Lack of contradictions
        density_bonus = min(0.2, len(evidence) * 0.04)
        friction_penalty = abs(total_friction)
        q_score = (composite_score * 0.4) + density_bonus - (friction_penalty * 0.8)
        q_score = round(max(0, min(1, q_score)) * 100, 2)

        # Scoring Gates (V3.7 Hardened)
        if composite_score >= 0.65 and is_peak and q_score >= 50:
            strength = "PEAK"
            confidence = "EXTREME"
        elif composite_score >= 0.54 and is_active and q_score >= 42:
            strength = "ACTIVE"
            confidence = "HIGH"
        elif composite_score >= 0.38 or (composite_score >= 0.28 and is_watch):
            strength = "WATCH"
            confidence = "MEDIUM"
        elif composite_score > 0:
            strength = "BACKGROUND"
            confidence = "LOW"
        else:
            strength = "INSUFFICIENT DATA"
            confidence = "SCANNING"

        # Special Case: Contradiction override
        if total_friction <= -0.25:
             strength = "MIXED"
             confidence = "VARYING"

        composite_score = max(0, min(1, composite_score))

        # 5. Extract Lists
        supporting = [e.description for e in evidence if e.strength_score > 0]
        contradicting = [e.description for e in evidence if e.strength_score < 0]

        from .data import DOMAIN_STATUS
        validation = DOMAIN_STATUS.get(domain, "UNDER REVIEW")

        # 6. Build Timing
        tw = timing_window or {"phase": "SCANNING", "description": "Analyzing triggers..."}

        return DomainPrediction(
            domain=domain,
            headline=f"{strength}: {domain} Trends",
            score=round(composite_score * 100, 2),
            quality_score=q_score,
            confidence=confidence,
            prediction_strength=strength,
            validation_status=validation,
            summary=summary_template.format(score=int(composite_score*100), strength=strength, promise=promise_level),
            evidence_chain=evidence,
            supporting_factors=supporting,
            contradicting_factors=contradicting,
            timing_window=tw,
            practical_actions=["Evaluate current planetary peak before major shifts."]
        )
