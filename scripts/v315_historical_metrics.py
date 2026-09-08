import os
import sys
import json
from datetime import datetime
from collections import defaultdict

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, PredictionOutcome

def calculate_metrics(outcomes):
    tp = len([o for o in outcomes if o.status == "OCCURRED" and o.prediction_strength in ["ACTIVE", "PEAK"]])
    fp = len([o for o in outcomes if o.status == "DID_NOT_OCCUR" and o.prediction_strength in ["ACTIVE", "PEAK"]])
    fn = len([o for o in outcomes if o.status == "OCCURRED" and o.prediction_strength not in ["ACTIVE", "PEAK"]])
    tn = len([o for o in outcomes if o.status == "DID_NOT_OCCUR" and o.prediction_strength not in ["ACTIVE", "PEAK"]])

    tp_watch = len([o for o in outcomes if o.status == "OCCURRED" and o.prediction_strength in ["WATCH", "ACTIVE", "PEAK"]])
    fn_watch = len([o for o in outcomes if o.status == "OCCURRED" and o.prediction_strength not in ["WATCH", "ACTIVE", "PEAK"]])

    return {
        "precision": tp / (tp + fp) if (tp + fp) > 0 else 0,
        "recall": tp / (tp + fn) if (tp + fn) > 0 else 0,
        "specificity": tn / (tn + fp) if (tn + fp) > 0 else 0,
        "watch_recall": tp_watch / (tp_watch + fn_watch) if (tp_watch + fn_watch) > 0 else 0,
        "count": len(outcomes)
    }

def main():
    app = create_app()
    with app.app_context():
        # Filter for frozen V3.15 HISTORICAL data
        hist_outcomes = PredictionOutcome.query.filter(
            PredictionOutcome.source_type == "HISTORICAL"
        ).all()

        if not hist_outcomes:
            print("STATUS: NO_HISTORICAL_DATA")
            return

        print("# V3.15 HISTORICAL VALIDATION METRICS\n")
        print("*This report is based on retrospective backtest data only.*\n")

        # 1. Global Performance
        m = calculate_metrics(hist_outcomes)
        print("## Global Performance")
        print(f"- **Historical Sample Size**: {m['count']}")
        print(f"- **Precision**: {m['precision']:.1%}")
        print(f"- **Recall**: {m['recall']:.1%}")
        print(f"- **Specificity**: {m['specificity']:.1%}")
        print(f"- **WATCH Recall**: {m['watch_recall']:.1%}\n")

        # 2. Domain Breakdown
        print("## Domain Breakdown")
        print("| Domain | Count | Recall | Precision |")
        print("| :--- | :---: | :---: | :---: |")

        domains = sorted(list(set([o.domain for o in hist_outcomes])))
        for d in domains:
            dm = calculate_metrics([o for o in hist_outcomes if o.domain == d])
            print(f"| {d} | {dm['count']} | {dm['recall']:.1%} | {dm['precision']:.1%} |")

if __name__ == "__main__":
    main()
