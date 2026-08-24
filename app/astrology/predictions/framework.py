from typing import List, Dict, Any, Optional
from ..core.models import PredictionFactor, DomainPrediction, CanonicalChart
from ..strength.aspects import get_graha_drishti

def _get(obj, attr, default=None):
    if hasattr(obj, attr):
        val = getattr(obj, attr)
        return val() if callable(val) else val
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return default

def are_associated(p1_name: str, p2_name: str, planets: Dict[str, Any]) -> bool:
    """Check if two planets are associated by conjunction or mutual aspect."""
    p1 = planets.get(p1_name)
    p2 = planets.get(p2_name)
    if not p1 or not p2: return False

    r1 = _get(p1, "rashi")
    r2 = _get(p2, "rashi")

    # Conjunction
    if r1 == r2: return True

    # Mutual Aspect
    p1_aspects = get_graha_drishti(p1_name, r1)
    p2_aspects = get_graha_drishti(p2_name, r2)

    if r2 in p1_aspects and r1 in p2_aspects:
        return True
    return False

class EvidenceEngine:
    """Standardizes astrological facts into evidence objects."""

    @staticmethod
    def create_factor(name: str, type: str, direction: str, weight: float, explanation: str) -> PredictionFactor:
        return PredictionFactor(
            factor=name,
            type=type,
            direction=direction,
            weight=weight,
            explanation=explanation
        )

class ContradictionEngine:
    """Detects and analyzes conflicting astrological signals."""

    @staticmethod
    def analyze(factors: List[PredictionFactor]) -> List[str]:
        contradictions = []
        positive_factors = [f for f in factors if f.direction == "positive"]
        negative_factors = [f for f in factors if f.direction == "negative"]

        if positive_factors and negative_factors:
            # Check for strong specific contradictions
            # 1. House vs. Lord
            for pos in positive_factors:
                for neg in negative_factors:
                    if pos.type == "house" and neg.type == "lord" and "House" in pos.explanation and "Lord" in neg.explanation:
                        contradictions.append(f"The primary house shows promise, but its ruling planet ({neg.factor}) is under pressure, indicating effort required to manifest results.")
                    if pos.type == "lord" and neg.type == "house" and "Lord" in pos.explanation and "House" in neg.explanation:
                        contradictions.append(f"A strong ruling planet suggests potential, yet the house environment itself is afflicted, leading to mixed experiences.")

            # 2. Varga contradiction
            varga_pos = [f for f in positive_factors if f.type == "varga"]
            varga_neg = [f for f in negative_factors if f.type == "varga"]
            d1_pos = [f for f in positive_factors if f.type in ["house", "lord"]]
            d1_neg = [f for f in negative_factors if f.type in ["house", "lord"]]

            if d1_pos and varga_neg:
                contradictions.append("Strong natal potential (D1) is hindered by unfavorable divisional chart (Varga) indicators, suggesting fruit may be delayed or diminished.")
            if d1_neg and varga_pos:
                contradictions.append("Natal challenges (D1) are significantly mitigated by strong divisional chart support, indicating eventual success after initial struggle.")

            # 3. Dasha vs. Transit
            dasha_pos = [f for f in positive_factors if f.type == "dasha"]
            dasha_neg = [f for f in negative_factors if f.type == "dasha"]
            transit_pos = [f for f in positive_factors if f.type == "transit"]
            transit_neg = [f for f in negative_factors if f.type == "transit"]

            if dasha_pos and transit_neg:
                contradictions.append("A supportive Dasha period is currently challenged by unfavorable transits, indicating a temporary phase of frustration despite long-term growth.")
            if dasha_neg and transit_pos:
                contradictions.append("Favorable transits are providing immediate relief, but the underlying Dasha period remains unsupportive for major permanent gains.")

            # 4. Strength contradiction
            strength_neg = any(f.type == "strength" and f.direction == "negative" for f in factors)
            if d1_pos and strength_neg:
                contradictions.append("Well-placed planets lack inherent structural strength (Shadbala), meaning opportunities may arise but lack the power to fully materialize.")

        return list(set(contradictions))

