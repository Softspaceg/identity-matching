"""Tests for identity_matching.id_matching — ID/passport number extraction."""

from __future__ import annotations

from identity_matching.id_matching import (
    extract_id_number,
    extract_passport_number,
    fields_id_match,
    find_conflicting_values,
    ids_match,
    normalize_id_number,
)


class TestNormalizeIdNumber:
    def test_strips_separators_from_15_digits(self):
        assert normalize_id_number("784-1111-1111111-1") == "784111111111111"

    def test_rejects_wrong_digit_count(self):
        assert normalize_id_number("784-1111-11-1") is None

    def test_empty_string_returns_none(self):
        assert normalize_id_number("") is None


class TestExtractIdNumber:
    def test_top_level_emirates_id(self):
        assert extract_id_number({"emirates_id": "784-1111-1111111-1"}) == "784111111111111"

    def test_top_level_id_number_field(self):
        assert extract_id_number({"id_number": "784111111111111"}) == "784111111111111"

    def test_nested_under_merged_front(self):
        fields = {"front": {"emirates_id": "784-1111-1111111-1"}, "back": {}}
        assert extract_id_number(fields) == "784111111111111"

    def test_mrz_fallback_from_top_level(self):
        fields = {"machine_readable_zone": ["IDARE784111111111111<<<<<<<<<<<<<"]}
        assert extract_id_number(fields) == "784111111111111"

    def test_mrz_fallback_from_merged_back(self):
        fields = {"back": {"machine_readable_zone": ["IDARE784111111111111<<<<<<<<<<<<<"]}}
        assert extract_id_number(fields) == "784111111111111"

    def test_malformed_id_number_is_rejected_not_returned_raw(self):
        """A non-15-digit value should not be returned raw -- garbage in, None out."""
        assert extract_id_number({"emirates_id": "12345"}) is None

    def test_returns_none_when_nothing_found(self):
        assert extract_id_number({"area": "100 sqm"}) is None


class TestExtractPassportNumber:
    def test_top_level_passport_number(self):
        assert extract_passport_number({"passport_number": " ab123456 "}) == "AB123456"

    def test_top_level_passport_no_alias(self):
        assert extract_passport_number({"passport_no": "ab123456"}) == "AB123456"

    def test_nested_under_merged_passport(self):
        """passport + passport_continue merge shape nests the primary page under 'passport'."""
        fields = {
            "passport": {"passport_number": "ab123456"},
            "passport_continue": {"visa_pages": []},
        }
        assert extract_passport_number(fields) == "AB123456"

    def test_top_level_takes_priority_over_nested(self):
        fields = {"passport_number": "top123", "passport": {"passport_number": "nested456"}}
        assert extract_passport_number(fields) == "TOP123"

    def test_returns_none_when_nothing_found(self):
        assert extract_passport_number({"area": "100 sqm"}) is None


class TestIdsMatch:
    def test_identical_ids_match(self):
        assert ids_match("784111111111111", "784111111111111") is True

    def test_different_ids_do_not_match(self):
        assert ids_match("784111111111111", "784222222222222") is False


class TestFieldsIdMatch:
    def test_matches_on_equal_extracted_ids(self):
        front = {"emirates_id": "784-1111-1111111-1"}
        back = {"machine_readable_zone": ["IDARE784111111111111<<<<<<<<<<<<<"]}
        assert fields_id_match(front, back) is True

    def test_does_not_match_different_ids(self):
        front = {"emirates_id": "784-1111-1111111-1"}
        back = {"emirates_id": "784-2222-2222222-2"}
        assert fields_id_match(front, back) is False

    def test_returns_none_when_either_side_has_no_id(self):
        front = {"emirates_id": "784-1111-1111111-1"}
        back = {"card_number": "123"}
        assert fields_id_match(front, back) is None


class TestFindConflictingValues:
    def test_no_conflict_when_all_values_agree(self):
        assert find_conflicting_values({"id front": "784111111111111", "full id": "784111111111111"}) is None

    def test_no_conflict_with_a_single_source(self):
        assert find_conflicting_values({"id front": "784111111111111"}) is None

    def test_empty_mapping_has_no_conflict(self):
        assert find_conflicting_values({}) is None

    def test_conflict_when_values_differ(self):
        values = {"id front": "784111111111111", "passport": "784222222222222"}
        assert find_conflicting_values(values) == values
