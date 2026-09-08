import os
import sys
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.astrology.core.chart import calculate_chart_data
from app.astrology.dasha import calculate_vimshottari
from app import create_app

def main():
    os.environ["FLASK_SECRET_KEY"] = "debug-key"
    app = create_app()
    # Michael Jordan: 1963-02-17
    birth_dt = datetime(1963, 2, 17, 13, 40)
    chart = calculate_chart_data(birth_dt, 35.22, -80.84, "America/New_York")

    sim_date = datetime(1975, 1, 1)

    with app.app_context():
        from app.astrology.predictions.engines.career import CareerPredictionEngine
        print(f"MJ Chart Details:")
        print(f"  Ascendant: {chart.ascendant:.2f} ({chart.asc_rashi+1} Rashi)")
        for p_name, p in chart.planets.items():
            print(f"  {p_name:10} : House {p.house} ({p.longitude:.2f} deg)")

        pred = CareerPredictionEngine.get_prediction(chart, sim_date)
        print(f"MJ Career 1975:")
        print(f"  Strength: {pred.prediction_strength}")
        print(f"  Score: {pred.score}")
        print(f"  Q: {pred.quality_score}")
        print(f"  Timing: {pred.timing_window.get('phase')} ({pred.timing_window.get('proximity_weight'):.2f})")
        print(f"  Evidence:")
        for e in pred.evidence_chain:
            print(f"    - {e.source}: {e.description} ({e.strength_score:.3f})")

if __name__ == "__main__":
    main()
