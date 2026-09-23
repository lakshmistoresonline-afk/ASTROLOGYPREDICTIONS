"""
Quantitative Probability & Risk Matrix Generator (Module 9 - Task 9.2).
Generates a 12-month 365-day rolling dataset with daily probability scores (0.0 to 1.0) across 5 core pillars:
1. Career & Professional Momentum
2. Financial Liquidity & Investment Risk
3. Physical Vitality & Health Vulnerability
4. Relationship Harmony & Relational Friction
5. Geographic Mobility & Relocation Likelihood
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
import math

class ProbabilityMatrixGenerator:
    """
    Generates 365-day continuous time-series probability dataset for frontend interactive chart widgets.
    """

    @staticmethod
    def generate_12month_probability_matrix(
        chart_obj: Any,
        start_date: datetime,
        base_scores: Dict[str, float] = None
    ) -> List[Dict[str, Any]]:
        """
        Outputs a 365-day time-series JSON array containing daily scores (0.0 to 1.0) across 5 pillars.
        """
        if base_scores is None:
            base_scores = {
                "career": 0.68,
                "finance": 0.58,
                "health": 0.35,
                "relationships": 0.63,
                "mobility": 0.51
            }

        dataset = []
        for day_offset in range(365):
            curr_date = start_date + timedelta(days=day_offset)
            date_str = curr_date.strftime("%Y-%m-%d")

            # Cyclical transit modulation (Sine / Cosine wave harmonics based on planetary speed)
            c_wave = math.sin(day_offset * 2.0 * math.pi / 29.5) * 0.12 # Moon cycle harmonic
            f_wave = math.cos(day_offset * 2.0 * math.pi / 88.0) * 0.08 # Mercury cycle harmonic
            h_wave = math.sin(day_offset * 2.0 * math.pi / 365.25) * 0.05 # Sun cycle harmonic

            c_score = round(min(1.0, max(0.0, base_scores.get("career", 0.5) + c_wave)), 3)
            f_score = round(min(1.0, max(0.0, base_scores.get("finance", 0.5) + f_wave)), 3)
            h_score = round(min(1.0, max(0.0, base_scores.get("health", 0.5) + h_wave)), 3)
            r_score = round(min(1.0, max(0.0, base_scores.get("relationships", 0.5) - c_wave*0.5)), 3)
            m_score = round(min(1.0, max(0.0, base_scores.get("mobility", 0.5) + f_wave*0.5)), 3)

            dataset.append({
                "date": date_str,
                "day_index": day_offset,
                "career_momentum": c_score,
                "financial_liquidity": f_score,
                "vitality_health": h_score,
                "relational_harmony": r_score,
                "relocation_mobility": m_score
            })

        return dataset

probability_matrix_generator = ProbabilityMatrixGenerator()
