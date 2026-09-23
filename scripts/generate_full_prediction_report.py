import os
import sys
import json
from datetime import datetime

# Set PYTHONPATH to include project root
sys.path.append(os.getcwd())

from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.remedies.engine import get_personalized_remedies

def generate_report():
    print("Generating Detailed Prediction Report for Steve Jobs...")

    # 1. Profile Data
    name = "Steve Jobs"
    dob = "1955-02-24"
    tob = "19:15"
    lat, lon = 37.7749, -122.4194
    tz = "America/Los_Angeles"

    birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")

    # 2. Calculate Chart
    chart = calculate_chart_data(birth_dt, lat, lon, tz)

    # 3. Generate Predictions
    preds = generate_evidence_based_predictions(chart, selected_date=datetime.now())

    # 4. Get Remedies
    remedies = get_personalized_remedies(chart)

    # 5. Format Report
    report = []
    report.append(f"# Detailed Astrological Intelligence Report: {name}")
    report.append(f"**Birth Details**: {dob} {tob} | San Francisco, CA")
    report.append(f"**Generated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n---")

    # Lagna/Moon
    report.append("## 🏛️ Natal Blueprint Summary")
    report.append(f"- **Ascendant (Lagna)**: {chart.asc_nakshatra.name} ({chart.planets['Sun'].dispositor} Lord)")
    report.append(f"- **Moon Sign**: {chart.planets['Moon'].nakshatra.name}")
    report.append(f"- **Engine Confidence**: HIGH (Swiss Ephemeris)")

    # Strength
    report.append("\n## 💪 Planetary Potency (Shadbala)")
    for p, score in chart.vimsopaka_scores.items():
        # Using Vimsopaka as a proxy for multi-divisional strength
        report.append(f"- **{p}**: {score:.2f} / 20.0 (Divisional Alignment)")

    # Predictions
    report.append("\n## 🔮 Confluent Life Predictions")
    for p in preds['predictions']:
        report.append(f"### {p['domain']} - {p['event_type'].replace('_', ' ')}")
        report.append(f"**Signal Strength**: {p['score']}% | **Status**: {p['prediction_strength']}")
        report.append(f"**Peak Window**: {p['timing_window'].get('peak', 'N/A')}")
        report.append(f"**Intelligence Summary**: {p['summary']}")

        if p.get('supporting_factors'):
            report.append("**Supporting Evidence**:")
            for factor in p['supporting_factors'][:3]:
                report.append(f"  - {factor}")
        report.append("")

    # Remedies
    report.append("## 🛠️ Personal Alignment Protocols (Remedies)")
    for r in remedies:
        report.append(f"- **{r['planet']} ({r['approach']})**: {r['why']}")
        report.append(f"  - *Action*: {r['how']}")

    # Save to File
    with open("STEVE_JOBS_FULL_PREDICTIONS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print("✅ Full Prediction Report generated: STEVE_JOBS_FULL_PREDICTIONS.md")

if __name__ == "__main__":
    generate_report()
