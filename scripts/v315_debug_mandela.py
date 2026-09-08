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

    # Nelson Mandela: 1918-07-18
    birth_dt = datetime(1918, 7, 18, 14, 54)
    chart = calculate_chart_data(birth_dt, -31.98, 28.51, "Africa/Johannesburg")

    # Event: Inauguration 1994-05-10
    sim_date = datetime(1994, 4, 10)

    with app.app_context():
        pred = FamePredictionEngine.get_prediction(chart, sim_date)
        print(f"Mandela Fame 1994:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
