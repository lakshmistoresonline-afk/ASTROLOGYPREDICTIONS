# V4 Rule Performance Tracking

## Rule Performance Engine (`tracker.py`)
- Tracks sample size, precision, recall, and timing error for every prediction rule across all 12 evidence families.
- Rules with insufficient sample size return `NO DATA` to maintain rigorous scientific honesty.
