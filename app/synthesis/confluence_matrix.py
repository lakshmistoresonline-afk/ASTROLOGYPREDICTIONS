"""
Multi-Engine Predictive Confluence Matrix & Contradiction Resolution (Module 7 - Part 4).
Calculates Predictive Confluence Score (PCS):
PCS = 0.30(S_KP) + 0.25(S_Parashari) + 0.20(S_BNN) + 0.15(S_Jaimini) + 0.10(S_Prashna)
Enforces KP Hard Lock (KP Cusp Sub-Lord negating promise sets status to BLOCKED / DELAYED).
"""
from typing import Dict, Any, List

class PredictiveConfluenceMatrix:
    """
    Multi-Engine Predictive Confluence Matrix (PCS).
    """

    @staticmethod
    def calculate_pcs_score(
        s_kp: float,        # 0.0 to 1.0 (KP Sub-Lord Promise)
        s_parashari: float, # 0.0 to 1.0 (Vimshottari + Vargas)
        s_bnn: float,       # 0.0 to 1.0 (Bhrigu Nandi Nadi Linkages)
        s_jaimini: float,   # 0.0 to 1.0 (Jaimini Chara Dasha)
        s_prashna: float,   # 0.0 to 1.0 (Prashna Horary Seed)
        kp_promise_favorable: bool = True
    ) -> Dict[str, Any]:
        """
        Calculates Predictive Confluence Score (PCS) and enforces KP Hard Lock.
        """
        raw_pcs = (
            (0.30 * s_kp) +
            (0.25 * s_parashari) +
            (0.20 * s_bnn) +
            (0.15 * s_jaimini) +
            (0.10 * s_prashna)
        ) * 100.0

        raw_pcs = round(min(100.0, max(0.0, raw_pcs)), 2)

        # KP Hard Lock Rule:
        # If KP Cusp Sub-Lord negates primary house promise, set status to BLOCKED / DELAYED
        if not kp_promise_favorable:
            event_status = "BLOCKED / DELAYED"
            final_pcs = min(42.0, raw_pcs * 0.5)
            contradiction_resolved = True
            rule_applied = "KP_HARD_LOCK_SUB_LORD_NEGATION"
        else:
            final_pcs = raw_pcs
            contradiction_resolved = False
            rule_applied = "MULTI_SYSTEM_CONFLUENCE_CONFIRMED"
            if final_pcs >= 78.0:
                event_status = "HIGH PROBABILITY / VERIFIED"
            elif final_pcs >= 50.0:
                event_status = "MODERATE PROBABILITY"
            else:
                event_status = "LOW_LATENT_SIGNAL"

        return {
            "predictive_confluence_score_pcs": round(final_pcs, 2),
            "raw_pcs": raw_pcs,
            "event_status": event_status,
            "kp_hard_lock_active": not kp_promise_favorable,
            "contradiction_resolved": contradiction_resolved,
            "rule_applied": rule_applied,
            "system_weights_breakdown": {
                "kp_weight": round(0.30 * s_kp * 100, 2),
                "parashari_weight": round(0.25 * s_parashari * 100, 2),
                "bnn_weight": round(0.20 * s_bnn * 100, 2),
                "jaimini_weight": round(0.15 * s_jaimini * 100, 2),
                "prashna_weight": round(0.10 * s_prashna * 100, 2)
            }
        }

predictive_confluence_matrix = PredictiveConfluenceMatrix()
