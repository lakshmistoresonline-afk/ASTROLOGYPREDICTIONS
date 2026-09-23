import os
import sys
from datetime import datetime

# Set PYTHONPATH
sys.path.append(os.getcwd())

from app.astrology.core.chart import calculate_chart_data

def verify():
    print("Testing Chart Calculation with Vimsopaka Scaling...")
    dt = datetime(1990, 1, 1, 12, 0)
    lat, lon = 28.6139, 77.2090
    tz = "Asia/Kolkata"

    chart = calculate_chart_data(dt, lat, lon, tz)

    if hasattr(chart, "vimsopaka_scores"):
        print("✅ vimsopaka_scores attribute exists.")
        print(f"   Scores: {chart.vimsopaka_scores}")
    else:
        print("❌ vimsopaka_scores attribute MISSING.")
        return

    # Test Natal Promise Scaling
    from app.astrology.predictions.v5_natal_promise import evaluate_natal_promise
    res = evaluate_natal_promise(chart, "CAREER", "PROMOTION")
    print(f"✅ Prediction Evaluation Score: {res['promise_score']}")
    print(f"   Level: {res['promise_level']}")

if __name__ == "__main__":
    verify()
