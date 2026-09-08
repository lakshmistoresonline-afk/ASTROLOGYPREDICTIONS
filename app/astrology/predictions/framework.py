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
    V2 Pro Intelligence Engine (V3.22).
    Implements Hierarchical Confluence with V3.15 Frozen Logic.
    """

    ENGINE_VERSION = "V3.22"

    WEIGHTS = {
        "NATAL_PROMISE": 0.35,
        "SECONDARY_PROMISE": 0.05,
        "DASHA_ACTIVATION": 0.25,
        "DASHA_FOUNDATION": 0.05,
        "TRANSIT_TRIGGER": 0.15,
        "DIVISIONAL_CONFIRM": 0.10,
        "YOGA_SUPPORT": 0.05,
        "PLANETARY_STRENGTH": 0.05,
        "CONFLICTS": -0.40
    }

    @staticmethod
    def create_evidence(level: str, description: str, score: float,
                        group: str = "PRIMARY", planet: str = None,
                        house: int = None, rationale: str = None,
                        evidence_type: str = "SUPPORTING",
                        source_layer: str = "NATAL",
                        independence_group: str = None) -> CorroborationEvidence:

        weight = CorroborationEngine.WEIGHTS.get(level, 0.0)
        abs_score = min(100.0, abs(score))
        weighted_score = (abs_score / 100.0) * weight

        return CorroborationEvidence(
            source=level,
            level=group,
            planet_involved=planet,
            house_involved=house,
            strength_score=weighted_score,
            description=description,
            rationale=rationale,
            evidence_type=evidence_type,
            source_layer=source_layer,
            independence_group=independence_group
        )

    @staticmethod
    def resolve_node_proxy(planet_name: str, chart: CanonicalChart) -> List[str]:
        if planet_name not in ["Rahu", "Ketu"]: return [planet_name]
        proxies = []
        p_info = chart.planets.get(planet_name)
        if not p_info: return [planet_name]
        proxies.append(p_info.dispositor)
        for other_name, other_p in chart.planets.items():
            if other_name == planet_name: continue
            if other_p.rashi == p_info.rashi: proxies.append(other_name)
        return list(set(proxies))

    @staticmethod
    def audit_dasha_activation(dasha_data: Dict[str, Any], chart: CanonicalChart,
                               relevant_lords: List[str], domain_label: str) -> List[CorroborationEvidence]:
        evidence = []
        antar_lord = dasha_data.get("current_antar", {}).get("lord")
        maha_lord = dasha_data.get("current_maha", {}).get("lord")
        if not antar_lord: return []
        if antar_lord in relevant_lords:
            evidence.append(CorroborationEngine.create_evidence("DASHA_ACTIVATION", f"TEMPORAL ACTIVATION: Period ruled by {antar_lord} triggers major {domain_label} themes.", 90.0, group="PRIMARY"))
        else:
            proxies = CorroborationEngine.resolve_node_proxy(antar_lord, chart)
            for p in proxies:
                if p in relevant_lords and p != antar_lord:
                    evidence.append(CorroborationEngine.create_evidence("DASHA_ACTIVATION", f"NODE PROXY: {antar_lord} acts through {p} (Relevant Lord for {domain_label}).", 50.0, group="SECONDARY"))
                    break
        if maha_lord in relevant_lords:
             evidence.append(CorroborationEngine.create_evidence("DASHA_ACTIVATION", f"MAHA ACTIVATION: Major life-cycle ruled by {maha_lord} provides strong support.", 70.0, group="PRIMARY"))
        else:
             evidence.append(CorroborationEngine.create_evidence("DASHA_FOUNDATION", f"DASHA FOUNDATION: Major cycle ruled by {maha_lord} provides background support.", 30.0, group="SECONDARY"))
        return evidence

    @staticmethod
    def synthesize(domain: str, promise_level: str, evidence: List[CorroborationEvidence],
                    summary_template: str, timing_window: Dict[str, Any] = None,
                    event_type: str = None, event_magnitude: str = "MODERATE",
                    what_may_develop: str = None) -> DomainPrediction:

        LAYER_GROUPS = {"NATAL_PROMISE": "PROMISE", "SECONDARY_PROMISE": "PROMISE", "DASHA_ACTIVATION": "DASHA", "DASHA_FOUNDATION": "DASHA", "TRANSIT_TRIGGER": "TRANSIT", "DIVISIONAL_CONFIRM": "VARGA", "YOGA_SUPPORT": "NATAL_OTHER", "PLANETARY_STRENGTH": "NATAL_OTHER"}
        group_contributions = {}
        unique_anchors = set()
        for e in evidence:
            group = LAYER_GROUPS.get(e.source, "OTHER")
            if group not in group_contributions: group_contributions[group] = []
            group_contributions[group].append(e.strength_score)
            anchor = e.planet_involved or f"H{e.house_involved}" if e.house_involved else e.source
            if e.strength_score > 0: unique_anchors.add(anchor)

        total_potential = 0.0
        unique_confirmation_layers = 0
        major_groups = set()
        for group, scores in group_contributions.items():
            pos_scores = [s for s in scores if s > 0]
            if pos_scores:
                m_score = max(pos_scores)
                total_potential += m_score
                if m_score >= 0.05:
                    unique_confirmation_layers += 1
                    major_groups.add(group)

        total_friction = sum([min(s for s in scores if s < 0) for scores in group_contributions.values() if any(s < 0 for s in scores)])
        composite_score = total_potential + total_friction
        if "PROMISE" in major_groups and "DASHA" in major_groups and "TRANSIT" in major_groups: composite_score += 0.10

        tw = timing_window or {"phase": "SCANNING", "proximity_weight": 0.0}
        phase = tw.get("phase")
        is_peak = phase == "PEAK_MANIFESTATION"
        is_active = phase in ["NEAR_TERM_ACTIVE", "PEAK_ACTIVE", "PEAK_MANIFESTATION"]

        density_bonus = min(0.2, len(evidence) * 0.03)
        anchor_diversity_bonus = min(0.2, len(unique_anchors) * 0.04)
        friction_penalty = abs(total_friction) * 1.0
        q_score = round(max(0, min(1, (composite_score * 0.4) + density_bonus + anchor_diversity_bonus - friction_penalty)) * 100, 2)

        sources = {e.source for e in evidence if e.strength_score > 0}
        has_antar = "DASHA_ACTIVATION" in sources
        has_primary_antar = any(e.source == "DASHA_ACTIVATION" and e.level == "PRIMARY" for e in evidence if e.strength_score > 0)
        has_primary_natal = "NATAL_PROMISE" in sources
        has_transit_layer = "TRANSIT_TRIGGER" in sources

        gate_score = 0.55
        gate_q = 52
        temporal_threshold = 0.55
        if domain in ["Career & Authority", "Education & Knowledge", "Fame & Reputation"]:
             gate_score = 0.38
             gate_q = 44
             temporal_threshold = 0.35
             if domain == "Fame & Reputation": gate_q = 32

        is_active_hardened = is_active
        if phase == "NEAR_TERM_ACTIVE" and tw.get("proximity_weight", 0) < temporal_threshold:
             is_active_hardened = False

        strength, confidence, status_label = "BACKGROUND", "LOW", "DORMANT"
        if composite_score >= 0.78 and is_peak and q_score >= 62 and len(unique_anchors) >= 3:
            if has_primary_natal and (has_antar or has_transit_layer):
                strength, confidence, status_label = "PEAK", "EXTREME", "PEAK"
            else:
                strength, confidence, status_label = "ACTIVE", "HIGH", "ACTIVE"
        elif composite_score >= gate_score and is_active_hardened and q_score >= gate_q and unique_confirmation_layers >= 2:
            if has_primary_natal and has_primary_antar and has_transit_layer:
                strength, confidence, status_label = "ACTIVE", "HIGH", "ACTIVE"
            elif has_primary_natal and (has_antar or has_transit_layer) and composite_score >= 0.58:
                strength, confidence, status_label = "ACTIVE", "HIGH", "ACTIVE"
            elif has_antar and has_transit_layer and q_score >= 50:
                 if has_primary_antar or composite_score >= 0.65:
                      strength, confidence, status_label = "ACTIVE", "HIGH", "ACTIVE"
                 else:
                      strength, confidence, status_label = "WATCH", "MEDIUM", "BUILDING"
            elif unique_confirmation_layers >= 3 and composite_score >= 0.52:
                 strength, confidence, status_label = "ACTIVE", "HIGH", "ACTIVE"
            else:
                strength, confidence, status_label = "WATCH", "MEDIUM", "BUILDING"
        elif composite_score >= 0.15 or (composite_score >= 0.05 and is_active):
            strength, confidence, status_label = "WATCH", "MEDIUM", "BUILDING"

        from .taxonomy import EVENT_TAXONOMY, MANIFESTATION_GUIDE
        taxonomy = EVENT_TAXONOMY.get(domain, ["DEVELOPMENT"])
        inferred_event = event_type or taxonomy[0]
        manifestation_hint = MANIFESTATION_GUIDE.get(inferred_event, f"Significant activation in {domain} sector.")

        from .narrative_composer import narrative_composer
        triggers = [e.planet_involved for e in evidence if e.source == "TRANSIT_TRIGGER" and e.planet_involved]
        plain_why = narrative_composer.compose_why_now(domain, inferred_event, triggers, len(evidence))

        final_summary = f"The current signal strength for {domain.lower()} is {int(composite_score*100)}/100. {plain_why}"

        # Determine representation magnitude (V3.22 Roadmap logic)
        rep_magnitude = "LOW"
        if composite_score >= 0.85: rep_magnitude = "MAJOR"
        elif composite_score >= 0.65: rep_magnitude = "SIGNIFICANT"
        elif composite_score >= 0.40: rep_magnitude = "MODERATE"

        return DomainPrediction(
            domain=domain,
            headline=f"{status_label}: {inferred_event.replace('_', ' ')}",
            score=round(composite_score * 100, 2),
            quality_score=q_score,
            confidence=confidence,
            prediction_strength=strength,
            event_type=inferred_event,
            event_magnitude=rep_magnitude,
            what_may_develop=what_may_develop,
            summary=final_summary,
            evidence_chain=evidence,
            supporting_factors=[e.description for e in evidence if e.strength_score > 0],
            contradicting_factors=[e.description for e in evidence if e.strength_score < 0],
            timing_window=tw,
            manifestations=[manifestation_hint],
            confirmation_criteria=[f"Observable shift in {domain}.", "Peak intensity match.", "Material evidence."],
            practical_actions=["Monitor peak triggers for alignment."],
            limitations="Signal scores represent internal strength, not statistical probability. Probability is NOT AVAILABLE."
        )
