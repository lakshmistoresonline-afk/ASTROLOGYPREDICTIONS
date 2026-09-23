"""
Automated Hallucination & Drift Detector (Module 16 - Task 16.1).
Cross-checks generated narrative text against raw AST JSON payload to detect and reject factual hallucinations.
"""
from typing import Dict, Any, List
import re

class HallucinationDriftDetector:
    """
    Production validation guard checking text statements against AST ground truth.
    """

    @staticmethod
    def verify_narrative_factuality(narrative_text: str, chart_obj: Any) -> Dict[str, Any]:
        """
        Cross-checks narrative claims against raw AST chart payload.
        Example: If text claims 'Mars in House 12', verifies that natal Mars is in House 12.
        """
        discrepancies = []
        text_lower = narrative_text.lower()

        planets = getattr(chart_obj, "planets", {})
        for p_name, p in planets.items():
            p_house = getattr(p, "house", 0)
            p_lower = p_name.lower()

            # Check for incorrect house claims (e.g. "mars in house 5" when Mars is in house 12)
            house_matches = re.findall(rf'{p_lower}\s+in\s+house\s+(\d+)', text_lower)
            for claimed_house in house_matches:
                if int(claimed_house) != p_house:
                    discrepancies.append(
                        f"FACTUAL_HALLUCINATION: Narrative claims {p_name} is in House {claimed_house}, but AST ground truth is House {p_house}."
                    )

        has_hallucination = len(discrepancies) > 0

        return {
            "has_hallucination": has_hallucination,
            "discrepancies": discrepancies,
            "factuality_score": 100.0 if not has_hallucination else 70.0,
            "recommendation": "PASSED" if not has_hallucination else "TRIGGER_MODEL_RETRY"
        }

hallucination_drift_detector = HallucinationDriftDetector()
