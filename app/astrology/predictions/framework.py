from typing import List, Dict, Any, Optional
from ..core.models import PredictionFactor, DomainPrediction, CanonicalChart
from ..strength.aspects import get_graha_drishti
from ..remedies.engine import REMEDIES_DATABASE

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
    if domain_name == "Career":
        sat_nadi = chart.nadi_connections.get("Saturn", [])
        sun_nadi = chart.nadi_connections.get("Sun", [])
        if "Jupiter" in sat_nadi or "Jupiter" in sun_nadi:
            refined.append(EvidenceEngine.create_factor("Life Expansion", "yoga", "positive", 15, "A special planetary link suggests ethical growth and significant expansion in your professional sphere."))

    # 2. Tajika Ithasala (Applying aspects)
    for ty in chart.tajika_yogas:
        if ty["status"] == "Applying" and ty["strength"] == "STRONG":
            if domain_name in ["Career", "Finance", "Marriage"]:
                refined.append(EvidenceEngine.create_factor("Upcoming Opportunity", "yoga", "positive", 10, "A strong celestial alignment is currently forming, facilitating a swift manifestation of results."))

    # 3. Rashi Drishti (Jaimini)
    benefics = ["Jupiter", "Venus", "Moon", "Mercury"]
    house_map = {"Career": 10, "Finance": 2, "Marriage": 7, "Health": 1}
    h_idx = house_map.get(domain_name)
    if h_idx is not None and chart.asc_rashi is not None:
        target_rashi = (chart.asc_rashi + h_idx - 1) % 12
        for r_idx, aspecting in chart.rashi_drishti.items():
            if target_rashi in aspecting:
                for p_name, p_info in chart.planets.items():
                    if p_info.rashi == r_idx and p_name in benefics:
                        refined.append(EvidenceEngine.create_factor("Benefic Support", "yoga", "positive", 8, f"This sector receives supportive energy from {p_name}, easing the path to success."))

    # 4. Sudarshana Chakra Resonance
    s_h_idx = house_map.get(domain_name)
    if s_h_idx:
        s_chakra = chart.sudarshana_chakra.get(s_h_idx)
        if s_chakra and s_chakra["resonance"] == "HIGH":
            refined.append(EvidenceEngine.create_factor("Unified Alignment", "house", "positive", 20, "This life area is strongly supported across multiple layers of your blueprint, indicating a definitive promise of fulfillment."))

    # 5. Sensitive Points (Bhrigu Bindu)
    bb_lon = chart.sensitive_points.get("Bhrigu Bindu")
    if bb_lon is not None:
        bb_rashi = int(bb_lon // 30)
        for p_name, p_info in chart.planets.items():
            if p_info.rashi == bb_rashi:
                refined.append(EvidenceEngine.create_factor("Destiny Trigger", "planet", "positive", 12, "A key planet is activating a sensitive destiny point in your chart, acting as a major catalyst for change."))

    # 6. KP Significators
    h_num = house_map.get(domain_name)
    if h_num is not None:
        sigs = chart.kp_significators.get(h_num, {})
        strong_sigs = sigs.get("A", []) + sigs.get("B", [])
        for s in strong_sigs:
            if s in ["Jupiter", "Venus", "Mercury"]:
                refined.append(EvidenceEngine.create_factor("Technical Confirmation", "planet", "positive", 15, f"Deep-layered analysis confirms strong planetary support for achieving goals in this area."))

    # 7. Bhrigu Chakra Paddhati (BCP) Activation
    bcp = chart.bcp_activation
    if bcp and h_num is not None and bcp.get("active_house") == h_num:
        refined.append(EvidenceEngine.create_factor("Temporal Focus", "house", "positive", 25, f"Your current age cycle is precisely activating this sector, bringing these specific life matters to the forefront."))

    # 8. Karakamsha / Swamsha Support
    ks = chart.karakamsha_swamsha
    if ks and h_num is not None and chart.asc_rashi is not None:
        k_rashi = ks.get("Karakamsha")
        if k_rashi is not None:
            target_rashi = (chart.asc_rashi + h_num - 1) % 12
            rel_h = (target_rashi - k_rashi + 12) % 12 + 1
            if rel_h in [1, 4, 7, 10, 5, 9]:
                refined.append(EvidenceEngine.create_factor("Soul-Level Fulfillment", "yoga", "positive", 12, "This life area aligns with your deeper soul-path, ensuring lasting personal satisfaction."))

    # 9. Panchadha Maitri (Planetary Relationships)
    l1_name = chart.house_lords.get(1)
    if h_num is not None:
        d_lord_name = chart.house_lords.get(h_num)
        if l1_name and d_lord_name and l1_name != d_lord_name:
            from ..strength.friendship import get_compound_friendship
            if l1_name in chart.planets and d_lord_name in chart.planets:
                rel = get_compound_friendship(l1_name, d_lord_name, chart.planets[l1_name].house, chart.planets[d_lord_name].house)
                if rel in ["Great Friend", "Friend"]:
                     refined.append(EvidenceEngine.create_factor("Natural Flow", "lord", "positive", 10, "The energy governing this domain is in harmony with your core identity, allowing for an easier manifestation of results."))
                elif rel in ["Enemy", "Great Enemy"]:
                     refined.append(EvidenceEngine.create_factor("Internal Friction", "lord", "negative", 10, "There is a slight mismatch between your desires and the energy of this sector, suggesting initial effort is needed."))

    # 11. Ashtakavarga Strength
    if h_num is not None and chart.ashtakavarga:
        target_rashi = (chart.asc_rashi + h_num - 1) % 12
        sav_points = chart.ashtakavarga.get("SAV", [28]*12)[target_rashi]
        if sav_points >= 30:
            refined.append(EvidenceEngine.create_factor("Vitality Boost", "ashtakavarga", "positive", 8, "This sector possesses high vital energy, providing a strong foundation for your efforts."))
        elif sav_points < 25:
            refined.append(EvidenceEngine.create_factor("Energy Maintenance", "ashtakavarga", "negative", 5, "This area may require more conscious energy management to achieve consistent results."))

    # 12. Planetary Avastha Details
    if h_num is not None:
        d_lord_name = chart.house_lords.get(h_num)
        p_info = chart.planets.get(d_lord_name)
        if p_info:
            if "Deept" in p_info.deeptadi_avastha:
                refined.append(EvidenceEngine.create_factor("Radiant Expression", "planet", "positive", 10, "The planetary ruler of this area is in a peak state of radiance, ensuring powerful results."))
            elif "Kopita" in p_info.deeptadi_avastha:
                refined.append(EvidenceEngine.create_factor("Pressure State", "planet", "negative", 10, "The ruler of this domain is currently under pressure, which may lead to impulsive or reactive outcomes."))

    # 13. Functional Obstruction
    for p_name, p_data in chart.planets.items():
        if p_data.house == h_num and p_data.functional_status == "Malefic":
            refined.append(EvidenceEngine.create_factor("Structural Hurdle", "planet", "negative", 8, "A challenging influence in this sector may cause recurring but manageable hurdles."))

    # 14. Planetary War
    for p_name, p_data in chart.planets.items():
        if p_data.is_in_planetary_war and (p_data.house == h_num or p_name == d_lord_name):
             refined.append(EvidenceEngine.create_factor("Energy Struggle", "planet", "negative", 12, "An intense struggle between planetary energies in this sector can cause volatile or unpredictable phases."))

    return refined

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

    # 1. New Details Containers
    varga_conf = []
    adv_details = []

    # Cross-validate with specialized systems if chart is provided
    if chart:
        # Cross-validation can now return structured details
        factors = cross_validate_with_specialized(chart, domain_name, factors)

        # Extract Divisional Details
        v_pos = [f for f in factors if f.type == "varga" and f.direction == "positive"]
        v_neg = [f for f in factors if f.type == "varga" and f.direction == "negative"]
        for v in v_pos: varga_conf.append(f"✓ {v.explanation}")
        for v in v_neg: varga_conf.append(f"⚠ {v.explanation}")

        # Extract Advanced/Yoga Details
        a_factors = [f for f in factors if f.type in ["yoga", "planet"] and "KP" not in f.factor and "BCP" not in f.factor]
        for a in a_factors: adv_details.append(a.explanation)

    pos_factors = [f for f in factors if f.direction == "positive"]
    neg_factors = [f for f in factors if f.direction == "negative"]

    # Calculate score (base 50)
    score = 50.0
    for f in factors:
        # Refine weight based on Avastha if it's a planet/lord factor
        w = f.weight
        if chart and f.type in ["planet", "lord"]:
            p_name = f.factor.split(' ')[0]
            p_info = chart.planets.get(p_name)
            if p_info:
                w *= p_info.avastha_weight

        if f.direction == "positive":
            score += w
        else:
            score -= w

    score = max(0.0, min(100.0, score))

    contradictions = ContradictionEngine.analyze(factors)

    # Check for confirmations
    v_conf_bool = varga_data.get("confirmed", False) if varga_data else bool(v_pos)
    d_conf = dasha_data.get("confirmed", False) if dasha_data else False
    t_conf = transit_data.get("confirmed", False) if transit_data else False

    confidence = ConfidenceEngine.calculate(factors, v_conf_bool, d_conf, t_conf)

    evidence_strings = [f"{'✓' if f.direction == 'positive' else '⚠'} {f.explanation}" for f in factors if f.type not in ["varga"]]

    # Generate Remedies if score is low
    remedies = []
    if score < 60:
        neg_planets = set()
        for f in neg_factors:
            if f.type in ["planet", "lord"]:
                p_name = f.factor.split(' ')[0]
                if p_name in REMEDIES_DATABASE:
                    neg_planets.add(p_name)

        for p in neg_planets:
            db_rem = REMEDIES_DATABASE[p]
            remedies.append({
                "planet": p,
                "mantra": db_rem.get("mantra"),
                "charity": db_rem.get("charity"),
                "lifestyle": db_rem.get("lifestyle")
            })

    # Timing Explanation
    t_exp = "Synchronized cosmic support detected." if d_conf or t_conf else "Requires internal effort; external support is currently neutral."
    if d_conf and t_conf: t_exp = "Peak temporal alignment: long-term and immediate triggers are active."

    return DomainPrediction(
        domain=domain_name,
        score=score,
        confidence=confidence,
        summary=summary_template.format(score=score, confidence=confidence),
        evidence=evidence_strings,
        positive_factors=pos_factors,
        negative_factors=neg_factors,
        contradictions=contradictions,
        remedies=remedies,
        divisional_confirmation=varga_conf,
        advanced_details=adv_details,
        timing_explanation=t_exp
    )
