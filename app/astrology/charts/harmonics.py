from typing import Dict, List, Any

def calculate_harmonics(planets_lon: Dict[str, float], harmonics: List[int]) -> Dict[int, Dict[str, float]]:
    """
    Calculate Western Harmonic charts (1 to N).
    Formula: (Longitude * H) % 360
    """
    results = {}
    for h in harmonics:
        h_chart = {}
        for name, lon in planets_lon.items():
            h_chart[name] = (lon * h) % 360
        results[h] = h_chart
    return results

def analyze_harmonic_resonance(harmonic_charts: Dict[int, Dict[str, float]]) -> List[str]:
    """Find conjunctions in high-order harmonics (indicating hidden talent/destiny)."""
    resonances = []
    # Check for conjunctions in H5 (Talent), H7 (Spirituality), H9 (Idealism)
    for h, chart in harmonic_charts.items():
        p_names = list(chart.keys())
        for i in range(len(p_names)):
            for j in range(i + 1, len(p_names)):
                if abs(chart[p_names[i]] - chart[p_names[j]]) < 1.0:
                    resonances.append(f"H{h} Resonance: {p_names[i]} and {p_names[j]} are conjunct in the {h}th Harmonic chart.")
    return resonances
