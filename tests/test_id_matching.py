"""Tests for identity_matching.id_matching — ID/passport number normalization and comparison."""

from __future__ import annotations

from identity_matching.id_matching import find_conflicting_values, ids_match, normalize_id_number


class TestNormalizeIdNumber:
    def test_strips_separators_from_15_digits(self):
        assert normalize_id_number("784-1111-1111111-1") == "784111111111111"

    def test_rejects_wrong_digit_count(self):
        assert normalize_id_number("784-1111-11-1") is None

    def test_empty_string_returns_none(self):
        assert normalize_id_number("") is None

    def test_converts_arabic_indic_digits_to_western(self):
        assert normalize_id_number("٧٨٤-١١١١-١١١١١١١-١") == "784111111111111"

    def test_arabic_indic_and_western_forms_of_the_same_id_match(self):
        assert normalize_id_number("٧٨٤-١١١١-١١١١١١١-١") == normalize_id_number(
            "784-1111-1111111-1"
        )


class TestIdsMatch:
    def test_identical_ids_match(self):
        assert ids_match("784111111111111", "784111111111111") is True

    def test_different_ids_do_not_match(self):
        assert ids_match("784111111111111", "784222222222222") is False


class TestFindConflictingValues:
    def test_no_conflict_when_all_values_agree(self):
        values = {"id front": "784111111111111", "full id": "784111111111111"}
        assert find_conflicting_values(values) is None

    def test_no_conflict_with_a_single_source(self):
        assert find_conflicting_values({"id front": "784111111111111"}) is None

    def test_empty_mapping_has_no_conflict(self):
        assert find_conflicting_values({}) is None

    def test_conflict_when_values_differ(self):
        values = {"id front": "784111111111111", "passport": "784222222222222"}
        assert find_conflicting_values(values) == values
