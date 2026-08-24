from typing import Dict, Any, List
from datetime import datetime, timedelta
from ..core.models import CanonicalChart, DomainPrediction
from .framework import analyze_domain, EvidenceEngine
from ..timing.engine import get_timing_score

def get_monthly_prediction(chart: CanonicalChart, target_date: datetime) -> Dict[str, Any]:
    """Generate a comprehensive monthly forecast."""
    # 1. Overall Trend (weighted across key domains)
    domains_to_check = {
        "Career": (["Saturn", "Sun", chart.house_lords[10]], [10, 6]),
        "Finance": (["Jupiter", "Venus", chart.house_lords[2]], [2, 11]),
        "Relationships": (["Venus", "Jupiter", chart.house_lords[7]], [7, 5]),
        "Health": (["Sun", "Moon", chart.house_lords[1]], [1, 6, 8])
    }

    monthly_scores = {}
    for domain, (planets, houses) in domains_to_check.items():
        timing = get_timing_score(chart, planets, houses, target_date)
        monthly_scores[domain] = {
            "score": timing["total_timing_score"] * 10,
            "label": timing["label"]
        }

    # 2. Key Opportunities & Cautions
    opportunities = []
    cautions = []

    for domain, data in monthly_scores.items():
        if data["score"] > 7.0:
            opportunities.append(f"Strong support for {domain} related activities.")
        elif data["score"] < 4.0:
            cautions.append(f"Potential challenges in {domain}; exercise patience.")

    # 3. Overall trend label
    avg_score = sum(d["score"] for d in monthly_scores.values()) / len(monthly_scores)
    overall_trend = "Growth & Expansion" if avg_score > 7.0 else "Consolidation" if avg_score > 4.5 else "Introspective Phase"

    return {
        "month": target_date.strftime("%B %Y"),
        "overall_trend": overall_trend,
        "scores": monthly_scores,
        "opportunities": opportunities,
        "cautions": cautions,
        "avg_score": round(avg_score, 1)
    }
