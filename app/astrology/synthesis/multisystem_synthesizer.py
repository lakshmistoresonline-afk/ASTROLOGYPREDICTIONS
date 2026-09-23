"""
Multi-System Cross-Verification Engine (Module 8 - Task 8.2).
Synthesizes weighted scores across 4 independent systems:
1. Vedic Vimshottari Dasha + Transit Kakshya: 40% weight
2. Jaimini Chara Dasha & Karaka Interlocking: 25% weight
3. Tajika Varshaphal & Sahams: 20% weight
4. BaZi Five-Element Balance Shifts: 15% weight
Outputs a unified Confluence Index Score (0-100%).
"""
from typing import Dict, Any, List

class MultiSystemSynthesizer:
    """
    Weighted Synthesis Matrix combining Vedic, Jaimini, Tajika, and BaZi systems.
    """

    WEIGHT_VEDIC = 0.40
    WEIGHT_JAIMINI = 0.25
    WEIGHT_TAJIKA = 0.20
    WEIGHT_BAZI = 0.15

    @staticmethod
    def calculate_confluence_index(
        vedic_score: float,    # 0.0 to 1.0
        jaimini_score: float,  # 0.0 to 1.0
        tajika_score: float,   # 0.0 to 1.0
        bazi_score: float      # 0.0 to 1.0
    ) -> Dict[str, Any]:
        """
        Calculates unified Confluence Index Score (0-100%).
        """
        v_contrib = vedic_score * MultiSystemSynthesizer.WEIGHT_VEDIC
        j_contrib = jaimini_score * MultiSystemSynthesizer.WEIGHT_JAIMINI
        t_contrib = tajika_score * MultiSystemSynthesizer.WEIGHT_TAJIKA
        b_contrib = bazi_score * MultiSystemSynthesizer.WEIGHT_BAZI

        total_index = (v_contrib + j_contrib + t_contrib + b_contrib) * 100.0
        total_index = round(min(100.0, max(0.0, total_index)), 2)

        # Confidence Grade
        if total_index >= 85.0:
            tier = "TOP_TIER_HIGH_CONFLUENCE"
            narrative_mode = "CONFIRMED_MULTISYSTEM_PEAK"
        elif total_index >= 60.0:
            tier = "STRONG_CONFLUENCE"
            narrative_mode = "STABLE_ALIGNMENT"
        elif total_index >= 30.0:
            tier = "MODERATE_ALIGNMENT"
            narrative_mode = "CONDITIONAL_MANIFESTATION"
        else:
            tier = "LOW_LATENT_SIGNAL"
            narrative_mode = "BACKGROUND_FRICTION"

        return {
            "confluence_index_score": total_index,
            "confluence_tier": tier,
            "narrative_mode": narrative_mode,
            "weighted_breakdown": {
                "vedic_kakshya_contribution": round(v_contrib * 100, 2),
                "jaimini_karaka_contribution": round(j_contrib * 100, 2),
                "tajika_sahams_contribution": round(t_contrib * 100, 2),
                "bazi_element_contribution": round(b_contrib * 100, 2)
            }
        }

multisystem_synthesizer = MultiSystemSynthesizer()
