"""Tests for matching_utils.text_matching — normalization and fuzzy free-text comparison."""

from __future__ import annotations

from matching_utils.text_matching import normalize_text, text_similarity, texts_match


class TestNormalizeText:
    def test_lowercases_strips_punctuation_collapses_whitespace(self):
        assert normalize_text("  Marina, Tower!  ") == "marina tower"

    def test_does_not_strip_honorific_like_tokens(self):
        assert normalize_text("Dr Villas Community") == "dr villas community"


class TestTextSimilarity:
    def test_word_order_insensitive(self):
        assert text_similarity("marina tower", "tower marina") == 1.0

    def test_identical_values_score_1(self):
        assert text_similarity("wadi al safa 5", "wadi al safa 5") == 1.0

    def test_different_values_score_low(self):
        assert text_similarity("wadi al safa 5", "dubai marina") < 0.5


class TestTextsMatch:
    def test_respects_threshold(self):
        assert texts_match("marina tower", "tower marina", threshold=0.85) is True
        assert texts_match("wadi al safa 5", "dubai marina", threshold=0.85) is False

    def test_boundary_is_inclusive(self):
        score = text_similarity("marina tower", "marina towers")
        assert texts_match("marina tower", "marina towers", threshold=score) is True
