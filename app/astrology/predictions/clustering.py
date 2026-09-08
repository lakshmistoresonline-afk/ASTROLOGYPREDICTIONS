from typing import List, Dict, Any
from collections import defaultdict
from datetime import datetime

class EventClusteringEngine:
    """
    V3.21 Clustering Engine.
    Identifies related signals sharing triggers and peaks.
    """

    @staticmethod
    def cluster_predictions(predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Groups domains by peak date and common triggers."""
        # 1. Group by Peak Date
        peaks = defaultdict(list)
        for p in predictions:
            peak = p.get('timing_window', {}).get('peak')
            if peak:
                peaks[peak].append(p)

        clusters = []
        for date, group in peaks.items():
            if len(group) > 1:
                # Potential Cluster
                domains = [p['domain'] for p in group]
                # Identify shared triggers (Transit node source + planet)
                triggers = set()
                for p in group:
                    for ev in p.get('evidence_chain', []):
                        if ev.get('source') == 'TRANSIT_TRIGGER' and ev.get('planet_involved'):
                            triggers.add(ev['planet_involved'])

                if triggers:
                    clusters.append({
                        "id": f"cluster-{date}-{list(triggers)[0]}",
                        "date": date,
                        "primary_trigger": list(triggers)[0],
                        "domains": domains,
                        "description": f"Synergetic peak in {', '.join(domains)} driven by {list(triggers)[0]} triggers."
                    })

        return clusters

clustering_engine = EventClusteringEngine()
