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

    # Stephen King: 1947-09-21
    birth_dt = datetime(1947, 9, 21, 1, 30)
    chart = calculate_chart_data(birth_dt, 43.65, -70.25, "America/New_York")

    # Event: Carrie sold 1974-04-05
    sim_date = datetime(1974, 3, 6)

    with app.app_context():
        pred = FinancePredictionEngine.get_prediction(chart, sim_date)
        print(f"King Finance 1974:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Timing: {pred.timing_window.get('phase')} ({pred.timing_window.get('proximity_weight'):.2f})")
        print(f"  is_active (internal check would be needed, but check weight):")

if __name__ == "__main__":
    main()
