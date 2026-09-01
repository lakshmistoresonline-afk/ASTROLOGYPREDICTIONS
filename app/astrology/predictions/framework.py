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
        "NATAL_PROMISE": 0.25, # Inherent capacity (Primary)
        "SECONDARY_PROMISE": 0.15, # Supporting house lords
        "DASHA_ACTIVATION": 0.20, # Timing - Life period context (Antar)
        "DASHA_FOUNDATION": 0.10, # Timing - Life period foundation (Maha)
        "TRANSIT_TRIGGER": 0.15, # Timing - Immediate trigger (Precision)
        "DIVISIONAL_CONFIRM": 0.10, # Soul/Action confirmation
        "YOGA_SUPPORT": 0.05, # Special combinations
        "ASPECT_SUPPORT": 0.05, # Influences
        "PLANETARY_STRENGTH": 0.05, # Shadbala
        "CONFLICTS": -0.50 # Limiting factors (Contradiction)
    }

    @staticmethod
    def create_evidence(level: str, description: str, score: float,
                        group: str = "PRIMARY", planet: str = None,
                        house: int = None, rationale: str = None) -> CorroborationEvidence:

        weight = CorroborationEngine.WEIGHTS.get(level, 0.0)
        # Score is 0-100+, cap at 100 for normalization (V3.8 Hardening)
        effective_score = min(100.0, score)
        weighted_score = (effective_score / 100.0) * weight

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

        # 1. Group evidence by source and anchor (Planet/House) (V3.8)
        source_contributions = {}
        unique_anchors = set()

        for e in evidence:
            if e.source not in source_contributions:
                source_contributions[e.source] = []
            source_contributions[e.source].append(e.strength_score)

            # Anchor is Planet or House involved
            anchor = e.planet_involved or f"H{e.house_involved}" if e.house_involved else e.source
            if e.strength_score > 0:
                unique_anchors.add(anchor)

        # 2. Calculate Confluence (Positive factors)
        # Take the maximum contribution for each source type to prevent "Node Inflation"
        total_potential = 0.0
        unique_confirmation_layers = 0
        for source, scores in source_contributions.items():
            if any(s > 0 for s in scores):
                total_potential += max(s for s in scores)
                unique_confirmation_layers += 1

        # 3. Calculate Contradiction (Negative factors)
        total_friction = 0.0
        for source, scores in source_contributions.items():
            if any(s < 0 for s in scores):
                total_friction += min(s for s in scores) # Most negative

        # 4. Final Composite Score
        composite_score = total_potential + total_friction

        # 5. Evidence Diversity Bonus (V3.8)
        # Reward convergence of multiple independent layers
        sources = {e.source for e in evidence if e.strength_score > 0}
        diversity_bonus = 0.0
        # If we have (Natal or Secondary) + (Dasha or Foundation) + (Transit or Varga), add bonus
        has_promise = "NATAL_PROMISE" in sources or "SECONDARY_PROMISE" in sources
        has_dasha = "DASHA_ACTIVATION" in sources or "DASHA_FOUNDATION" in sources
        has_trigger = "TRANSIT_TRIGGER" in sources or "DIVISIONAL_CONFIRM" in sources

        if has_promise and has_dasha and has_trigger:
            diversity_bonus = 0.10 # Increased from 0.08 for Recall recovery

        composite_score += diversity_bonus

        # 6. State Determination Model (V3.8 Hardened)
        tw = timing_window or {"phase": "SCANNING", "description": "Analyzing triggers..."}
        phase = tw.get("phase")

        is_peak = phase == "PEAK_MANIFESTATION"
        is_active = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

        # 7. Quality Metric (V3.8)
        # Factors: Evidence density + Independent Anchors + Confluence + Lack of contradictions
        density_bonus = min(0.2, len(evidence) * 0.03)
        anchor_diversity_bonus = min(0.2, len(unique_anchors) * 0.04)
        friction_penalty = abs(total_friction) * 1.5 # Stricter for Precision recovery

        q_score = (composite_score * 0.3) + density_bonus + anchor_diversity_bonus - friction_penalty
        q_score = round(max(0, min(1, q_score)) * 100, 2)

        # 8. Scoring Gates (V3.8 Precision Recovery)
        # PEAK requires high score, peak timing, and high diversity
        if composite_score >= 0.60 and is_peak and q_score >= 48 and len(unique_anchors) >= 3:
            strength = "PEAK"
            confidence = "EXTREME"
        # ACTIVE requires independent layers convergence
        elif composite_score >= 0.42 and is_active and q_score >= 35 and unique_confirmation_layers >= 2:
            strength = "ACTIVE"
            confidence = "HIGH"
        # WATCH is more inclusive
        elif composite_score >= 0.33 or (composite_score >= 0.25 and is_active):
            strength = "WATCH"
            confidence = "MEDIUM"
        elif composite_score > 0:
            strength = "BACKGROUND"
            confidence = "LOW"
        else:
            strength = "INSUFFICIENT DATA"
            confidence = "SCANNING"

        # Special Case: Contradiction override
        if total_friction <= -0.30:
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
