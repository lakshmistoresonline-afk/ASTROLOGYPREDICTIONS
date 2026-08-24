# Yoga Detector Reference

This document lists the planetary combinations (yogas) detected by the ASTROLOGYPREDICTIONS engine.

## 🏛️ Standard Categories

### Rajayogis (Success & Rise)
- **Kendra-Trikona Associations**: Lords of 1, 4, 7, 10 associated with lords of 5, 9.
- **Dharma Karma Adhipati**: Association between 9th and 10th lords.
- **Pancha Mahapurusha**: Ruchaka, Bhadra, Hamsa, Malavya, Shasha.

### Dhana Yogas (Wealth)
- **Wealth Lords**: Associations between lords of 1, 2, 5, 9, 11.
- **Lakshmi Yoga**: 9th lord in Kendra and strong Lagna lord.
- **Vasumathi Yoga**: Benefics in Upachaya houses (3, 6, 10, 11).

### Specialized Combinations
- **Gaja Kesari**: Jupiter in Kendra from Moon.
- **Budha Aditya**: Sun and Mercury conjunction (without combustion).
- **Adhi Yoga**: Benefics in 6, 7, 8 from Moon.
- **Kala Sarpa**: All planets hemmed between nodes.
- **Guru-Chandala**: Jupiter with nodes (Questioning tradition).
- **Punarphoo**: Saturn and Moon association (Delays and depth).

### Cautions & Challenges
- **Kemadruma**: No planets in signs adjacent to Moon.
- **Daridra Yoga**: 11th lord in Dusthana (6, 8, 12).
- **Neecha Bhanga**: Potential cancellation factors for debilitated planets.

## ⚙️ Logic Standards
Every yoga is detected using deterministic house/rashi math and returns:
- `present`: Boolean status.
- `strength`: Calculated based on planetary dignity.
- `interpretation`: Traditional Parashari meaning.
