import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engines.fame import FamePredictionEngine

def main():
    os.environ["FLASK_SECRET_KEY"] = "debug-key"
    app = create_app()

    # Lata Mangeshkar: 1929-09-28
    birth_dt = datetime(1929, 9, 28, 22, 0)
    chart = calculate_chart_data(birth_dt, 18.52, 73.85, "Asia/Kolkata")

    # Event: Mahal breakthrough 1949
    sim_date = datetime(1948, 12, 2)

    with app.app_context():
        pred = FamePredictionEngine.get_prediction(chart, sim_date)
        print(f"Lata Fame 1949:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
