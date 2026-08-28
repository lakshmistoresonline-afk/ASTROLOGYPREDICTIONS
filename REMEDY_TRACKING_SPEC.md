# REMEDY TRACKING SPECIFICATION (V1.0)

## 1. OBJECTIVE
To monitor user adherence to prescribed traditional remedies and collect qualitative feedback on perceived balance.

## 2. ADHERENCE LOOP
Remedies are not "Effective" or "Ineffective" in a clinical sense; they are "Deterministic" and "Traditional". Adherence is the primary metric.

### tracking actions
- **COMPLETE**: Mark the remedy as performed for the current cycle.
- **SKIP**: Log a non-performance event without breaking the sequence.
- **PAUSE**: Temporarily disable tracking for an active remedy.

## 3. METRICS
- **ADHERENCE RATE**: % of cycles completed vs prescribed.
- **STREAK**: Consecutive days of completion.
- **CONSISTENCY**: Verification that the engine returns the same remedy for the same chart condition.

## 4. FEEDBACK (CALIBRATION)
Users can provide optional notes upon completion:
- Perceived feeling of "Balance".
- Qualitative notes on life area stress levels.

## 5. REPRODUCIBILITY
Remedies are tied to the `remedyVersion` registered in the prediction snapshot.
