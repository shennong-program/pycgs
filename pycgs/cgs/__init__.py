"""
`pycgs.cgs` is a module that provides the core algorithms and functions for Coreference-based Graph Search (CGS). 
"""

__all__ = [
    "foundational_cgs",
    "weighted_cgs",
    "PrimaryTermExtractor",
]

from .algorithms import foundational_cgs, weighted_cgs
from .primary_term_extractor import PrimaryTermExtractor
