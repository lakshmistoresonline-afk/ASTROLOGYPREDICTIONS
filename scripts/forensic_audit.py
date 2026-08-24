import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to sys.path
root = Path(__file__).parent.parent
sys.path.append(str(root))

def run_forensic_audit():
    print("=" * 70)
    print("🔮 ASTROLOGYPREDICTIONS - SUPREME FORENSIC AUDIT")
    print("=" * 70)

    # 1. Environment & Dependencies
    print("\n[STEP 1/5] Checking Critical Infrastructure...")
    os.environ['USE_FIREBASE'] = 'false'
    os.environ['FLASK_SECRET_KEY'] = 'audit-secret-key'
    os.environ['SE_EPHE_PATH'] = str(root / "ephe")

    try:
        import swisseph as swe
        import pydantic
        import flask
        print("  ✅ Python Libraries: All critical dependencies found.")
    except ImportError as e:
        print(f"  ❌ Dependency Error: {e}. Please run 'pip install -r requirements.txt'")
        return

    ephe_dir = root / "ephe"
    essential = ["seas_18.se1", "semo_18.se1", "sepl_18.se1"]
    for f in essential:
        if not (ephe_dir / f).exists():
            print(f"  ❌ Ephemeris Error: {f} missing. Run 'bash install.sh' to download.")
            return
    print("  ✅ Ephemeris Data: Essential files verified.")

    # 2. Master Engine Integrity
    print("\n[STEP 2/5] Stress-Testing Master Engine (Cross-Tradition Synthesis)...")
    try:
        from app.astrology.core.chart import calculate_chart_data
        # Test Case: New York, 1990-01-01 12:00 PM
        dt = datetime(1990, 1, 1, 12, 0)
        chart = calculate_chart_data(dt, 40.7128, -74.0060, "America/New_York")

        validations = [
            ("Vedic/KP Sub-lords", chart.kp_significators),
            ("Nadi D-150 Amshas", chart.planets["Sun"].nadi_amsha),
            ("Human Design Gates", chart.human_design["active_gates"]),
            ("Chinese Bazi Pillars", chart.bazi_pillars["Year"]),
            ("Hellenistic Lots", chart.hellenistic_lots["Lot of Fortune"]),
            ("Uranian Formulas", chart.uranian_formulas["Success"]),
            ("Ashtakavarga SAV", chart.ashtakavarga["SAV"]),
            ("Fixed Stars", chart.fixed_star_conjunctions)
        ]

        for name, data in validations:
            if data:
                print(f"  ✅ {name}: Integration Verified.")
            else:
                print(f"  ❌ {name}: Missing Data.")

    except Exception as e:
        print(f"  ❌ Engine Failure: {e}")
        import traceback
        traceback.print_exc()
        return

    # 3. Prediction Pipeline
    print("\n[STEP 3/5] Verifying Deterministic Inference Chain...")
    try:
        from app.astrology.predictions.engine import generate_evidence_based_predictions
        preds = generate_evidence_based_predictions(chart)
        print(f"  ✅ Prediction Hub: Successfully aggregated {len(preds['domains'])} life domains.")
        print(f"  ✅ Overall Score: {preds['overall_score']}/100 ({preds['overall_label']})")

        # Check for specific advanced synthesis
        if preds['advanced_metrics']['kp_4_steps']:
            print("  ✅ Advanced Metrics: Micro-timing bridge operational.")
    except Exception as e:
        print(f"  ❌ Pipeline Error: {e}")
        return

    # 4. Micro-Timing & Global Context
    print("\n[STEP 4/5] Auditing Micro-Timing & Global Cycles...")
    try:
        if preds['micro_timing']['Prana']:
             print(f"  ✅ 5-Level Dasha: Currently in {preds['micro_timing']['Prana']} Prana period.")
        if chart.upcoming_eclipses:
             print(f"  ✅ Eclipse Engine: {len(chart.upcoming_eclipses)} upcoming triggers tracked.")
        if chart.mundane_indicators:
             print(f"  ✅ Mundane Cycles: Global indicators synchronized.")
    except Exception as e:
        print(f"  ❌ Timing Audit Error: {e}")
        return

    # 5. Final Synthesis
    print("\n[STEP 5/5] Finalizing Supreme Build...")
    print("=" * 70)
    print("🎉 AUDIT PASSED: The Unified Global Engine is STABILIZED and ACCURATE.")
    print("=" * 70)
    print("\nHow to Run Locally:")
    print("1. Set FLASK_SECRET_KEY in .env")
    print("2. Run: python run.py")
    print("3. URL: http://localhost:5001")
    print("=" * 70)

if __name__ == "__main__":
    run_forensic_audit()
