# -*- coding: utf-8 -*-
"""
PandasAI is a wrapper around a LLM to make dataframes conversational
"""
from .smart_dataframe import SmartDataframe
from .smart_datalake import SmartDatalake
from .helpers.cache import Cache
from .agent import Agent
from .skills import skill

def clear_cache(filename: str = None):
    """Clear the cache"""
    cache = Cache(filename or "cache_db")
    cache.clear()


__all__ = [
    "SmartDataframe",
    "SmartDatalake",
    "Agent",
    "clear_cache",
    "skill",
]
