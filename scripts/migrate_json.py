import json
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.database.models import db, Chart

def migrate():
    json_path = Path(__file__).parent.parent / "data" / "charts.json"
    if not json_path.exists():
        print("No legacy charts.json found.")
        return

    app = create_app()
    with app.app_context():
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading JSON: {e}")
            return

        print(f"Found {len(data)} charts in legacy store.")

        count = 0
        for cid, chart_data in data.items():
            # Check if already exists
            if Chart.query.get(cid):
                continue

            bd = chart_data.get("birth_datetime", "")
            dob = bd[:10] if "T" in bd else ""
            tob = bd[11:16] if "T" in bd else ""

            new_chart = Chart(
                id=cid,
                name=chart_data.get("name"),
                dob=dob,
                tob=tob,
                place=chart_data.get("place"),
                lat=chart_data.get("latitude"),
                lon=chart_data.get("longitude_coord"),
                tz=chart_data.get("timezone")
            )
            new_chart.set_data(chart_data)
            db.session.add(new_chart)
            count += 1

        db.session.commit()
        print(f"Successfully migrated {count} charts to SQLite.")

if __name__ == "__main__":
    migrate()
