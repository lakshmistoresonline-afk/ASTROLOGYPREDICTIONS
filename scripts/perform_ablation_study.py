import os
import sys
import json
from v312_audit_engine import run_audit

def main():
    os.environ["FLASK_SECRET_KEY"] = "audit-key-v312"
    from app import create_app
    app = create_app()

    ablation_scenarios = [
        {"label": "BASE", "overrides": {}},
        {"label": "NO_FOUNDATION", "overrides": {"DASHA_FOUNDATION": 0.0}},
        {"label": "NO_SECONDARY", "overrides": {"SECONDARY_PROMISE": 0.0}},
        {"label": "MINIMAL", "overrides": {"DASHA_FOUNDATION": 0.0, "SECONDARY_PROMISE": 0.0}},
    ]

    report = "# Combined Ablation Study: Jyotish OS Engine (V3.11 Baseline)\n\n"
    report += "| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec | Enrichment |\n"
    report += "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n"

    all_res = []
    for s in ablation_scenarios:
        print(f"Running scenario: {s['label']}")
        # Using full 39 cases
        res = run_audit(s['label'], slice(0, 39), config_overrides=s['overrides'], app=app)
        report += f"| {s['label']} | {res['precision']:.1%} | {res['recall']:.1%} | {res['specificity']:.1%} | {res['peak_n']} | {res['peak_precision']:.1%} | {res['enrichment']:.2f}x |\n"
        all_res.append(res)

    report += "\n## Analysis for Specificity Regression\n"
    # Regression was 74.4% (V3.10) -> 48.7% (V3.11 BASE)

    base_spec = all_res[0]['specificity']
    no_foundation_spec = all_res[1]['specificity']
    no_secondary_spec = all_res[2]['specificity']

    foundation_impact = no_foundation_spec - base_spec
    secondary_impact = no_secondary_spec - base_spec

    if foundation_impact > secondary_impact:
        report += f"**DASHA_FOUNDATION** is the primary driver of specificity regression (Gain when removed: {foundation_impact:.1%}).\n"
    elif secondary_impact > foundation_impact:
        report += f"**SECONDARY_PROMISE** is the primary driver of specificity regression (Gain when removed: {secondary_impact:.1%}).\n"
    else:
        report += "Both features contribute significantly to the specificity regression.\n"

    print(report)
    with open("ABLATION_STUDY_RESULTS.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()
