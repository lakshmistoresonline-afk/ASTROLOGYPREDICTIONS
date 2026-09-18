from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, g, flash
from datetime import datetime
from ..database.models import db, UserAccount, SubscriptionRecord, OrderRecord, PaymentRecord, EntitlementRecord, PaymentSettings
from ..services.commercial import EntitlementService, PaymentService
from ..services.auth import login_required, require_admin

commercial_bp = Blueprint("commercial", __name__)

@commercial_bp.route("/pricing")
def pricing():
    return render_template("commercial/pricing.html")

@commercial_bp.route("/checkout/<product_id>")
@login_required
def checkout(product_id):
    prices = {
        "plus_monthly": 499.00,
        "plus_yearly": 4999.00,
        "report_career": 299.00,
        "report_marriage": 299.00,
        "report_finance": 299.00
    }
    amount = prices.get(product_id, 499.00)
    uid = g.current_user.id
    order = PaymentService.create_order(user_id=uid, product_id=product_id)
    settings = PaymentService.get_settings()
    return render_template("commercial/checkout.html", order=order, product_id=product_id, amount=amount, settings=settings)

@commercial_bp.route("/payment/submit-proof", methods=["POST"])
@login_required
def submit_payment_proof():
    order_id = request.form.get("order_id")
    utr = request.form.get("utr_number")
    if not order_id or not utr:
        flash("Order ID and UTR transaction reference are required.", "danger")
        return redirect(url_for("commercial.pricing"))

    try:
        PaymentService.submit_payment_proof(int(order_id), utr)
        flash("Payment proof submitted successfully! Awaiting administrator verification.", "success")
        return render_template("commercial/under_review.html", order_id=order_id, utr=utr)
    except Exception as e:
        flash(f"Error submitting payment: {e}", "danger")
        return redirect(url_for("commercial.pricing"))

@commercial_bp.route("/admin/payments")
@require_admin
def admin_payments():
    pending_orders = OrderRecord.query.filter_by(status="payment_submitted").all()
    all_orders = OrderRecord.query.order_by(OrderRecord.created_at.desc()).limit(50).all()
    settings = PaymentService.get_settings()
    return render_template("commercial/admin_payments.html", pending_orders=pending_orders, all_orders=all_orders, settings=settings)

@commercial_bp.route("/admin/payments/approve/<int:order_id>", methods=["POST"])
@require_admin
def admin_approve_payment(order_id):
    success = PaymentService.verify_and_approve_order(order_id)
    if success:
        flash(f"Order #{order_id} verified and entitlement activated successfully.", "success")
    else:
        flash(f"Failed to approve order #{order_id}.", "danger")
    return redirect(url_for("commercial.admin_payments"))

@commercial_bp.route("/admin/payments/reject/<int:order_id>", methods=["POST"])
@require_admin
def admin_reject_payment(order_id):
    success = PaymentService.reject_order(order_id)
    if success:
        flash(f"Order #{order_id} rejected.", "warning")
    else:
        flash(f"Failed to reject order #{order_id}.", "danger")
    return redirect(url_for("commercial.admin_payments"))

@commercial_bp.route("/admin/payments/settings", methods=["POST"])
@require_admin
def admin_update_payment_settings():
    upi_id = request.form.get("upi_id")
    payee_name = request.form.get("payee_name")
    qr_url = request.form.get("qr_code_url")
    instructions = request.form.get("instructions")
    is_active = bool(request.form.get("is_active"))

    PaymentService.update_settings(upi_id, payee_name, qr_url, instructions, is_active)
    flash("Payment settings updated successfully.", "success")
    return redirect(url_for("commercial.admin_payments"))

@commercial_bp.route("/admin/business")
@require_admin
def admin_business():
    orders = OrderRecord.query.all()
    subscriptions = SubscriptionRecord.query.all()
    total_revenue = sum([o.amount for o in orders if o.status == "paid"])
    active_subs = len([s for s in subscriptions if s.status == "active"])
    return render_template("commercial/admin_business.html", orders=orders, subscriptions=subscriptions, total_revenue=total_revenue, active_subs=active_subs)
