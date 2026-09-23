"""
Server-Sent Events (SSE) Gateway (Part 2 - Task 2).
Exposes GET /api/v3/stream/transits/live delivering millisecond-level transit stream data.
"""
from flask import Blueprint, Response
from datetime import datetime
import json
import time

streaming_v3_bp = Blueprint("streaming_v3", __name__, url_prefix="/api/v3/stream")

@streaming_v3_bp.route("/transits/live", methods=["GET"])
def live_transit_sse_stream():
    """
    GET /api/v3/stream/transits/live
    Server-Sent Events (SSE) endpoint delivering real-time transit updates.
    """
    def generate_sse_events():
        from .websocket_transits import calculate_current_transits_realtime
        while True:
            payload = calculate_current_transits_realtime()
            data_str = json.dumps(payload)
            yield f"event: transit_update\ndata: {data_str}\n\n"
            time.sleep(1.0)

    return Response(generate_sse_events(), mimetype="text/event-stream")
