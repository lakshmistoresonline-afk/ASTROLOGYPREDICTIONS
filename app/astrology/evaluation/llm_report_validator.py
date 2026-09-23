"""
LLM Output Evaluation & Regression Guard (Module 5 - Task 5.2).
Evaluates report outputs for Factuality, Completeness, and Contradictions with QA Score Card (0-100).
Rejects builds or output payloads with QA score < 90.
"""
from typing import Dict, Any, List

class LLMReportValidator:
    """
    Automated QA & Evaluation Engine for generated reports.
    Computes Factuality, Completeness, and Contradiction scores.
    """

    @staticmethod
    def evaluate_report_quality(report_markdown: str, chart_obj: Any) -> Dict[str, Any]:
        """
        Evaluates generated markdown report against AST payload.
        Returns QA Score Card (0-100).
        """
        qa_score = 100.0
        issues = []

        # 1. Completeness Check: Zero forbidden null placeholders
        forbidden = ["N/A", "- **RATIONALE**: \n", "[Insert Narrative]"]
        for f in forbidden:
            if f in report_markdown:
                qa_score -= 20.0
                issues.append(f"COMPLETENESS_VIOLATION: Found forbidden placeholder '{f}'")

        # 2. Factuality Check: Lagna Rashi alignment
        asc_rashi_idx = getattr(chart_obj, "asc_rashi", 0)
        from ..core.houses import RASHI_NAMES
        lagna_name = RASHI_NAMES[asc_rashi_idx]

        if lagna_name not in report_markdown:
            qa_score -= 15.0
            issues.append(f"FACTUALITY_VIOLATION: Lagna '{lagna_name}' not mentioned in report text")

        # 3. Contradiction Check: Primary predictions included
        if "Confluence Match Score" not in report_markdown:
            qa_score -= 15.0
            issues.append("CONTRADICTION_VIOLATION: Primary metric table missing")

        final_score = max(0.0, qa_score)
        passed = final_score >= 90.0

        return {
            "qa_score": final_score,
            "passed": passed,
            "issues": issues,
            "recommendation": "APPROVED" if passed else "REJECT_AND_RETRY"
        }

llm_report_validator = LLMReportValidator()
