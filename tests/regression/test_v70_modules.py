import pytest
from datetime import datetime
from app.services.push_notifier import push_notifier
from app.workers.daily_transits_worker import daily_transits_worker

def test_v70_push_notifier_localized_delivery():
    res_en = push_notifier.dispatch_confluence_push(
        fcm_token="fcm_token_12345",
        domain="Career & Authority",
        confluence_score=88.0,
        lang_code="en"
    )
    assert res_en["dispatched"] is True
    assert "Career & Authority" in res_en["title"]
    assert res_en["confluence_score"] == 88.0

    res_hi = push_notifier.dispatch_confluence_push(
        fcm_token="fcm_token_67890",
        domain="Dasha",
        confluence_score=82.0,
        lang_code="hi"
    )
    assert res_hi["dispatched"] is True
    assert "दशा" in res_hi["title"]

def test_v70_daily_transits_worker_scan():
    user_profiles = [
        {"id": "usr_1", "fcm_token": "fcm_token_sample_1", "latest_confluence_score": 82.0, "lang_code": "en"},
        {"id": "usr_2", "fcm_token": None, "latest_confluence_score": 40.0, "lang_code": "en"}
    ]

    scan_res = daily_transits_worker.execute_daily_transit_scan(user_profiles)
    assert scan_res["worker_event"] == "DAILY_TRANSIT_SCAN_COMPLETED"
    assert scan_res["scanned_profiles"] == 2
    assert scan_res["push_alerts_dispatched"] == 1
