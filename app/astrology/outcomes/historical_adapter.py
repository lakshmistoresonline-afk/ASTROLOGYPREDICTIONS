import json
import os
from typing import List, Dict, Any
from .dataset_importer import ImportedOutcomeRecord, dataset_registry

def load_historical_cases_dataset(json_path: str = "data/backtest/raw/historical_cases.json") -> Dict[str, Any]:
    """
    Adapter converting historical_cases.json into V4 canonical outcome records (REAL_OUTCOME_DATA).
    """
    if not os.path.exists(json_path):
        return {"success": False, "error": "File not found"}

    with open(json_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    records: List[ImportedOutcomeRecord] = []
    for idx, case in enumerate(cases):
        name = case.get("name", f"Historical_Case_{idx}")
        dob = case.get("dob")
        tob = case.get("tob")
        lat = case.get("lat")
        lon = case.get("lon")
        tz = case.get("tz", "UTC")

        for ev in case.get("events", []):
            event_date = ev.get("date")
            domain = ev.get("domain")
            desc = ev.get("description")
            status = ev.get("status")
            ev_type = ev.get("type", "major_life_event")

            # Map status == OCCURRED to valid real outcome record
            if status == "OCCURRED":
                raw_rec = {
                    "person_id": name,
                    "birth_date": dob,
                    "birth_time": tob,
                    "birth_timezone": tz,
                    "birth_place": name,
                    "latitude": lat,
                    "longitude": lon,
                    "event_type": ev_type,
                    "event_date": event_date,
                    "event_precision": "EXACT_DAY",
                    "birth_time_precision": "EXACT_RECORDED",
                    "source": "historical_cases.json",
                    "source_reference": desc,
                    "provenance": f"Biographical Archive ({domain})",
                    "dataset_classification": "REAL_OUTCOME_DATA"
                }
                records.append(ImportedOutcomeRecord(raw_rec))

    meta = dataset_registry.register_dataset(
        dataset_id="historical_cases_v1",
        name="Historical Biographical Cases",
        version="1.0",
        classification="REAL_OUTCOME_DATA",
        source="Historical Archive (historical_cases.json)",
        license_str="Research/Open Source",
        provenance="Curated biographical dataset",
        records=records
    )

    return {"success": True, "meta": meta, "record_count": len(records)}
