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

    # Malala Yousafzai: 1997-07-12
    birth_dt = datetime(1997, 7, 12, 10, 30)
    chart = calculate_chart_data(birth_dt, 34.77, 72.36, "Asia/Karachi")

    # Event: Nobel Prize 2014-10-10
    sim_date = datetime(2014, 9, 10)

    with app.app_context():
        pred = FamePredictionEngine.get_prediction(chart, sim_date)
        print(f"Malala Fame 2014:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
