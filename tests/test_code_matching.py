"""Tests for matching_utils.code_matching — reference code normalization and comparison."""

from __future__ import annotations

from matching_utils.code_matching import codes_match, normalize_code


class TestNormalizeCode:
    def test_uppercases(self):
        assert normalize_code("asic-2026-0007560") == "ASIC20260007560"

    def test_strips_dashes_and_spaces(self):
        assert normalize_code("ASIC 2026 0007560") == "ASIC20260007560"

    def test_strips_underscores(self):
        assert normalize_code("unit_no_203") == "UNITNO203"

    def test_empty_string_normalizes_to_empty(self):
        assert normalize_code("") == ""


class TestCodesMatch:
    def test_identical_codes_match(self):
        assert codes_match("ASIC-2026-0007560", "ASIC-2026-0007560") is True

    def test_differently_formatted_same_code_matches(self):
        assert codes_match("ASIC-2026-0007560", "asic 2026 0007560") is True

    def test_one_character_difference_does_not_match(self):
        assert codes_match("ASIC-2026-0007560", "ASIC-2026-0007561") is False

    def test_different_codes_do_not_match(self):
        assert codes_match("203", "204") is False
