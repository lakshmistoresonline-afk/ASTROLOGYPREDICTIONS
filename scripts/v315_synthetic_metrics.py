import os
import sys
import json
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, PredictionOutcome

def main():
    app = create_app()
    with app.app_context():
        # Filter for SYNTHETIC tests
        tests = PredictionOutcome.query.filter(
            PredictionOutcome.source_type == "SYNTHETIC"
        ).all()

        if not tests:
            print("STATUS: NO_SYNTHETIC_TESTS")
            return

        print("# V3.15 SYNTHETIC / TECHNICAL PIPELINE TESTS\n")
        print("| ID | Domain | Strength | Outcome | Timing Error |")
        print("| :--- | :--- | :--- | :--- | :--- |")

        for t in tests:
            print(f"| {t.id} | {t.domain} | {t.prediction_strength} | {t.status} | {t.timing_error_days}d |")

if __name__ == "__main__":
    main()
