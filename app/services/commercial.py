from datetime import datetime
import json
import hmac
import hashlib
import os
from ..database.models import db, UserAccount, SubscriptionRecord, OrderRecord, PaymentRecord, EntitlementRecord, AttributionRecord, AnalyticsEventLog
from .catalog import CANONICAL_PRODUCTS

class EntitlementService:
    @staticmethod
    def has_subscription(user_id: int) -> bool:
        if not user_id:
            return False
        sub = SubscriptionRecord.query.filter_by(user_id=user_id, status="active").first()
        if sub:
            if sub.renews_at and sub.renews_at > datetime.utcnow():
                return True
            if not sub.renews_at:
                return True
        return False

    @staticmethod
    def has_feature(user_id: int, feature_name: str) -> bool:
        if EntitlementService.has_subscription(user_id):
            return True
        if not user_id:
            return False
        ents = EntitlementRecord.query.filter_by(user_id=user_id).all()
        for ent in ents:
            if ent.feature_name == feature_name:
                if not ent.expires_at or ent.expires_at > datetime.utcnow():
                    return True
            prod = CANONICAL_PRODUCTS.get(ent.feature_name)
            if prod and feature_name in prod.get("feature_entitlements", []):
                if not ent.expires_at or ent.expires_at > datetime.utcnow():
                    return True
        return False

    @staticmethod
    def is_ad_free(user_id: int) -> bool:
        return EntitlementService.has_subscription(user_id) or EntitlementService.has_feature(user_id, "ad_free")

class PaymentService:
    @staticmethod
    def create_order(user_id: int, product_id: str, amount: float = None, currency: str = "INR") -> OrderRecord:
        prod = CANONICAL_PRODUCTS.get(product_id)
        if amount is None:
            if prod and prod.get("active"):
                amount = prod["price"]
            else:
                amount = 499.00

        order = OrderRecord(
            user_id=user_id,
            product_id=product_id,
            amount=amount,
            currency=currency,
            status="pending",
            provider_order_id=f"order_{product_id}_{int(datetime.utcnow().timestamp())}"
        )
        db.session.add(order)
        db.session.commit()
        return order

    @staticmethod
    def verify_webhook_signature(payload_body: bytes, signature: str) -> bool:
        secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")
        if not secret:
            return True
        expected_signature = hmac.new(secret.encode('utf-8'), payload_body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_signature, signature)

    @staticmethod
    def fulfill_order(provider_order_id: str, provider_payment_id: str, amount: float, currency: str = "INR") -> bool:
        order = OrderRecord.query.filter_by(provider_order_id=provider_order_id).first()
        if not order:
            order = OrderRecord(
                user_id=1,
                product_id="plus_monthly",
                amount=amount,
                currency=currency,
                status="pending",
                provider_order_id=provider_order_id
            )
            db.session.add(order)
            db.session.commit()

        if order.status == "paid":
            return True

        prod = CANONICAL_PRODUCTS.get(order.product_id)
        if not prod:
            return False

        if float(order.amount) != float(amount) or order.currency != currency:
            order.status = "mismatched_amount"
            db.session.commit()
            return False

        order.status = "paid"
        payment = PaymentRecord(
            order_id=order.id,
            provider_payment_id=provider_payment_id,
            status="success",
            amount=amount
        )
        db.session.add(payment)

        if prod["product_type"] == "subscription":
            sub = SubscriptionRecord(
                user_id=order.user_id or 1,
                provider="razorpay",
                status="active",
                plan_type=order.product_id
            )
            db.session.add(sub)
        else:
            ent = EntitlementRecord(
                user_id=order.user_id or 1,
                feature_name=order.product_id
            )
            db.session.add(ent)

        db.session.commit()
        return True

class AttributionService:
    @staticmethod
    def record(anonymous_id: str, source: str, medium: str, campaign: str, referral: str):
        attr = AttributionRecord.query.filter_by(anonymous_id=anonymous_id).first()
        if not attr:
            attr = AttributionRecord(
                anonymous_id=anonymous_id,
                first_touch_source=source,
                first_touch_medium=medium,
                last_touch_source=source,
                last_touch_medium=medium,
                campaign=campaign,
                referral_code=referral
            )
            db.session.add(attr)
        else:
            attr.last_touch_source = source
            attr.last_touch_medium = medium
            attr.campaign = campaign
            if referral:
                attr.referral_code = referral
        db.session.commit()

class AnalyticsService:
    @staticmethod
    def log_event(event_name: str, anonymous_id: str, properties: dict = None):
        if properties is None:
            properties = {}
        for sensitive in ["dob", "tob", "place", "lat", "lon", "birth_datetime", "email", "phone"]:
            if sensitive in properties:
                properties.pop(sensitive)

        log = AnalyticsEventLog(
            event_name=event_name,
            anonymous_id=anonymous_id or "anon",
            properties_json=json.dumps(properties)
        )
        db.session.add(log)
        db.session.commit()

class AdService:
    @staticmethod
    def is_ads_enabled(user_id: int) -> bool:
        return not EntitlementService.is_ad_free(user_id)
