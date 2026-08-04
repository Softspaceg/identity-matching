"""
Name matching — normalization and fuzzy comparison of person names.

Pure value-to-value functions: callers extract names from their own document
shapes (each app's extracted_data schema is its own concern) and pass the
resulting strings in here. This is the single place to change how names are
compared — the normalization rules, the similarity algorithm, the decision
threshold — with the change taking effect in every consuming app.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rapidfuzz import fuzz

HONORIFIC_TITLES = frozenset(
    {
        "mr",
        "mrs",
        "ms",
        "miss",
        "mx",
        "dr",
        "prof",
        "eng",
        "sheikh",
        "sheikha",
        "sir",
        "madam",
    }
)


def normalize_name(name: str) -> str:
    """Lowercase, remove punctuation, strip honorific titles, collapse whitespace."""
    cleaned = re.sub(r"[^\w\s]", "", name.lower())
    tokens = [token for token in cleaned.split() if token not in HONORIFIC_TITLES]
    return " ".join(tokens)


def name_similarity(first: str, second: str) -> float:
    """Fuzzy similarity between two names, 0.0–1.0.

    Uses token_sort_ratio, which compares the words of each name irrespective
    of their order — documents list the same person as "Mengyi Pei", "PEI
    MENGYI", or "Pei, Mengyi", and all three are the same identity. A
    character-sequence ratio scores those as different people.

    Both names should already be normalize_name()'d.
    """
    return fuzz.token_sort_ratio(first, second) / 100.0


def names_match(first: str, second: str, threshold: float) -> bool:
    """Decide whether two normalized names refer to the same person."""
    return name_similarity(first, second) >= threshold


@dataclass
class NameMatch:
    """The best-scoring candidate name found for a target, with its similarity score."""

    name: str
    score: float


def best_name_match(target_name: str, candidate_names: list[str]) -> NameMatch | None:
    """Return the candidate closest to target_name, or None if there are no candidates."""
    if not candidate_names:
        return None
    return max(
        (
            NameMatch(candidate, name_similarity(target_name, candidate))
            for candidate in candidate_names
        ),
        key=lambda match: match.score,
    )
