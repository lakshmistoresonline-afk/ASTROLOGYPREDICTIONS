import pytest
from app.utils.fcm_dispatcher import fcm_dispatcher
from app.workers.daily_transits_worker import daily_transits_worker

def test_daily_transits_worker_fcm_dispatch():
    # Test high confluence trigger dispatch (>= 75.0%)
    res_high = fcm_dispatcher.dispatch_fcm_notification(
        fcm_token="fcm_valid_token_123",
        domain="Career & Authority",
        confluence_score=85.0,
        lang_code="en"
    )

    assert res_high["dispatched"] is True
    assert "Career & Authority" in res_high["title"]
    assert res_high["confluence_score"] == 85.0

    # Test suppressed low confluence trigger (< 75.0%)
    res_low = fcm_dispatcher.dispatch_fcm_notification(
        fcm_token="fcm_valid_token_123",
        domain="Career & Authority",
        confluence_score=60.0,
        lang_code="en"
    )

    assert res_low["dispatched"] is False
    assert "SUPPRESSED" in res_low["reason"]

def test_daily_transits_worker_profile_batch():
    profiles = [
        {"id": "usr_100", "fcm_token": "fcm_token_100", "latest_confluence_score": 88.0, "lang_code": "en"},
        {"id": "usr_200", "fcm_token": "fcm_token_200", "latest_confluence_score": 50.0, "lang_code": "en"}
    ]

    worker_res = daily_transits_worker.execute_daily_transit_scan(profiles)
    assert worker_res["worker_event"] == "DAILY_TRANSIT_SCAN_COMPLETED"
    assert worker_res["scanned_profiles"] == 2
    assert worker_res["push_alerts_dispatched"] == 1
