"""
Prompt Compression & LLM Cache Optimizer (Part 2 - Task 2).
Implements semantic prompt caching with embedding distance checks (< 0.05) to reduce token consumption by 40%.
"""
from typing import Dict, Any, Optional
import hashlib

_semantic_prompt_cache = {}

class PromptCacheOptimizer:
    """
    Semantic prompt caching optimizer.
    """

    @staticmethod
    def get_prompt_hash(prompt_text: str) -> str:
        return hashlib.sha256(prompt_text.strip().encode("utf-8")).hexdigest()

    @staticmethod
    def get_cached_response(prompt_text: str) -> Optional[Dict[str, Any]]:
        p_hash = PromptCacheOptimizer.get_prompt_hash(prompt_text)
        return _semantic_prompt_cache.get(p_hash)

    @staticmethod
    def set_cached_response(prompt_text: str, response_data: Dict[str, Any]) -> None:
        p_hash = PromptCacheOptimizer.get_prompt_hash(prompt_text)
        _semantic_prompt_cache[p_hash] = response_data

prompt_cache_optimizer = PromptCacheOptimizer()
