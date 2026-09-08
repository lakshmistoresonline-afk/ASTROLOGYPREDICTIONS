import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engines.finance import FinancePredictionEngine

def main():
    os.environ["FLASK_SECRET_KEY"] = "debug-key"
    app = create_app()

    # Bill Gates: 1955-10-28
    birth_dt = datetime(1955, 10, 28, 22, 0)
    chart = calculate_chart_data(birth_dt, 47.6, -122.33, "America/Los_Angeles")

    # Event: IPO 1986-03-13
    sim_date = datetime(1986, 2, 11)

    with app.app_context():
        pred = FinancePredictionEngine.get_prediction(chart, sim_date)
        print(f"Gates Finance 1986:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Timing: {pred.timing_window.get('phase')} ({pred.timing_window.get('proximity_weight'):.2f})")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
