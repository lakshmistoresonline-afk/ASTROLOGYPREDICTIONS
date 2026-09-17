# Astro Predictions — Revenue Architecture

## 1. Entities
- `UserAccount`, `SubscriptionRecord`, `OrderRecord`, `PaymentRecord`, `EntitlementRecord`, `AttributionRecord`, `AnalyticsEventLog`.

## 2. Fulfillment Flow
Client Purchase → Payment Provider (Razorpay / Google Play Billing) → Server Verification Webhook → `PaymentService.fulfill_order()` → `EntitlementRecord` / `SubscriptionRecord` update → Audit Logging.
