"""Test-driven development: paired gRNA design for deletions and nickase strategies."""
from src.crispr.grna_design import (
    calculate_paired_efficiency,
    design_paired_grna,
)


class TestPairedGRNADesign:
    """Test paired gRNA design for deletions and nickase strategies."""

    def test_design_paired_grna_returns_dict_with_grna1_and_grna2(self):
        """design_paired_grna should return a dict containing grna1 and grna2."""
        # Target with multiple NGG PAM sites spaced ~100 bp apart
        target = (
            "GAGTCCGAGCAGAAGAAGAA" + "GG" + "A" * 46 +
            "GAGTCCGAGCAGAAGAAGAA" + "GG" + "A" * 46 +
            "GAGTCCGAGCAGAAGAAGAA" + "GG"
        )
        result = design_paired_grna(target, pam="NGG", min_distance=50, max_distance=200)
        assert result is not None
        assert "grna1" in result
        assert "grna2" in result
        assert "distance" in result
        assert "efficiency" in result
        assert "pam" in result

    def test_design_paired_grna_no_valid_pair_returns_none(self):
        """design_paired_grna should return None when no valid pair exists."""
        # Target with only one PAM site — no pair possible
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_paired_grna(target, pam="NGG", min_distance=50, max_distance=200)
        assert result is None

    def test_design_paired_grna_distance_within_range(self):
        """Paired gRNA distance should be within the specified range."""
        target = (
            "GAGTCCGAGCAGAAGAAGAA" + "GG" + "A" * 46 +
            "GAGTCCGAGCAGAAGAAGAA" + "GG" + "A" * 46 +
            "GAGTCCGAGCAGAAGAAGAA" + "GG"
        )
        result = design_paired_grna(target, pam="NGG", min_distance=50, max_distance=200)
        assert result is not None
        assert 50 <= result["distance"] <= 200


class TestPairedEfficiency:
    """Test paired gRNA efficiency calculation."""

    def test_calculate_paired_efficiency_returns_float_in_range(self):
        """calculate_paired_efficiency should return a float between 0 and 1."""
        grna1 = "GAGTCCGAGCAGAAGAAGAA"
        grna2 = "GAGTCCGAGCAGAAGAAGAA"
        score = calculate_paired_efficiency(grna1, grna2, distance=100)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_calculate_paired_efficiency_optimal_distance_high_score(self):
        """Optimal distance should yield a score greater than 0.5."""
        grna1 = "GAGTCCGAGCAGAAGAAGAA"
        grna2 = "GAGTCCGAGCAGAAGAAGAA"
        score = calculate_paired_efficiency(grna1, grna2, distance=100)
        assert score > 0.5
