"""Tests for matching_utils.name_matching — normalization and fuzzy name comparison."""

from __future__ import annotations

from matching_utils.name_matching import (
    best_name_match,
    name_similarity,
    names_match,
    normalize_name,
)


class TestNormalizeName:
    def test_lowercases_strips_punctuation_collapses_whitespace(self):
        assert normalize_name("  John   O'Smith! ") == "john osmith"

    def test_strips_leading_honorific(self):
        assert normalize_name("Mr. Raza Abbas Rizvi") == "raza abbas rizvi"

    def test_strips_honorific_anywhere(self):
        assert normalize_name("Dr Jane Smith Prof") == "jane smith"

    def test_honorific_only_matches_whole_token(self):
        assert normalize_name("Mrs Drake") == "drake"


class TestNameSimilarity:
    def test_word_order_insensitive(self):
        assert name_similarity("mengyi pei", "pei mengyi") == 1.0

    def test_identical_names_score_1(self):
        assert name_similarity("john smith", "john smith") == 1.0

    def test_different_names_score_low(self):
        assert name_similarity("john smith", "jane doe") < 0.5


class TestNamesMatch:
    def test_respects_threshold(self):
        assert names_match("mengyi pei", "pei mengyi", threshold=0.85) is True
        assert names_match("john smith", "jane doe", threshold=0.85) is False

    def test_boundary_is_inclusive(self):
        score = name_similarity("john smith", "john smyth")
        assert names_match("john smith", "john smyth", threshold=score) is True


class TestBestNameMatch:
    def test_picks_highest_scoring_candidate(self):
        best = best_name_match("john smith", ["jane doe", "john smith", "smith john"])
        assert best is not None
        assert best.name in {"john smith", "smith john"}
        assert best.score == 1.0

    def test_returns_none_for_empty_candidates(self):
        assert best_name_match("john smith", []) is None
