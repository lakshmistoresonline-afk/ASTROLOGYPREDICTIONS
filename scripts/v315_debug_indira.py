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

    # Indira Gandhi: 1917-11-19
    birth_dt = datetime(1917, 11, 19, 23, 11)
    chart = calculate_chart_data(birth_dt, 25.45, 81.85, "Asia/Kolkata")

    # Event: PM 1966-01-24
    sim_date = datetime(1965, 12, 25)

    with app.app_context():
        print(f"Indira Chart Details:")
        print(f"  Ascendant: {chart.ascendant:.2f} ({chart.asc_rashi+1} Rashi)")
        for p_name, p in chart.planets.items():
            print(f"  {p_name:10} : House {p.house} ({p.longitude:.2f} deg)")

        pred = CareerPredictionEngine.get_prediction(chart, sim_date)
        print(f"Indira Career 1966:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Timing: {pred.timing_window.get('phase')} ({pred.timing_window.get('proximity_weight'):.2f})")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
