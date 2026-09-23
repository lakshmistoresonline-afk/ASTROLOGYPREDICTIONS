"""
Multi-Turn What-If Scenario Simulator (Module 13 - Task 13.2).
Evaluates and compares prospective candidate dates/times in real time with side-by-side comparative scores.
"""
from typing import Dict, Any, List
from datetime import datetime
from ..astrology.predictions.engine import generate_evidence_based_predictions

class ScenarioSimulator:
    """
    Evaluates side-by-side 'What-If' scenarios for prospective launch/event dates.
    """

    @staticmethod
    def compare_candidate_dates(
        chart_obj: Any,
        domain: str,
        option_a_dt: datetime,
        option_b_dt: datetime
    ) -> Dict[str, Any]:
        """
        Evaluates and compares two candidate dates through the prediction pipeline.
        """
        preds_a = generate_evidence_based_predictions(chart_obj, selected_date=option_a_dt)
        preds_b = generate_evidence_based_predictions(chart_obj, selected_date=option_b_dt)

        # Get domain score for Option A
        score_a = 50.0
        for p in preds_a.get("predictions", []):
            if domain.lower() in p.get("domain", "").lower():
                score_a = p.get("score", 50.0)
                break

        # Get domain score for Option B
        score_b = 50.0
        for p in preds_b.get("predictions", []):
            if domain.lower() in p.get("domain", "").lower():
                score_b = p.get("score", 50.0)
                break

        recommended = "Option A" if score_a >= score_b else "Option B"

        return {
            "domain": domain,
            "option_a": {
                "date": option_a_dt.strftime("%Y-%m-%d"),
                "confluence_score": round(score_a, 2)
            },
            "option_b": {
                "date": option_b_dt.strftime("%Y-%m-%d"),
                "confluence_score": round(score_b, 2)
            },
            "recommendation": recommended,
            "analysis": f"{recommended} offers superior multi-system planetary alignment ({max(score_a, score_b):.1f}% vs {min(score_a, score_b):.1f}%)."
        }

scenario_simulator = ScenarioSimulator()
