"""
ID/passport number matching — normalization and comparison of Emirates ID and
passport numbers.

Pure value-to-value functions: callers extract ID/passport numbers from their
own document shapes (each app's extracted_data schema is its own concern) and
pass the resulting strings in here. See name_matching.py for the equivalent
utilities for person names.
"""

from __future__ import annotations

import re


def normalize_id_number(raw: str) -> str | None:
    """Strip non-digits; return the value only if exactly 15 digits remain."""
    digits = re.sub(r"\D", "", raw)
    return digits if len(digits) == 15 else None


def ids_match(id_a: str, id_b: str) -> bool:
    """Decide whether two normalized ID/passport numbers refer to the same document."""
    return id_a == id_b


def find_conflicting_values(values_by_source: dict[str, str]) -> dict[str, str] | None:
    """
    Given an exact-match field's extracted value keyed by source label (e.g. a
    document type), return the same mapping if more than one distinct value is
    present -- a conflict across sources that should all agree -- else None.
    """
    if len(set(values_by_source.values())) <= 1:
        return None
    return values_by_source
