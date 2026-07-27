"""
ID/passport number matching — extraction and normalization of Emirates ID and
passport numbers from extracted_data dicts produced by OCR/extraction
pipelines.

These are pure functions with no I/O: input is a raw string or a dict of
extracted fields; output is a cleaned, canonical value. See name_matching.py
for the equivalent utilities for person names.
"""

from __future__ import annotations

import re

# ── Shared helpers ────────────────────────────────────────────────────────────

def _nested_dict(fields: dict, key: str) -> dict:
    """Return fields[key] if it holds a dict, else an empty dict."""
    value = fields.get(key)
    return value if isinstance(value, dict) else {}


# ── Emirates ID number ────────────────────────────────────────────────────────

def normalize_id_number(raw: str) -> str | None:
    """Strip non-digits; return the value only if exactly 15 digits remain."""
    digits = re.sub(r"\D", "", raw)
    return digits if len(digits) == 15 else None


def extract_id_number(fields: dict) -> str | None:
    """
    Extract a normalized 15-digit Emirates ID number from an extracted_data dict.

    Tries the visible emirates_id / id_number field first (top-level and merged
    ID front sub-dict). Falls back to the last 15 digits of MRZ line 1 (TD1 format).
    """
    front = _nested_dict(fields, "front")
    raw = (
        fields.get("emirates_id")
        or fields.get("id_number")
        or front.get("emirates_id")
        or front.get("id_number")
    )
    if raw:
        normalized = normalize_id_number(str(raw))
        if normalized:
            return normalized
    back = _nested_dict(fields, "back")
    mrz = fields.get("machine_readable_zone") or back.get("machine_readable_zone")
    if mrz and isinstance(mrz, list) and mrz:
        digits = re.sub(r"\D", "", str(mrz[0]))
        if len(digits) >= 15:
            return digits[-15:]
    return None


# ── Passport number ───────────────────────────────────────────────────────────

def extract_passport_number(fields: dict) -> str | None:
    """
    Extract and normalize a passport number from an extracted_data dict.

    Tries the top level first, then the merged passport sub-dict (passport +
    passport_continue merge shape).
    """
    passport = _nested_dict(fields, "passport")
    raw = (
        fields.get("passport_number")
        or fields.get("passport_no")
        or fields.get("passport_num")
        or passport.get("passport_number")
        or passport.get("passport_no")
        or passport.get("passport_num")
    )
    if not raw:
        return None
    return re.sub(r"\s+", "", str(raw)).upper()
