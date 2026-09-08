import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engines.career import CareerPredictionEngine

def main():
    os.environ["FLASK_SECRET_KEY"] = "debug-key"
    app = create_app()

    # Serena Williams: 1981-09-26
    birth_dt = datetime(1981, 9, 26, 20, 28)
    chart = calculate_chart_data(birth_dt, 31.45, -83.51, "America/New_York")

    # Event: US Open 1999-09-11
    sim_date = datetime(1999, 8, 12)

    with app.app_context():
        pred = CareerPredictionEngine.get_prediction(chart, sim_date)
        print(f"Serena Career 1999:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
