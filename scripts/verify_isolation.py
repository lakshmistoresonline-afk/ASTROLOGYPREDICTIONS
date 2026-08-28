from app import create_app
from app.database.models import db, Chart, Profile
import os

def test_isolation():
    os.environ["FLASK_SECRET_KEY"] = "isolation-test-key"
    app = create_app()
    with app.app_context():
        db.create_all()

        # User A
        p1 = Profile(name="User A")
        db.session.add(p1)
        db.session.commit()
        c1 = Chart(id="A1", profile_id=p1.id, name="Chart A")
        db.session.add(c1)

        # User B
        p2 = Profile(name="User B")
        db.session.add(p2)
        db.session.commit()
        c2 = Chart(id="B1", profile_id=p2.id, name="Chart B")
        db.session.add(c2)
        db.session.commit()

        # Verify
        charts_a = Chart.query.filter_by(profile_id=p1.id).all()
        charts_b = Chart.query.filter_by(profile_id=p2.id).all()

        assert len(charts_a) == 1 and charts_a[0].id == "A1"
        assert len(charts_b) == 1 and charts_b[0].id == "B1"
        print("Data Isolation: PASS")

if __name__ == "__main__":
    test_isolation()
