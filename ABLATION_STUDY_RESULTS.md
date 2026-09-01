# Ablation Study: Jyotish OS Engine (V3.11 Baseline)

| Scenario | Precision | Recall | Specificity | PEAK N | PEAK Prec |
| :--- | :---: | :---: | :---: | :---: | :---: |
| BASELINE | 41.2% | 35.9% | 48.7% | 10 | 70.0% |
| NO_FOUNDATION | 42.4% | 35.9% | 51.3% | 7 | 57.1% |
| NO_SECONDARY | 42.9% | 30.8% | 59.0% | 7 | 85.7% |
| MINIMAL | 44.4% | 30.8% | 61.5% | 4 | 75.0% |

## Analysis
**DASHA_FOUNDATION** contributes most to specificity regression (Drop: -2.6%).
