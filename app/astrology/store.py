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
        # Hardened Name Validation (Phase 8)
        name = chart_data.get("name") or "Native"
        dob = chart_data.get("birth_dob")
        tob = chart_data.get("birth_tob")

        # Duplicate Protection (Phase 9)
        existing = Chart.query.filter_by(name=name, dob=dob, tob=tob).first()
        if existing:
            return existing.id

        cid = str(uuid.uuid4())[:8]
        new_chart = Chart(
            id=cid,
            name=name,
            dob=dob,
            tob=tob,
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
        except Exception:
            return []

    def get_chart(cid: str) -> dict | None:
        c = db.session.get(Chart, cid)
        if c:
            data = c.get_data()
            data["id"] = c.id

            # Ensure DOB/TOB are present even if columns were empty (Phase 4 Logic)
            if c.dob:
                data["birth_dob"] = c.dob
                data["birth_tob"] = c.tob
            elif data.get("birth_datetime"):
                try:
                    dt = datetime.fromisoformat(str(data.get("birth_datetime")))
                    data["birth_dob"] = dt.strftime("%Y-%m-%d")
                    data["birth_tob"] = dt.strftime("%H:%M")
                except:
                    pass
            elif not data.get("birth_dob") and data.get("birth_datetime"):
                try:
                    dt = datetime.fromisoformat(str(data.get("birth_datetime")))
                    data["birth_dob"] = dt.strftime("%Y-%m-%d")
                    data["birth_tob"] = dt.strftime("%H:%M")
                except:
                    pass

            if not data.get("birth_dob") and c.saved_at:
                data["birth_dob"] = c.saved_at.strftime("%Y-%m-%d")
                data["birth_tob"] = "12:00"

            data["latitude"] = c.lat if c.lat is not None else data.get("latitude")
            data["longitude_coord"] = c.lon if c.lon is not None else data.get("longitude")
            data["timezone"] = c.tz or data.get("timezone") or "Asia/Kolkata"
            return data
        return None

    def delete_chart(cid: str) -> bool:
        c = Chart.query.get(cid)
        if c:
            db.session.delete(c)
            db.session.commit()
            return True
        return False

    def save_prediction_snapshot(chart_id: str, domain_pred: dict, source_type: str = "UNVERIFIED",
                                 participant_id: str = None, session_id: str = None, group_id: str = "BETA_GROUP_1",
                                 cohort: str = None):
        """Auto-generate immutable snapshot for tracking. Prevents duplicates within 24h."""
        from ..database.models import PredictionOutcome, db, Chart, Profile
        from datetime import datetime, timedelta
        import json

        # Fetch cohort from profile if not provided
        if not cohort:
            chart = Chart.query.get(chart_id)
            if chart and chart.profile_id:
                profile = Profile.query.get(chart.profile_id)
                if profile:
                    cohort = "HOLDOUT" if profile.is_holdout else "VALIDATION"

        # Duplicate check
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
            engine_version="V3.22", # Premium Transformation
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
