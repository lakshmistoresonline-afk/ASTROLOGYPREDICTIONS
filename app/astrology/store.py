import os
import uuid
from datetime import datetime
from ..database.models import db, Chart

# Toggle between Local SQLite, Firestore
USE_FIREBASE = os.getenv("USE_FIREBASE", "false").lower() == "true"

if USE_FIREBASE:
    from . import firebase_store as fb

    def save_chart(chart_data: dict) -> str:
        return fb.save_chart(chart_data)

    def list_charts() -> list:
        return fb.list_charts()

    def get_chart(cid: str) -> dict | None:
        return fb.get_chart(cid)

    def delete_chart(cid: str) -> bool:
        return fb.delete_chart(cid)

else:
    # SQLITE Implementation
    def save_chart(chart_data: dict) -> str:
        cid = str(uuid.uuid4())[:8]
        new_chart = Chart(
            id=cid,
            name=chart_data.get("name"),
            dob=chart_data.get("birth_dob"),
            tob=chart_data.get("birth_tob"),
            place=chart_data.get("place"),
            lat=chart_data.get("latitude"),
            lon=chart_data.get("longitude_coord"),
            tz=chart_data.get("timezone")
        )
        new_chart.set_data(chart_data)
        db.session.add(new_chart)
        db.session.commit()
        return cid

    def list_charts() -> list:
        try:
            charts = Chart.query.order_by(Chart.saved_at.desc()).all()
            results = []
            for c in charts:
                data = c.get_data()
                data["id"] = c.id
                data["saved_at"] = c.saved_at.isoformat() if c.saved_at else datetime.now().isoformat()
                # Ensure keys exist for template
                data["name"] = data.get("name", c.name or "Unknown")
                data["birth_datetime"] = data.get("birth_datetime", "")
                results.append(data)
            return results
        except Exception as e:
            print(f"Error listing charts: {e}")
            return []

    def get_chart(cid: str) -> dict | None:
        c = Chart.query.get(cid)
        if c:
            data = c.get_data()
            data["id"] = c.id
            return data
        return None

    def delete_chart(cid: str) -> bool:
        c = Chart.query.get(cid)
        if c:
            db.session.delete(c)
            db.session.commit()
            return True
        return False