def cross_validate_with_specialized(chart: CanonicalChart, domain_name: str, base_factors: List[PredictionFactor]) -> List[PredictionFactor]:
    """
    Apply Tajika, Nadi, and Jaimini Rashi Drishti to refine the prediction.
    """
    refined = list(base_factors)

    # 1. Nadi Cross-validation (Planet-to-Planet connections)
    # Example: If Career is being checked (Sun/Saturn), check their Nadi links
    if domain_name == "Career":
        sat_nadi = chart.nadi_connections.get("Saturn", [])
        sun_nadi = chart.nadi_connections.get("Sun", [])
        if "Jupiter" in sat_nadi or "Jupiter" in sun_nadi:
            refined.append(EvidenceEngine.create_factor("Nadi Link (Career-Jup)", "yoga", "positive", 15, "Jupiter's Nadi link to career planets indicates significant expansion and professional ethics."))

    # 2. Tajika Ithasala (Applying aspects)
    # Powerful for 'Immediate' results or current year potential
    for ty in chart.tajika_yogas:
        if ty["status"] == "Applying" and ty["strength"] == "STRONG":
            # Check if participating planets are relevant to domain
            # (Simplified for now: any strong Ithasala is a general boost)
            if domain_name in ["Career", "Finance", "Marriage"]:
                refined.append(EvidenceEngine.create_factor("Tajika Ithasala", "yoga", "positive", 10, f"Positive applying aspect ({ty['name']}) facilitates swift manifestation of results."))

    # 3. Rashi Drishti (Jaimini)
    # Check if any benefic rashi aspects the primary house
    benefics = ["Jupiter", "Venus", "Moon", "Mercury"]
    # Map domain to house
    house_map = {"Career": 10, "Finance": 2, "Marriage": 7, "Health": 1}
    h_idx = house_map.get(domain_name)
    if h_idx is not None and chart.asc_rashi is not None:
        target_rashi = (chart.asc_rashi + h_idx - 1) % 12
        for r_idx, aspecting in chart.rashi_drishti.items():
            if target_rashi in aspecting:
                # Sign at r_idx aspects target house. Is there a benefic there?
                for p_name, p_info in chart.planets.items():
                    if p_info.rashi == r_idx and p_name in benefics:
                        refined.append(EvidenceEngine.create_factor("Rashi Drishti", "yoga", "positive", 8, f"Target house receives supportive Jaimini aspect from {p_name} in rashi {r_idx}."))

    # 4. Sudarshana Chakra Resonance
    # If the house is strong from all 3 points (Lagna, Moon, Sun)
    s_h_idx = house_map.get(domain_name)
    if s_h_idx:
        s_chakra = chart.sudarshana_chakra.get(s_h_idx)
        if s_chakra and s_chakra["resonance"] == "HIGH":
            refined.append(EvidenceEngine.create_factor("Sudarshana Resonance", "house", "positive", 20, "This domain is strong from the perspective of the Body, Mind, and Soul (Sudarshana), indicating a definitive karmic promise."))

    # 5. Sensitive Points (Bhrigu Bindu / Khara)
    bb_lon = chart.sensitive_points.get("Bhrigu Bindu")
    if bb_lon is not None:
        bb_rashi = int(bb_lon // 30)
        # Check if any planet aspects Bhrigu Bindu (simplified)
        for p_name, p_info in chart.planets.items():
            if p_info.rashi == bb_rashi:
                refined.append(EvidenceEngine.create_factor("Destiny Trigger", "planet", "positive", 12, f"Planet {p_name} sits on your Bhrigu Bindu (Destiny Point), acting as a major karmic catalyst."))

    # 6. KP Significators
    # Level A & B are strongest
    h_num = house_map.get(domain_name)
    if h_num is not None:
        sigs = chart.kp_significators.get(h_num, {})
        strong_sigs = sigs.get("A", []) + sigs.get("B", [])
        for s in strong_sigs:
            # Check if this significator is also a domain planet
            if s in ["Jupiter", "Venus", "Mercury"]:
                refined.append(EvidenceEngine.create_factor("KP Support", "planet", "positive", 15, f"KP System confirms {s} as a primary significator for {domain_name}."))

    # 7. Bhrigu Chakra Paddhati (BCP) Activation
    bcp = chart.bcp_activation
    if bcp and h_num is not None and bcp.get("active_house") == h_num:
        refined.append(EvidenceEngine.create_factor("BCP Activation", "house", "positive", 25, f"Bhrigu Chakra Paddhati (BCP) confirms this house is currently ACTIVE for your {bcp['age']}th year, bringing matters of {domain_name} to the forefront."))

    # 8. Karakamsha / Swamsha Support
    ks = chart.karakamsha_swamsha
    if ks and h_num is not None and chart.asc_rashi is not None:
        # Check if domain house relative to Karakamsha is strong
        k_rashi = ks.get("Karakamsha")
        if k_rashi is not None:
            target_rashi = (chart.asc_rashi + h_num - 1) % 12
            rel_h = (target_rashi - k_rashi + 12) % 12 + 1
            if rel_h in [1, 4, 7, 10, 5, 9]:
                refined.append(EvidenceEngine.create_factor("Soul Strength (Karakamsha)", "yoga", "positive", 12, f"This life area is auspiciously placed (H{rel_h}) from your Atmakaraka's Navamsha seat, ensuring soul-level fulfillment."))

    # 9. Panchadha Maitri (Planetary Relationships)
    # Check relationship between domain lord and Lagna Lord
    l1_name = chart.house_lords.get(1)
    if h_num is not None:
        d_lord_name = chart.house_lords.get(h_num)
        if l1_name and d_lord_name and l1_name != d_lord_name:
            from ..strength.friendship import get_compound_friendship
            # Ensure planets exist
            if l1_name in chart.planets and d_lord_name in chart.planets:
                rel = get_compound_friendship(l1_name, d_lord_name, chart.planets[l1_name].house, chart.planets[d_lord_name].house)
                if rel in ["Great Friend", "Friend"]:
                     refined.append(EvidenceEngine.create_factor("Planetary Relationship", "lord", "positive", 10, f"The lord of this domain ({d_lord_name}) is a {rel} of your Lagna Lord ({l1_name}), indicating ease of manifestation."))
                elif rel in ["Enemy", "Great Enemy"]:
                     refined.append(EvidenceEngine.create_factor("Planetary Relationship", "lord", "negative", 10, f"The lord of this domain ({d_lord_name}) is an {rel} of your Lagna Lord ({l1_name}), suggesting internal conflict in achieving results."))

    return refined

class ConfidenceEngine:
    """Calculates overall confidence score for a prediction."""

    @staticmethod
    def calculate(factors: List[PredictionFactor], varga_confirmation: bool = False, dasha_confirmation: bool = False, transit_confirmation: bool = False) -> str:
        score = 0

        # 1. Depth of evidence (0-4 points)
        if len(factors) >= 10:
            score += 4
        elif len(factors) >= 7:
            score += 3
        elif len(factors) >= 4:
            score += 2
        elif len(factors) >= 2:
            score += 1

        # 2. Cross-chart verification (0-6 points)
        if varga_confirmation:
            score += 2
        if dasha_confirmation:
            score += 2
        if transit_confirmation:
            score += 2

        # 3. Consistency (Penalty for heavy contradiction)
        positive_factors = [f for f in factors if f.direction == "positive"]
        negative_factors = [f for f in factors if f.direction == "negative"]
        if positive_factors and negative_factors:
            ratio = min(len(positive_factors), len(negative_factors)) / max(len(positive_factors), len(negative_factors))
            if ratio > 0.5: # Heavy contradiction
                score -= 1

        if score >= 7:
            return "VERY HIGH"
        if score >= 5:
            return "HIGH"
        if score >= 3:
            return "MEDIUM"
        return "LOW"

def analyze_domain(
    domain_name: str,
    factors: List[PredictionFactor],
    summary_template: str,
    varga_data: Optional[Dict[str, Any]] = None,
    dasha_data: Optional[Dict[str, Any]] = None,
    transit_data: Optional[Dict[str, Any]] = None,
    chart: Optional[CanonicalChart] = None # Added chart for cross-validation
) -> DomainPrediction:
    """Unified helper to build a DomainPrediction."""

    # Cross-validate with specialized systems if chart is provided
    if chart:
        factors = cross_validate_with_specialized(chart, domain_name, factors)

    pos_factors = [f for f in factors if f.direction == "positive"]
    neg_factors = [f for f in factors if f.direction == "negative"]

    # Calculate score (base 50)
    score = 50.0
    for f in factors:
        # Refine weight based on Avastha if it's a planet/lord factor
        w = f.weight
        if chart and f.type in ["planet", "lord"]:
            p_info = chart.planets.get(f.factor.split(' ')[0]) # Heuristic to get planet name
            if p_info:
                w *= p_info.avastha_weight

        if f.direction == "positive":
            score += w
        else:
            score -= w

    score = max(0.0, min(100.0, score))

    contradictions = ContradictionEngine.analyze(factors)

    # Check for confirmations
    v_conf = varga_data.get("confirmed", False) if varga_data else False
    d_conf = dasha_data.get("confirmed", False) if dasha_data else False
    t_conf = transit_data.get("confirmed", False) if transit_data else False

    confidence = ConfidenceEngine.calculate(factors, v_conf, d_conf, t_conf)

    evidence_strings = [f"{'✓' if f.direction == 'positive' else '⚠'} {f.explanation}" for f in factors]

    return DomainPrediction(
        domain=domain_name,
        score=score,
        confidence=confidence,
        summary=summary_template.format(score=score, confidence=confidence),
        evidence=evidence_strings,
        positive_factors=pos_factors,
        negative_factors=neg_factors,
        contradictions=contradictions
    )
