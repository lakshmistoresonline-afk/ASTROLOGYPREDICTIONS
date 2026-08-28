# BLIND TEST PROTOCOL

## 1. OBJECTIVE
To evaluate the Jyotish Engine's predictive accuracy without human bias or future-knowledge leakage.

## 2. ELIGIBILITY
- Engines: Career, Finance, Marriage, Health, Travel.
- Requirement: Frozen codebase. No rule changes permitted during protocol execution.

## 3. PROCEDURE
1. **Input Isolation**: The engine is provided with `BirthData` and a `HistoricalCutoffDate`.
2. **Deterministic Execution**: The `CalculationClient` fetches facts. `CorroborationEngine` synthesizes predictions.
3. **Trace Generation**: Save the hierarchicalFactObject for auditing.
4. **Scoring**: Reveal actual historical event date and compare against `TimingWindow`.
5. **Metric Reporting**: Log as per `TIMING_ACCURACY_REPORT`.

## 4. BLIND CONSTRAINTS
- NO manual dasha selection.
- NO manual transit house activation hints.
- NO access to the "Success" labels in the dataset until AFTER prediction is committed.

## 5. SUCCESS CRITERIA
- **VALIDATED**: Signal weight hierarchy produces consistent matches across 30+ charts.
- **PRELIMINARY**: High match rate on small sample size (<10).
- **FAILED**: Significant timing errors (>180 days) or false positives in high-confidence categories.
