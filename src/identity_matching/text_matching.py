"""
Free-text matching — normalization and fuzzy comparison of descriptive text
fields (community names, building names, property types, nationalities, and
similar short descriptive strings extracted from documents).

Pure value-to-value functions: callers extract the value from their own
document shape and pass the resulting strings in here. See name_matching.py
for the equivalent utilities for person names -- unlike that module, this one
applies no name-specific normalization (no honorific stripping), since a
community or property-type string is not a person's name.
"""

from __future__ import annotations

import re

from rapidfuzz import fuzz


def normalize_text(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace."""
    cleaned = re.sub(r"[^\w\s]", "", text.lower())
    return " ".join(cleaned.split())


def text_similarity(first: str, second: str) -> float:
    """Fuzzy similarity between two free-text values, 0.0-1.0.

    Uses token_sort_ratio, which compares the words of each value irrespective
    of their order -- "Marina Tower" and "Tower Marina" score identically. Both
    values should already be normalize_text()'d.
    """
    return fuzz.token_sort_ratio(first, second) / 100.0


def texts_match(first: str, second: str, threshold: float) -> bool:
    """Decide whether two normalized free-text values refer to the same thing."""
    return text_similarity(first, second) >= threshold
