"""
Async Task Orchestrator & Parallel Feature Extractor (Module 4 - Task 4.2).
Executes independent chart evaluation routines concurrently using thread pools for sub-100ms pipeline execution.
"""
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor
from ..strength.shadbala import calculate_shadbala
from ..charts.ashtakavarga import calculate_ashtakavarga
from ..core.bazi import calculate_bazi_pillars
from ..core.human_design import calculate_human_design

class ParallelExtractor:
    """
    Parallel Feature Extractor executing independent worker threads concurrently.
    Worker 1: Shadbala & Dignities
    Worker 2: Ashtakavarga Matrix Aggregation
    Worker 3: BaZi Four Pillars
    Worker 4: Human Design Systems
    """

    @staticmethod
    def extract_features_parallel(chart_obj: Any) -> Dict[str, Any]:
        """
        Executes feature workers concurrently in parallel.
        """
        results = {}

        def worker_shadbala():
            return getattr(chart_obj, "vimsopaka_scores", {})

        def worker_ashtakavarga():
            planets_rashi = {n: getattr(p, "rashi", 0) for n, p in getattr(chart_obj, "planets", {}).items()}
            asc_rashi = getattr(chart_obj, "asc_rashi", 0)
            return calculate_ashtakavarga(planets_rashi, asc_rashi)

        def worker_bazi():
            b_dt = getattr(chart_obj, "birth_datetime")
            return calculate_bazi_pillars(b_dt.year, b_dt.month, b_dt.day, b_dt.hour)

        def worker_human_design():
            return calculate_human_design(getattr(chart_obj, "planets", {}))

        with ThreadPoolExecutor(max_workers=4) as executor:
            f_shad = executor.submit(worker_shadbala)
            f_asht = executor.submit(worker_ashtakavarga)
            f_bazi = executor.submit(worker_bazi)
            f_hd = executor.submit(worker_human_design)

            results["vimsopaka"] = f_shad.result()
            results["ashtakavarga"] = f_asht.result()
            results["bazi"] = f_bazi.result()
            results["human_design"] = f_hd.result()

        return results

parallel_extractor = ParallelExtractor()
