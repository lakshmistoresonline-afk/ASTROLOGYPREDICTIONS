"""
Automated Contradiction Resolution & Synthesis Matrix (Module 22 - Task 22.3).
Applies hierarchical priority tree to resolve opposing system signals (KP vs Parashari vs Jaimini):
Rule 1: KP Dominance on Event Feasibility (Sub-lord signifying 6/8/12 negates event feasibility -> BLOCKED/DELAYED)
Rule 2: Parashari Dominance on Narrative & Magnitude (Determines overall scale and emotional/physical impact)
Rule 3: Jaimini Confirmation (+25% boost if Chara Dasha and AK/AmK sync)
"""
from typing import Dict, Any, List

class ContradictionResolver:
    """
    Hierarchical Priority Tree resolving opposing signals between KP, Parashari, and Jaimini systems.
    """

    @staticmethod
    def resolve_contradictions(
        kp_favorable: bool,
        parashari_score: float,     # 0.0 to 100.0
        jaimini_activated: bool,
        domain: str,
        event_type: str
    ) -> Dict[str, Any]:
        """
        Outputs a single harmonized prediction verdict and unified narrative string.
        """
        final_score = parashari_score

        # Rule 1: KP Dominance on Event Feasibility
        if not kp_favorable:
            verdict = "BLOCKED / DELAYED"
            # Cap score at 40% if KP Sub-Lord negates feasibility
            final_score = min(40.0, parashari_score * 0.5)
            harmonized_narrative = (
                f"While Parashari indicators show active momentum ({parashari_score:.1f}%), "
                f"KP Sub-Lord significators signify 6th/8th/12th house friction, "
                f"rendering {event_type} temporarily BLOCKED or DELAYED until Sub-Lord transit alignment."
            )
        else:
            verdict = "CONFIRMED_ACTIVE"
            # Rule 3: Jaimini Confirmation Boost (+25% boost)
            if jaimini_activated:
                final_score = min(100.0, parashari_score * 1.25)
                harmonized_narrative = (
                    f"KP Sub-Lord promise confirms event feasibility, supported by Parashari Dasha ({parashari_score:.1f}%) "
                    f"and Jaimini Karaka activation, yielding high-confluence {event_type} manifestation."
                )
            else:
                harmonized_narrative = (
                    f"KP Sub-Lord promise confirms {event_type} feasibility, aligned with Parashari Dasha timeline ({parashari_score:.1f}%)."
                )

        return {
            "domain": domain,
            "event_type": event_type,
            "verdict": verdict,
            "kp_feasibility": "FAVORABLE" if kp_favorable else "UNFAVORABLE_BLOCK",
            "jaimini_confirmation_boost": jaimini_activated,
            "final_harmonized_score": round(final_score, 2),
            "harmonized_narrative": harmonized_narrative,
            "has_contradiction": not kp_favorable
        }

contradiction_resolver = ContradictionResolver()
