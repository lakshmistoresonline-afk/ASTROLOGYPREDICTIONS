import os
import uuid
from datetime import datetime
from ..database.models import db, Chart

# Toggle between Local SQLite, Firestore
USE_FIREBASE = os.getenv("USE_FIREBASE", "false").lower() == "true"

if USE_FIREBASE:
    from . import firebase_store as fb

    def save_chart(owner_uid: str, chart_data: dict) -> str:
        return fb.save_chart(owner_uid, chart_data)

    def list_charts(owner_uid: str) -> list:
        return fb.list_charts(owner_uid)

    def get_chart(owner_uid: str, cid: str) -> dict | None:
        return fb.get_chart(owner_uid, cid)

    def delete_chart(owner_uid: str, cid: str) -> bool:
        return fb.delete_chart(owner_uid, cid)

else:
    # SQLITE Implementation with strict owner scoping
    def save_chart(owner_uid: str, chart_data: dict) -> str:
        if not owner_uid:
            raise ValueError("AUTHENTICATION_REQUIRED: owner_uid is mandatory for saving a chart.")
        name = chart_data.get("name") or "Native"
        dob = chart_data.get("birth_dob")
        tob = chart_data.get("birth_tob")

        # Fallback to birth_datetime if dob/tob missing (V3.22 patch)
        if not dob or not tob:
            bdt_str = chart_data.get("birth_datetime")
            if bdt_str:
                try:
                    # Handle both datetime objects and ISO strings
                    if hasattr(bdt_str, "strftime"):
                        bdt = bdt_str
                    else:
                        from datetime import datetime
                        bdt = datetime.fromisoformat(str(bdt_str).replace('Z', '+00:00'))

                    if not dob: dob = bdt.strftime("%Y-%m-%d")
                    if not tob: tob = bdt.strftime("%H:%M")
                except:
                    pass

        if not dob or not tob:
            raise ValueError("DATA_INTEGRITY_ERROR: Birth date and birth time are required.")

        existing = Chart.query.filter_by(owner_uid=owner_uid, name=name, dob=dob, tob=tob).first()
        if existing:
            return existing.id

        cid = str(uuid.uuid4())[:8]
        new_chart = Chart(
            id=cid,
            owner_uid=owner_uid,
            name=name,
            dob=dob,
            tob=tob,
            place=chart_data.get("place"),
            lat=chart_data.get("latitude") or chart_data.get("lat"),
            lon=chart_data.get("longitude") or chart_data.get("longitude_coord") or chart_data.get("lon"),
            tz=chart_data.get("timezone") or chart_data.get("tz")
        )
        new_chart.set_data(chart_data)
        db.session.add(new_chart)
        db.session.commit()
        return cid

    def list_charts(owner_uid: str) -> list:
        if not owner_uid:
            return []
        try:
            charts = Chart.query.filter_by(owner_uid=owner_uid).order_by(Chart.saved_at.desc()).all()
            results = []
            for c in charts:
                data = c.get_data()
                data["id"] = c.id
                data["owner_uid"] = c.owner_uid
                data["saved_at"] = c.saved_at.isoformat() if c.saved_at else datetime.utcnow().isoformat()
                data["name"] = data.get("name", c.name or "Unknown")
                data["birth_datetime"] = data.get("birth_datetime", "")
                results.append(data)
            return results
        except Exception:
            return []

    def get_chart(owner_uid: str, cid: str) -> dict | None:
        if not owner_uid:
            return None
        c = Chart.query.filter_by(id=cid, owner_uid=owner_uid).first()
        if c:
            data = c.get_data()
            data["id"] = c.id
            data["owner_uid"] = c.owner_uid
            return data
        return None

    def delete_chart(owner_uid: str, cid: str) -> bool:
        if not owner_uid:
            return False
        c = Chart.query.filter_by(id=cid, owner_uid=owner_uid).first()
        if c:
            db.session.delete(c)
            db.session.commit()
            return True
        return False

    def save_prediction_snapshot(chart_id: str, domain_pred: dict, source_type: str = "UNVERIFIED",
                                 participant_id: str = None, session_id: str = None, group_id: str = "BETA_GROUP_1",
                                 cohort: str = None):
        from ..database.models import PredictionOutcome, db, Chart, Profile
        from datetime import datetime, timedelta
        import json

        if not cohort:
            chart = Chart.query.get(chart_id)
            if chart and chart.profile_id:
                profile = Profile.query.get(chart.profile_id)
                if profile:
                    cohort = "HOLDOUT" if profile.is_holdout else "VALIDATION"

        existing = PredictionOutcome.query.filter_by(
            chart_id=chart_id,
            domain=domain_pred.get("domain"),
            prediction_text=domain_pred.get("summary"),
            source_type=source_type
        ).filter(PredictionOutcome.created_at > datetime.utcnow() - timedelta(days=1)).first()

        if existing: return existing.id

        tw = domain_pred.get("timing_window", {})

        snapshot = PredictionOutcome(
            chart_id=chart_id,
            group_id=group_id,
            participant_id=participant_id,
            session_id=session_id,
            engine_version="V3.22",
            calculation_version="CALC-SWE-2.10.3",
            dasha_version="DASHA-VIM-365.2425",
            transit_version="TRANSIT-V3.15",
            evidence_version="EVIDENCE-V3.15",
            remedy_version="REMEDY-V3.15",
            timing_calibration_version="V3.22",
            domain=domain_pred.get("domain"),
            event_type=domain_pred.get("event_type"),
            event_magnitude=domain_pred.get("event_magnitude"),
            what_may_develop=domain_pred.get("what_may_develop"),
            prediction_strength=domain_pred.get("prediction_strength"),
            engine_confidence=domain_pred.get("confidence"),
            signal_score=domain_pred.get("score") / 100.0 if domain_pred.get("score") else 0.0,
            quality_score=domain_pred.get("quality_score"),
            calibrated_probability=None,
            prediction_text=domain_pred.get("summary"),
            possible_manifestations=json.dumps(domain_pred.get("manifestations", [])),
            confirmation_criteria=json.dumps(domain_pred.get("confirmation_criteria", [])),
            what_to_do=json.dumps(domain_pred.get("practical_actions", [])),
            remedy_text=json.dumps(domain_pred.get("remedies", [])),
            evidence_snapshot=json.dumps(domain_pred.get("evidence_chain", [])),
            start_date=tw.get("build") or tw.get("activation"),
            peak_date=tw.get("peak"),
            end_date=tw.get("decline"),
            timing_phase=tw.get("phase"),
            proximity_weight=tw.get("proximity_weight"),
            status="PENDING",
            source_type=source_type,
            cohort=cohort,
            matching_version="EVENT-MATCH-V1"
        )
        db.session.add(snapshot)
        db.session.commit()
        return snapshot.id
