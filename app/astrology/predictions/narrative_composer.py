from typing import Dict, Any, List

class PredictionNarrativeComposer:
    """
    V3.22 Narrative Intelligence.
    Generates rich, comprehensive, multi-paragraph, evidence-driven interpretations and timing breakdowns.
    """

    TEMPLATES = {
        "Career & Authority": (
            "The professional sector and matters of authority are significantly activated by {primary_trigger}. "
            "This configuration indicates a powerful window for {event_type}, underpinned by {evidence_count} corroborating independent astrological nodes.\n\n"
            "**Natal Promise & Structural Alignment**: The foundational natal chart configuration provides structural support for leadership and professional expansion. "
            "Planetary positions in the career houses emphasize long-term strategic endurance and recognition from administrative or institutional forces.\n\n"
            "**Dasha & Transit Influence**: The active Vimshottari Dasha planetary rulers activate career leadership houses, coinciding with precision transit triggers that heighten productivity and executive capability."
        ),
        "Finance & Wealth": (
            "Financial indicators point toward substantial focus on {event_type}, driven primarily by the strong positioning and activation of {primary_trigger}. "
            "With {evidence_count} corroborating evidence points, this cycle highlights wealth generation and asset consolidation.\n\n"
            "**Natal Promise & Wealth Yoga**: Second and eleventh house lord alignments establish a secure foundation for financial growth, supporting prudent investments and resource management.\n\n"
            "**Dasha & Transit Influence**: Current planetary periods favor financial expansion, while beneficial transits unlock new streams of revenue and strategic economic planning."
        ),
        "Marriage & Relationships": (
            "The relationship landscape shows deep activation for {event_type}, guided by the energetic resonance of {primary_trigger}. "
            "This cycle is supported by {evidence_count} astrological corroborations focusing on partnership harmony and emotional bonding.\n\n"
            "**Natal Promise & Partnership Indicators**: Seventh house dynamics and D9 Navamsha confirmations reveal strong potential for relationship milestones and mutual growth.\n\n"
            "**Dasha & Transit Influence**: Active dasha rulers activate partnership sectors, creating optimal conditions for deepening commitments and resolving past interpersonal friction."
        ),
        "Default": (
            "Significant activation has been detected in the {domain} sector concerning {event_type}. "
            "Deterministic analysis confirms this period through {evidence_count} corroborating astrological evidence nodes.\n\n"
            "**Astrological Breakdown**: Planetary alignments and active life-cycle periods emphasize this domain, highlighting opportunities for personal development and conscious timing execution.\n\n"
            "**Practical Guidance**: Align your actions with these energetic peaks to maximize long-term positive outcomes."
        )
    }

    @staticmethod
    def compose_why_now(domain: str, event_type: str, triggers: List[str], evidence_count: int) -> str:
        template = PredictionNarrativeComposer.TEMPLATES.get(domain, PredictionNarrativeComposer.TEMPLATES["Default"])
        primary = triggers[0] if triggers else "confluence of planetary cycles"

        return template.format(
            domain=domain,
            event_type=event_type.replace('_', ' ').lower(),
            primary_trigger=primary,
            evidence_count=evidence_count
        )

narrative_composer = PredictionNarrativeComposer()
