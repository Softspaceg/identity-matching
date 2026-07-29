"""
Code matching — normalization and exact comparison of alphanumeric reference
codes (contract numbers, unit numbers, plate numbers, etc.).

Pure value-to-value functions: callers extract the value from their own
document shape and pass the resulting strings in here. See name_matching.py
for the equivalent utilities for person names.

Unlike name_matching, comparison here is exact after normalization, not
fuzzy: a reference code that's off by one character identifies a different
record, not a "close enough" match — the same document, reformatted, should
still normalize to the same code.
"""

from __future__ import annotations

import re


def normalize_code(raw: str) -> str:
    """Uppercase; strip whitespace, dashes, and underscores. Lets two codes be
    compared even if one has extra spaces or different separator placement
    (e.g. "ASIC-2026-0007560" vs "ASIC 2026 0007560")."""
    return re.sub(r"[\s\-_]+", "", raw.upper())


def codes_match(code_a: str, code_b: str) -> bool:
    """Decide whether two normalized codes are the same value."""
    return normalize_code(code_a) == normalize_code(code_b)
