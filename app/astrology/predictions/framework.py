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
        "NATAL_PROMISE": 0.40, # Primary foundation
        "SECONDARY_PROMISE": 0.05, # Supporting placements
        "DASHA_ACTIVATION": 0.20, # Timing - Life period (Antar)
        "DASHA_FOUNDATION": 0.05, # Timing - Life period (Maha)
        "TRANSIT_TRIGGER": 0.25, # Timing - Current sky (Trigger)
        "DIVISIONAL_CONFIRM": 0.12, # Soul/Action confirmation
        "YOGA_SUPPORT": 0.05, # Special combinations
        "ASPECT_SUPPORT": 0.05, # Influences
        "PLANETARY_STRENGTH": 0.05, # Shadbala
        "CONFLICTS": -0.70 # Limiting factors (Increased penalty)
    }

    @staticmethod
    def create_evidence(level: str, description: str, score: float,
                        group: str = "PRIMARY", planet: str = None,
                        house: int = None, rationale: str = None) -> CorroborationEvidence:

        weight = CorroborationEngine.WEIGHTS.get(level, 0.0)
        # Score is 0-100, normalize to weighted impact (Handle as magnitude)
        abs_score = min(100.0, abs(score))
        weighted_score = (abs_score / 100.0) * weight

        return CorroborationEvidence(
            source=level,
            level=group,
            planet_involved=planet,
            house_involved=house,
            strength_score=weighted_score,
            description=description,
            rationale=rationale
        )

    WEIGHTS = {
        "NATAL_PROMISE": 0.40, # Primary foundation
        "SECONDARY_PROMISE": 0.05, # Supporting placements
        "DASHA_ACTIVATION": 0.20, # Timing - Life period (Antar)
        "DASHA_FOUNDATION": 0.03, # Timing - Life period (Maha)
        "TRANSIT_TRIGGER": 0.15, # Timing - Current sky
        "DIVISIONAL_CONFIRM": 0.10, # Soul/Action confirmation
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
        # Score is 0-100, normalize to weighted impact (Magnitude based)
        abs_score = min(100.0, abs(score))
        weighted_score = (abs_score / 100.0) * weight

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

        # 1. Higher-level groups for independence audit (V3.12)
        LAYER_GROUPS = {
            "NATAL_PROMISE": "PROMISE",
            "SECONDARY_PROMISE": "PROMISE",
            "DASHA_ACTIVATION": "DASHA",
            "DASHA_FOUNDATION": "DASHA",
            "TRANSIT_TRIGGER": "TRANSIT",
            "DIVISIONAL_CONFIRM": "VARGA",
            "YOGA_SUPPORT": "NATAL_OTHER",
            "ASPECT_SUPPORT": "NATAL_OTHER",
            "PLANETARY_STRENGTH": "NATAL_OTHER"
        }

        # 2. Group evidence by Layer Group to prevent "Node Inflation"
        group_contributions = {}
        unique_anchors = set()

        for e in evidence:
            group = LAYER_GROUPS.get(e.source, "OTHER")
            if group not in group_contributions:
                group_contributions[group] = []
            group_contributions[group].append(e.strength_score)

            # Anchor is Planet or House involved
            anchor = e.planet_involved or f"H{e.house_involved}" if e.house_involved else e.source
            if e.strength_score > 0:
                unique_anchors.add(anchor)

        # 3. Calculate Confluence (Positive factors)
        # Take the maximum contribution for each GROUP to ensure independence
        total_potential = 0.0
        unique_layer_groups = set()
        for group, scores in group_contributions.items():
            pos_scores = [s for s in scores if s > 0]
            if pos_scores:
                m_score = max(pos_scores)
                total_potential += m_score
                # V3.12: Hardened Layer Counting - Only count as a "Layer" if significant
                if m_score >= 0.08: # Min weighted impact to count as a major layer
                    unique_layer_groups.add(group)

        # 4. Calculate Contradiction (Negative factors)
        total_friction = 0.0
        for group, scores in group_contributions.items():
            neg_scores = [s for s in scores if s < 0]
            if neg_scores:
                total_friction += min(neg_scores) # Most negative per group

        # 5. Final Composite Score
        composite_score = total_potential + total_friction

        # 6. Evidence Diversity Bonus (V3.12)
        # Reward convergence of PROMISE + DASHA + (TRANSIT or VARGA)
        diversity_bonus = 0.0
        if "PROMISE" in unique_layer_groups and "DASHA" in unique_layer_groups:
            if "TRANSIT" in unique_layer_groups or "VARGA" in unique_layer_groups:
                diversity_bonus = 0.12 # Increased for Recall recovery

        composite_score += diversity_bonus

        # 7. State Determination Model
        tw = timing_window or {"phase": "SCANNING", "description": "Analyzing triggers..."}
        phase = tw.get("phase")

        is_peak = phase == "PEAK_MANIFESTATION"
        is_active = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

        # 8. Quality Metric
        density_bonus = min(0.15, len(evidence) * 0.02)
        anchor_diversity_bonus = min(0.2, len(unique_anchors) * 0.05)
        layer_diversity_bonus = min(0.15, len(unique_layer_groups) * 0.04)

        q_score = (composite_score * 0.4) + density_bonus + anchor_diversity_bonus + layer_diversity_bonus - abs(total_friction)
        q_score = round(max(0, min(1, q_score)) * 100, 2)

        # 9. Scoring Gates (V3.12 Precision Recovery)
        # PEAK requires high score, peak timing, and full convergence (4+ groups)
        if composite_score >= 0.65 and is_peak and q_score >= 52 and len(unique_layer_groups) >= 4:
             strength = "PEAK"
             confidence = "EXTREME"
        # ACTIVE requires independent layers convergence
        elif composite_score >= 0.32 and is_active and q_score >= 30:
            has_promise = "PROMISE" in unique_layer_groups
            has_dasha = "DASHA" in unique_layer_groups
            has_transit = "TRANSIT" in unique_layer_groups
            has_varga = "VARGA" in unique_layer_groups

            layers_count = len(unique_layer_groups)

            # Paths to ACTIVE:
            if layers_count >= 3 and has_promise and (has_dasha or has_transit):
                 strength = "ACTIVE"
                 confidence = "HIGH"
            elif has_dasha and has_transit and q_score >= 48:
                 strength = "ACTIVE" # Timing-led trigger
                 confidence = "HIGH"
            elif has_promise and has_dasha and has_varga:
                 strength = "ACTIVE" # Soul-path confirm
                 confidence = "HIGH"
            elif has_promise and has_transit and q_score >= 50:
                 strength = "ACTIVE" # Sudden breakthrough
                 confidence = "HIGH"
            else:
                strength = "WATCH"
                confidence = "MEDIUM"
        # WATCH is more inclusive
        elif composite_score >= 0.30 or (composite_score >= 0.20 and is_active):
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
