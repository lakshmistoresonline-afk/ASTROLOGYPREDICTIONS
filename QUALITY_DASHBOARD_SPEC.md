# QUALITY DASHBOARD SPECIFICATION (ADMIN ONLY)

## 1. OBJECTIVE
To provide real-time visualization of engine performance across all live production data.

## 2. KEY PERFORMANCE INDICATORS (KPIs)
- **EVENT DETECTION RATE**: % of non-"DID NOT OCCUR" outcomes.
- **TIMING PRECISION**: Histogram of matches across 15, 30, and 90-day buckets.
- **CONFIDENCE CORRELATION**: Comparison of match rates between VERY STRONG and MODERATE labels.
- **FALSE POSITIVE RATE**: % of DID NOT OCCUR outcomes for STRONG+ labels.

## 3. DOMAIN STATUS REGISTRY
Internal registry mapping domains to validation confidence:
- **VALIDATED**: 50+ cases, >80% detection, >60% timing hit.
- **PRELIMINARY**: <50 cases or lower match rates.
- **INSUFFICIENT DATA**: <10 cases.

## 4. VERSION COMPARISON
Capability to toggle between V1.0 snapshots and future V1.1+ outcomes to ensure rule changes are making the system more correct.

## 5. AUDIT TRAIL
Access to every individual prediction trace (Why this prediction?) to investigate timing or detection failures.
