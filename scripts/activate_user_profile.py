import os
import sys
from datetime import datetime

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database.models import db, Chart
from app.astrology.core.chart import calculate_chart_data
from app.astrology.store import save_chart

def activate():
    app = create_app()
    with app.app_context():
        name = "Subramanian T S"
        dob = "1986-09-28"
        tob = "16:30"
        place = "Palakkad"
        lat, lon = 10.7867, 76.6547
        tz_str = "Asia/Kolkata"

        print(f"Calculating chart for {name}...")
        birth_dt = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
        chart_obj = calculate_chart_data(birth_dt, lat, lon, tz_str)

        chart_dict = chart_obj.model_dump()
        chart_dict["name"] = name
        chart_dict["birth_dob"] = dob
        chart_dict["birth_tob"] = tob
        chart_dict["place"] = place
        chart_dict["latitude"] = lat
        chart_dict["longitude_coord"] = lon
        chart_dict["timezone"] = tz_str

        cid = save_chart(chart_dict)
        print(f"✅ Profile activated in database. ID: {cid}")
        print("Please restart your browser or refresh the page.")

if __name__ == "__main__":
    activate()
