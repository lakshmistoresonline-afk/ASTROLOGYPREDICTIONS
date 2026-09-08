import os
import sys
from datetime import datetime, timedelta

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engines.education import EducationPredictionEngine

def main():
    os.environ["FLASK_SECRET_KEY"] = "debug-key"
    app = create_app()

    # Albert Einstein: 1879-03-14
    birth_dt = datetime(1879, 3, 14, 11, 30)
    chart = calculate_chart_data(birth_dt, 48.4, 10.0, "Europe/Berlin")

    # FP date 1890-01-01
    sim_date = datetime(1889, 12, 2)

    with app.app_context():
        pred = EducationPredictionEngine.get_prediction(chart, sim_date)
        print(f"Einstein Education 1890:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Timing: {pred.timing_window.get('phase')} ({pred.timing_window.get('proximity_weight'):.2f})")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
