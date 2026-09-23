"""
Zero-Downtime Health Check Probes & Prometheus Metrics Endpoint (Module 24 - Task 24.4).
Probes GET /health/live (Liveness) and GET /health/ready (Readiness), and exports GET /metrics.
"""
from flask import Blueprint, jsonify, Response
from datetime import datetime
import sys
import psutil
from ..services.ephemeris_sync_service import ephemeris_sync_service
from ..middleware.observability_middleware import observability_middleware

health_bp = Blueprint("health", __name__)

@health_bp.route("/health/live", methods=["GET"])
def liveness_probe():
    """
    GET /health/live
    Kubernetes Liveness Probe: Checks process status and memory usage.
    """
    mem = psutil.virtual_memory()
    return jsonify({
        "status": "UP",
        "timestamp": datetime.now().isoformat(),
        "python_version": sys.version.split()[0],
        "memory_percent_used": mem.percent
    }), 200

@health_bp.route("/health/ready", methods=["GET"])
def readiness_probe():
    """
    GET /health/ready
    Kubernetes Readiness Probe: Verifies Swiss Ephemeris data files and calculation ready state.
    """
    sync_info = ephemeris_sync_service.sync_ephemeris_files()
    if sync_info.get("ephemeris_path_valid"):
        return jsonify({
            "status": "READY",
            "timestamp": datetime.now().isoformat(),
            "ephemeris_sync": sync_info
        }), 200

    return jsonify({
        "status": "NOT_READY",
        "timestamp": datetime.now().isoformat(),
        "reason": "Ephemeris path invalid or unreadable"
    }), 503

@health_bp.route("/metrics", methods=["GET"])
def prometheus_metrics():
    """
    GET /metrics
    Prometheus metrics exporter.
    """
    metrics_text = observability_middleware.generate_prometheus_metrics_text()
    return Response(metrics_text, mimetype="text/plain")
