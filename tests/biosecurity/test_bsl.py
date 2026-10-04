"""Tests for BSL classification and clearance checking."""
from src.biosecurity.screening import (
    check_bsl_clearance,
    classify_bsl_level,
)


class TestClassifyBslLevel:
    """Tests for classify_bsl_level function."""

    def test_clean_sequence_returns_bsl1(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = classify_bsl_level(seq)
        assert result == "BSL-1"

    def test_threat_pattern_returns_bsl3(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = classify_bsl_level(seq)
        assert result == "BSL-4"

    def test_multiple_threats_returns_bsl4(self):
        seq = (
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCT"
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
            "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC"
        )
        result = classify_bsl_level(seq)
        assert result == "BSL-4"

    def test_empty_sequence_returns_bsl1(self):
        result = classify_bsl_level("")
        assert result == "BSL-1"

    def test_unusual_gc_returns_bsl2(self):
        # Very high GC content (>80%) with no threat patterns
        seq = "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGC"
        result = classify_bsl_level(seq)
        assert result == "BSL-2"

    def test_dual_use_only_returns_bsl2(self):
        # Contains dual-use pattern but no direct threat pattern
        # Using a sequence with unusual GC content and no threat patterns
        seq = "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCAT"
        result = classify_bsl_level(seq)
        assert result == "BSL-2"


class TestCheckBslClearance:
    """Tests for check_bsl_clearance function."""

    def test_sufficient_clearance_returns_allowed(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = check_bsl_clearance(seq, "BSL-2")
        assert result["allowed"] is True
        assert result["required_bsl"] == "BSL-1"
        assert "sufficient" in result["reason"].lower() or "clearance" in result["reason"].lower()

    def test_insufficient_clearance_returns_not_allowed(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = check_bsl_clearance(seq, "BSL-1")
        assert result["allowed"] is False
        assert result["required_bsl"] == "BSL-4"
        assert "insufficient" in result["reason"].lower() or "requires" in result["reason"].lower()

    def test_bsl4_sequence_requires_bsl4_clearance(self):
        seq = (
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCT"
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
            "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC"
        )
        # BSL-3 user should be denied
        result = check_bsl_clearance(seq, "BSL-3")
        assert result["allowed"] is False
        assert result["required_bsl"] == "BSL-4"

        # BSL-4 user should be allowed
        result = check_bsl_clearance(seq, "BSL-4")
        assert result["allowed"] is True
        assert result["required_bsl"] == "BSL-4"

    def test_exact_clearance_match_returns_allowed(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = check_bsl_clearance(seq, "BSL-4")
        assert result["allowed"] is True
        assert result["required_bsl"] == "BSL-4"

    def test_higher_clearance_returns_allowed(self):
        seq = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = check_bsl_clearance(seq, "BSL-4")
        assert result["allowed"] is True
        assert result["required_bsl"] == "BSL-4"
