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
    """Convert Arabic-Indic digits to Western, strip remaining non-digits,
    and return the value only if exactly 15 digits remain.

    The Arabic-Indic conversion matters because Python's `\\D` (non-digit)
    already treats Arabic-Indic digits as digits, so they'd otherwise pass
    the length check but never equal the Western-digit spelling of the same
    number -- documents extracted with Arabic-Indic numerals wouldn't match
    the same ID written in Western digits."""
    western = raw.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    digits = re.sub(r"\D", "", western)
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
