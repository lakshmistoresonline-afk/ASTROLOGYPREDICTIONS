from typing import Dict, Any, List

class PredictionNarrativeComposer:
    """
    V3.22 Narrative Intelligence.
    Generates domain-specific, evidence-driven explanations without boilerplate.
    """

    TEMPLATES = {
        "Career & Authority": "The professional sector is activated by {primary_trigger}. This indicates potential for {event_type}, supported by {evidence_count} nodes of independent evidence.",
        "Finance & Wealth": "Financial signals suggest a focus on {event_type}. The strength of this period is driven by {primary_trigger} in your natal and dasha layers.",
        "Marriage & Relationships": "The relationship landscape shows activation for {event_type}. This window is primarily influenced by {primary_trigger} triggers.",
        "Property & Assets": "Asset-related windows are opening for {event_type}. The alignment of {primary_trigger} supports long-term structural decisions.",
        "Default": "Significant activation detected in {domain} related to {event_type}. Evidence shows {evidence_count} corroborating nodes."
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
