from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
from ..database.models import db, UserAccount, SubscriptionRecord, OrderRecord, PaymentRecord, EntitlementRecord, AnalyticsEventLog
from ..services.commercial import EntitlementService, PaymentService, AnalyticsService

commercial_bp = Blueprint("commercial", __name__)

@commercial_bp.route("/pricing")
def pricing():
    return render_template("commercial/pricing.html")

@commercial_bp.route("/checkout/<product_id>")
def checkout(product_id):
    prices = {
        "plus_monthly": 499.00,
        "plus_yearly": 4999.00,
        "report_career": 299.00,
        "report_marriage": 299.00
    }
    amount = prices.get(product_id, 499.00)
    uid = session.get("user_id", 1) # default demo user or test account
    order = PaymentService.create_order(user_id=uid, product_id=product_id, amount=amount)
    return render_template("commercial/checkout.html", order=order, product_id=product_id, amount=amount)

@commercial_bp.route("/payment/success")
def payment_success():
    provider_order_id = request.args.get("order_id")
    provider_payment_id = request.args.get("payment_id", f"pay_{uuid4().hex[:8]}")
    if provider_order_id:
        PaymentService.fulfill_order(provider_order_id, provider_payment_id, 499.00)
    return render_template("commercial/success.html")

@commercial_bp.route("/payment/webhook", methods=["POST"])
def payment_webhook():
    data = request.json or {}
    event = data.get("event")
    if event == "payment.captured":
        payload = data.get("payload", {}).get("payment", {}).get("entity", {})
        order_id = payload.get("notes", {}).get("provider_order_id")
        payment_id = payload.get("id")
        amount = payload.get("amount", 0) / 100.0
        if order_id:
            PaymentService.fulfill_order(order_id, payment_id, amount)
    return jsonify({"status": "ok"})

@commercial_bp.route("/admin/business")
def admin_business():
    orders = OrderRecord.query.all()
    subscriptions = SubscriptionRecord.query.all()
    total_revenue = sum([o.amount for o in orders if o.status == "paid"])
    active_subs = len([s for s in subscriptions if s.status == "active"])
    return render_template("commercial/admin_business.html", orders=orders, subscriptions=subscriptions, total_revenue=total_revenue, active_subs=active_subs)
