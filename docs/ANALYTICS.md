# Astro Predictions — Analytics & Attribution

## 1. Analytics Service
- Privacy-first event logging (`AnalyticsService.log_event`). Strips all sensitive personal birth data (dob, tob, place, lat, lon) before persistence.

## 2. Attribution Service
- Captures UTM parameters (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `ref`, `referral_code`) and maintains first-touch and last-touch attribution records.
