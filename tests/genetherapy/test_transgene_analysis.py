"""Test-driven development: Transgene sequence analysis module."""

from src.genetherapy.vector_design import (
    analyze_transgene_sequence,
    calculate_immunogenicity_risk,
)


# ---------------------------------------------------------------------------
# analyze_transgene_sequence
# ---------------------------------------------------------------------------
class TestAnalyzeTransgeneSequence:
    """Test transgene sequence analysis."""

    def test_returns_dict_with_required_keys(self):
        """Returns dict with gc_content, has_polyA, has_cryptic_splice, orf_length, warnings."""
        result = analyze_transgene_sequence("ATGCATGCATGC")
        assert isinstance(result, dict)
        assert "gc_content" in result
        assert "has_polyA" in result
        assert "has_cryptic_splice" in result
        assert "orf_length" in result
        assert "warnings" in result

    def test_polya_signal_detected(self):
        """Sequence with AATAAA polyA signal should return has_polyA=True."""
        result = analyze_transgene_sequence("ATGCATGCATGCATGCATGCAATAAATAG")
        assert result["has_polyA"] is True

    def test_normal_gc_content_in_range(self):
        """Sequence with normal GC content should return gc_content in [0.3, 0.7]."""
        result = analyze_transgene_sequence("ATGCATGCATGCATGCATGC")
        assert 0.3 <= result["gc_content"] <= 0.7

    def test_gc_content_calculation(self):
        """GC content should be calculated correctly."""
        # 12 bases: 6 G/C, 6 A/T -> 0.5
        result = analyze_transgene_sequence("GGCCATGCATAT")
        assert abs(result["gc_content"] - 0.5) < 0.01

    def test_no_polya_signal(self):
        """Sequence without polyA signal should return has_polyA=False."""
        result = analyze_transgene_sequence("ATGCATGCATGCATGCATGC")
        assert result["has_polyA"] is False

    def test_cryptic_splice_site_detected(self):
        """Sequence with cryptic splice site (GT...AG) should return has_cryptic_splice=True."""
        # GT at start, AG at end with enough spacing
        seq = "GT" + "ATGC" * 20 + "AG"
        result = analyze_transgene_sequence(seq)
        assert result["has_cryptic_splice"] is True

    def test_no_cryptic_splice_site(self):
        """Sequence without cryptic splice site should return has_cryptic_splice=False."""
        result = analyze_transgene_sequence("ATGCATGCATGCATGCATGC")
        assert result["has_cryptic_splice"] is False

    def test_orf_length_positive(self):
        """ORF length should be a positive integer for a valid sequence."""
        result = analyze_transgene_sequence("ATGAAATAA")
        assert isinstance(result["orf_length"], int)
        assert result["orf_length"] > 0

    def test_warnings_is_list(self):
        """Warnings should be a list."""
        result = analyze_transgene_sequence("ATGCATGCATGCATGCATGC")
        assert isinstance(result["warnings"], list)

    def test_high_gc_warning(self):
        """High GC content should generate a warning."""
        result = analyze_transgene_sequence("GCGCGCGCGCGCGCGCGCGC")
        assert len(result["warnings"]) > 0

    def test_low_gc_warning(self):
        """Low GC content should generate a warning."""
        result = analyze_transgene_sequence("ATATATATATATATATATAT")
        assert len(result["warnings"]) > 0


# ---------------------------------------------------------------------------
# calculate_immunogenicity_risk
# ---------------------------------------------------------------------------
class TestCalculateImmunogenicityRisk:
    """Test immunogenicity risk calculation."""

    def test_returns_float_in_range(self):
        """Should return a float between 0 and 1."""
        result = calculate_immunogenicity_risk("ATGCATGCATGCATGCATGC", "AAV9")
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_high_cpg_returns_high_risk(self):
        """High CpG content should return risk > 0.5."""
        seq = "CG" * 50
        result = calculate_immunogenicity_risk(seq, "AAV2")
        assert result > 0.5

    def test_low_cpg_returns_low_risk(self):
        """Low CpG content should return risk < 0.5."""
        seq = "AT" * 50
        result = calculate_immunogenicity_risk(seq, "AAV9")
        assert result < 0.5
