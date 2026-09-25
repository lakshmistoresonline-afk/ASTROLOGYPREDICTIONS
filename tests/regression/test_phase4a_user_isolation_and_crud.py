import pytest
import os
from app import create_app

def test_unauthenticated_requests_return_401():
    app = create_app()
    client = app.test_client()

    # Unauthenticated GET /api/v1/charts
    res = client.get("/api/v1/charts")
    assert res.status_code == 401
    data = res.get_json()
    assert data["error"] == "AUTHENTICATION_REQUIRED"

    # Unauthenticated GET /api/v1/dashboard
    res = client.get("/api/v1/dashboard")
    assert res.status_code == 401 or res.status_code == 302

    # Unauthenticated POST /api/v1/charts
    res = client.post("/api/v1/charts", json={"name": "Test"})
    assert res.status_code == 401

def test_two_user_chart_isolation_and_crud():
    app = create_app()
    client_a = app.test_client()
    client_b = app.test_client()

    # Authenticate User A session
    with client_a.session_transaction() as sess:
        sess["firebase_id_token"] = "token_user_a"
        sess["firebase_uid"] = "uid_user_a"
        sess["birth_name"] = "User A"

    # Authenticate User B session
    with client_b.session_transaction() as sess:
        sess["firebase_id_token"] = "token_user_b"
        sess["firebase_uid"] = "uid_user_b"
        sess["birth_name"] = "User B"

    # 1. User A creates Chart A
    chart_data_a = {
        "name": "Chart A Native",
        "birth_dob": "1990-01-01",
        "birth_tob": "10:00",
        "birth_place": "New Delhi, India",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    res_a = client_a.post("/api/v1/charts", json=chart_data_a)
    assert res_a.status_code == 201
    cid_a = res_a.get_json()["chart_id"]

    # 2. User B creates Chart B
    chart_data_b = {
        "name": "Chart B Native",
        "birth_dob": "1995-05-15",
        "birth_tob": "14:30",
        "birth_place": "London, UK",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "timezone": "Europe/London"
    }
    res_b = client_b.post("/api/v1/charts", json=chart_data_b)
    assert res_b.status_code == 201
    cid_b = res_b.get_json()["chart_id"]

    # 3. User A lists charts -> sees ONLY Chart A
    res_list_a = client_a.get("/api/v1/charts")
    assert res_list_a.status_code == 200
    charts_a = res_list_a.get_json()["charts"]
    cids_a = [c.get("id") or c.get("chart_id") for c in charts_a]
    assert cid_a in cids_a
    assert cid_b not in cids_a

    # 4. User B lists charts -> sees ONLY Chart B
    res_list_b = client_b.get("/api/v1/charts")
    assert res_list_b.status_code == 200
    charts_b = res_list_b.get_json()["charts"]
    cids_b = [c.get("id") or c.get("chart_id") for c in charts_b]
    assert cid_b in cids_b
    assert cid_a not in cids_b

    # 5. User A attempts to activate User B's Chart B -> 404 / 403 Forbidden
    res_cross_act = client_a.post(f"/api/v1/charts/{cid_b}/activate")
    assert res_cross_act.status_code in [403, 404]

    # 6. User A attempts to delete User B's Chart B -> 404 / 403 Forbidden
    res_cross_del = client_a.delete(f"/api/v1/charts/{cid_b}")
    assert res_cross_del.status_code in [403, 404]

    # 7. User A deletes Chart A -> 200 OK
    res_del_a = client_a.delete(f"/api/v1/charts/{cid_a}")
    assert res_del_a.status_code == 200

    # 8. User A lists charts -> Chart A is now gone
    res_list_a_after = client_a.get("/api/v1/charts")
    charts_a_after = res_list_a_after.get_json()["charts"]
    cids_a_after = [c.get("id") or c.get("chart_id") for c in charts_a_after]
    assert cid_a not in cids_a_after

def test_matchmaking_validation_error():
    app = create_app()
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["firebase_id_token"] = "token_tester"
        sess["firebase_uid"] = "uid_tester"

    # Missing b_dob / g_dob returns 400 VALIDATION_ERROR
    res = client.post("/api/v1/matchmaking", json={})
    assert res.status_code == 400
    data = res.get_json()
    assert data["error"] == "VALIDATION_ERROR"
