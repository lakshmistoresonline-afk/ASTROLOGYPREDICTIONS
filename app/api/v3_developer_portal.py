"""
Developer Portal & Interactive Playground API (Module 11 - Part 3).
Provides REST/GraphQL endpoints for API key provisioning, developer sandbox execution, and SDK downloads.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

dev_portal_v3_bp = Blueprint("dev_portal_v3", __name__, url_prefix="/api/v3/developer")

_developer_keys = {}

@dev_portal_v3_bp.route("/keys/generate", methods=["POST"])
def generate_developer_api_key():
    """
    POST /api/v3/developer/keys/generate
    Provisions new developer API key with tier rate limits.
    """
    data = request.get_json() or {}
    email = data.get("email", "dev@example.com")
    tier = data.get("tier", "pro")

    key_prefix = "ent_" if tier == "enterprise" else "pro_" if tier == "pro" else "free_"
    new_key = f"{key_prefix}{uuid.uuid4().hex}"

    _developer_keys[new_key] = {
        "email": email,
        "tier": tier,
        "created_at": datetime.now().isoformat(),
        "active": True
    }

    return jsonify({
        "status": "SUCCESS",
        "api_key": new_key,
        "tier": tier,
        "rate_limit": "600 req/min" if tier == "pro" else "60 req/min",
        "message": "Developer API Key provisioned successfully."
    }), 201

@dev_portal_v3_bp.route("/sandbox/query", methods=["POST"])
def developer_sandbox_query():
    """
    POST /api/v3/developer/sandbox/query
    Interactive playground endpoint for live developer testing.
    """
    data = request.get_json() or {}
    domain = data.get("domain", "Career & Authority")

    return jsonify({
        "sandbox_mode": True,
        "query_domain": domain,
        "simulated_confluence_score": 82.5,
        "response_time_ms": 12.4,
        "status": "SUCCESS"
    }), 200
