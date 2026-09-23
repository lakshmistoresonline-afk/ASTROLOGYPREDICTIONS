import os
import sys
import json
from datetime import datetime, timedelta

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.astrology.core.chart import calculate_chart_data
from app.astrology.predictions.engine import generate_evidence_based_predictions
from app.astrology.predictions.v317_timeline import lifetime_timeline_engine_v17
from app.astrology.remedies.engine import get_personalized_remedies
from app.astrology.core.bazi import calculate_bazi_pillars
from app.astrology.core.human_design import calculate_human_design
from app.astrology.core.galactic import analyze_galactic_aspects
from app.astrology.core.planets import NAKSHATRA_NAMES
from app.astrology.core.houses import RASHI_NAMES
from app.astrology.dasha import calculate_vimshottari
from app.api.external import geocode_place
from app.utils.pdf_generator import generate_complete_pdf
from app.astrology.evaluation.report_dag_orchestrator import report_dag_orchestrator

def run_gandhi_report():
    print("=" * 80)
    print("🌟 ASTRO PREDICTIONS - MAHATMA GANDHI FULL EMPIRICAL REPORT GENERATOR")
    print("===========================================================================")

    user_data = {
        "name": "Mahatma Gandhi",
        "dob": "1869-10-02",
        "tob": "08:36",
        "place": "Porbandar, Gujarat, India"
    }

    # Porbandar coordinates: 21.6417 N, 69.6293 E
    lat = 21.6417
    lon = 69.6293
    tz_str = "Asia/Kolkata"

    app = create_app()
    with app.app_context():
        birth_dt = datetime.strptime(f"{user_data['dob']} {user_data['tob']}", "%Y-%m-%d %H:%M")

        print("\n[STEP 1] Calculating Canonical Swiss Ephemeris Birth Chart for 1869-10-02 08:36...")
        chart = calculate_chart_data(birth_dt, lat, lon, tz_str)

        print(f"  ✅ Ascendant (Lagna): {RASHI_NAMES[chart.asc_rashi]} ({chart.ascendant % 30:.2f}°) | Nakshatra: {chart.asc_nakshatra.name} (Pada {chart.asc_nakshatra.pada}, Lord: {chart.asc_nakshatra.lord})")
        print(f"  ✅ Moon Sign: {RASHI_NAMES[chart.planets['Moon'].rashi]} ({chart.planets['Moon'].degree:.2f}°) | Nakshatra: {chart.planets['Moon'].nakshatra.name} (Pada {chart.planets['Moon'].nakshatra.pada})")
        print(f"  ✅ Sun Sign: {RASHI_NAMES[chart.planets['Sun'].rashi]} ({chart.planets['Sun'].degree:.2f}°) | Nakshatra: {chart.planets['Sun'].nakshatra.name}")
        print(f"  ✅ SHA256 Fingerprint: {chart.chart_fingerprint}")

        print("\n[STEP 2] Computing Point-in-Time Vimshottari Dasha Hierarchy at Birth...")
        dasha_info = calculate_vimshottari(chart.planets["Moon"].longitude, birth_dt, calculation_date=birth_dt)
        cm = dasha_info.get("current_maha", {})
        ca = dasha_info.get("current_antar", {})

        print(f"  ✅ Dasha at Birth: {cm.get('lord', 'N/A')} Mahadasha (Ends: {cm.get('end_str', 'N/A')})")

        print("\n[STEP 3] Executing Confluent Prediction Pipeline Across All 16 Domains...")
        now = datetime(1915, 1, 9) # Historical benchmark target date (Return to India / Public Leadership)
        preds = generate_evidence_based_predictions(chart, selected_date=now)
        predictions_list = preds.get('predictions', [])

        print(f"  ✅ Total Domains Evaluated: {len(predictions_list)}")
        for idx, p in enumerate(predictions_list, 1):
            print(f"     {idx:2d}. [{p.get('domain')}] {p.get('event_type')} | Score: {p.get('score')}% | Level: {p.get('prediction_strength')}")

        print("\n[STEP 4] Mapping Chronological Lifetime Roadmap (Age 0 - 80)...")
        dummy_id = f"gandhi-{chart.chart_fingerprint[:16]}"
        timeline = lifetime_timeline_engine_v17.generate_lifetime_timeline(chart, dummy_id)

        print(f"  ✅ Total Lifetime Events Mapped: {len(timeline.events)}")

        print("\n[STEP 5] Formulating Personalized Remedies & Alignment Protocols...")
        remedies = get_personalized_remedies(chart)

        # 3-Pass DAG Orchestration
        bazi = calculate_bazi_pillars(1869, 10, 2, 8, target_year=1915)
        dag_ast = report_dag_orchestrator.orchestrate_3_pass_report(
            chart_obj=chart,
            selected_date=now,
            predictions=predictions_list,
            bazi_data=bazi,
            timeline_events=timeline.events,
            remedies=remedies
        )

        # Generate PDF Report
        report_data = {
            "profile": {
                "name": user_data["name"],
                "dob": user_data["dob"],
                "tob": user_data["tob"],
                "place": user_data["place"],
                "lat": lat,
                "lon": lon,
                "tz": tz_str
            },
            "present": {
                "as_of": "1915-01-09",
                "top_signals": predictions_list[:5],
                "predictions": predictions_list,
                "timeline": preds.get('timeline', [])
            },
            "lifecycle": {
                "events": [e.model_dump() if hasattr(e, 'model_dump') else e for e in timeline.events],
                "phases": timeline.phases
            },
            "dashas": dasha_info.get("mahadashas", [])
        }

        pdf_bytes = generate_complete_pdf(report_data)
        pdf_filename = "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.pdf"
        pdf_path = os.path.abspath(pdf_filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"\n  ✅ PDF Render: SUCCESS ({len(pdf_bytes)} bytes)")
        print(f"  Saved PDF to: {pdf_path}")

        # Save Markdown Report
        md_filename = "FULL_INTELLIGENCE_REPORT_Mahatma_Gandhi.md"
        md_path = os.path.abspath(md_filename)

        md = []
        md.append(f"# 🌟 Authoritative Astrological Intelligence Report")
        md.append(f"**Subject Name**: {user_data['name']}")
        md.append(f"**Birth Particulars**: {user_data['dob']} at {user_data['tob']} | {user_data['place']}")
        md.append(f"**Coordinates**: {lat:.4f}° N, {lon:.4f}° E | **Timezone**: {tz_str}")
        md.append(f"**Engine Version**: P0.3-R42 / V3.36 Hardened Engine")
        md.append(f"**SHA256 Fingerprint**: `{chart.chart_fingerprint}`")
        md.append("\n" + "---" + "\n")

        md.append("## 🏛️ 1. Complete Natal Blueprint & Planetary Positions")
        md.append(f"- **Ascendant (Lagna)**: {RASHI_NAMES[chart.asc_rashi]} ({chart.ascendant % 30:.2f}°) | Nakshatra: **{chart.asc_nakshatra.name}** (Pada {chart.asc_nakshatra.pada}, Lord: {chart.asc_nakshatra.lord})")
        md.append(f"- **Moon Sign (Rashi)**: {RASHI_NAMES[chart.planets['Moon'].rashi]} ({chart.planets['Moon'].degree:.2f}°) | Nakshatra: **{chart.planets['Moon'].nakshatra.name}** (Pada {chart.planets['Moon'].nakshatra.pada}, Dispositor: {chart.planets['Moon'].dispositor})")
        md.append(f"- **Sun Sign**: {RASHI_NAMES[chart.planets['Sun'].rashi]} ({chart.planets['Sun'].degree:.2f}°) | Nakshatra: **{chart.planets['Sun'].nakshatra.name}**")
        md.append(f"- **Ayanamsa**: {chart.ayanamsa:.4f}° (Lahiri Sidereal)")

        md.append("\n### Comprehensive Planetary Metrics Table")
        md.append("| Planet | Longitude | Rashi | House | Dignity (Sthanabala) | Deeptadi State | Baladi Age Avastha | Retrograde | Combust | Shadbala | Vimsopaka (/20) |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for p_name, p in chart.planets.items():
            v_score = chart.vimsopaka_scores.get(p_name, 0.0)
            retro = "YES" if p.is_retrograde else "No"
            comb = "YES" if p.is_combust else "No"
            md.append(f"| **{p_name}** | {p.longitude:.2f}° | {RASHI_NAMES[p.rashi]} | House {p.house} | {p.dignity} | {p.deeptadi_avastha} | {p.baladi_avastha} | {retro} | {comb} | {p.shadbala_score:.1f} | {v_score:.2f} |")

        md.append("\n### Ashtakavarga Rashi Bindu Totals (SAV - Exact 337 Parashari Points)")
        md.append("| Rashi | SAV Points | Strength Evaluation |")
        md.append("|---|---|---|")
        if hasattr(chart, 'ashtakavarga') and isinstance(chart.ashtakavarga, dict):
            sav_list = chart.ashtakavarga.get('SAV', [0]*12)
            if isinstance(sav_list, list) and len(sav_list) >= 12:
                for r_idx in range(12):
                    b_num = sav_list[r_idx]
                    status = "Strong Prosperity (>28)" if b_num >= 28 else "Balanced Support (24-27)" if b_num >= 24 else "Challenging Friction (<24)"
                    md.append(f"| {RASHI_NAMES[r_idx]} | {b_num} Bindus | {status} |")

        md.append("\n## 📅 2. Lifetime Roadmap & Milestone Atlas")
        md.append("| Peak Date / Year | Domain | Event Type | Signal Strength | Detailed Summary Narrative |")
        md.append("|---|---|---|---|---|")
        for ev in timeline.events:
            e_dict = ev.model_dump() if hasattr(ev, 'model_dump') else ev
            p_date = e_dict.get('peak_date') or e_dict.get('peak', 'Active')
            narrative = e_dict.get('evidence_summary') or e_dict.get('why_now') or e_dict.get('summary') or f"Significant lifecycle milestone in {e_dict.get('domain')} sector."
            md.append(f"| **{p_date}** | {e_dict.get('domain', 'N/A')} | {e_dict.get('event_type', 'N/A')} | `{e_dict.get('event_magnitude', e_dict.get('strength', 'PEAK'))}` | {narrative} |")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        print(f"  ✅ Saved Markdown to: {md_path}")

if __name__ == "__main__":
    run_gandhi_report()
