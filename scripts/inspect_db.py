import os
from app import create_app
from app.database.models import db, Profile, Chart, PredictionOutcome, RemedyTask

def inspect():
    os.environ["FLASK_SECRET_KEY"] = "inspect-key"
    app = create_app()
    with app.app_context():
        profiles = Profile.query.all()
        print(f"TOTAL_PROFILES: {len(profiles)}")
        for p in profiles:
            print(f"PROFILE: {p.name} (ID: {p.id})")
            charts = Chart.query.filter_by(profile_id=p.id).all()
            print(f"  CHARTS: {len(charts)}")
            for c in charts:
                outcomes = PredictionOutcome.query.filter_by(chart_id=c.id).all()
                active_outcomes = [o for o in outcomes if o.status != 'PENDING']
                print(f"    CHART: {c.name} - SNAPSHOTS: {len(outcomes)} - REPORTED: {len(active_outcomes)}")

        remedies = RemedyTask.query.all()
        print(f"TOTAL_REMEDY_TASKS: {len(remedies)}")
        active_remedies = [r for r in remedies if r.completion_count > 0]
        print(f"ACTIVE_REMEDY_INTERACTIONS: {len(active_remedies)}")

if __name__ == "__main__":
    inspect()
