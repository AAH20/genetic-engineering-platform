"""Test-driven development: prime editing gRNA design module."""
from src.crispr.grna_design import (
    calculate_prime_editing_efficiency,
    design_prime_editing_grna,
)


class TestDesignPrimeEditingGRna:
    """Test prime editing gRNA design."""

    def test_returns_dict_with_required_keys(self):
        """design_prime_editing_grna should return a dict with all required keys."""
        target = "GAGTCCGAGCAGAAGAAGAAGGGATCGATCGATCG"
        result = design_prime_editing_grna(target)
        assert result is not None
        assert isinstance(result, dict)
        assert "spacer" in result
        assert "rt_template" in result
        assert "pbs" in result
        assert "pam" in result
        assert "efficiency" in result

    def test_no_pam_returns_none(self):
        """design_prime_editing_grna with no PAM should return None."""
        target = "ATATATATATATATATATATATATATATATAT"
        result = design_prime_editing_grna(target)
        assert result is None

    def test_rt_template_is_reverse_complement(self):
        """RT template is reverse complement of target region downstream of nick."""
        target = "GAGTCCGAGCAGAAGAAGAAGGGATCGATCGATCG"
        result = design_prime_editing_grna(target)
        assert result is not None
        # The RT template should be a valid DNA sequence
        rt = result["rt_template"]
        assert len(rt) > 0
        assert all(c in "ACGT" for c in rt)
        # The RT template should be the reverse complement of some region in the target
        # We verify by checking that the reverse complement of rt appears in the target
        complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
        rc_rt = "".join(complement[c] for c in reversed(rt))
        assert rc_rt in target.upper()

    def test_spacer_is_20nt(self):
        """Spacer should be 20 nucleotides long."""
        target = "GAGTCCGAGCAGAAGAAGAAGGGATCGATCGATCG"
        result = design_prime_editing_grna(target)
        assert result is not None
        assert len(result["spacer"]) == 20

    def test_pbs_is_valid(self):
        """PBS should be a valid DNA sequence."""
        target = "GAGTCCGAGCAGAAGAAGAAGGGATCGATCGATCG"
        result = design_prime_editing_grna(target)
        assert result is not None
        pbs = result["pbs"]
        assert len(pbs) > 0
        assert all(c in "ACGT" for c in pbs)


class TestCalculatePrimeEditingEfficiency:
    """Test prime editing efficiency calculation."""

    def test_returns_float_in_range(self):
        """Efficiency should be a float between 0 and 1."""
        spacer = "GAGTCCGAGCAGAAGAAGAA"
        rt_template = "ATCGATCGAT"
        pbs = "GCTAGCTAGC"
        score = calculate_prime_editing_efficiency(spacer, rt_template, pbs)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_optimal_params_returns_high_score(self):
        """Optimal parameters should return a score > 0.5."""
        # Optimal: 20nt spacer with good GC, 10nt RT template, 10nt PBS with good GC
        spacer = "GAGTCCGAGCAGAAGAAGAA"
        rt_template = "ATCGATCGAT"
        pbs = "GCTAGCTAGC"
        score = calculate_prime_editing_efficiency(spacer, rt_template, pbs)
        assert score > 0.5

    def test_empty_spacer_returns_zero(self):
        """Empty spacer should return 0."""
        score = calculate_prime_editing_efficiency("", "ATCG", "GCTA")
        assert score == 0.0

    def test_short_pbs_returns_lower_score(self):
        """Shorter PBS should generally yield lower scores."""
        spacer = "GAGTCCGAGCAGAAGAAGAA"
        rt_template = "ATCGATCGAT"
        long_pbs = "GCTAGCTAGCTAGCTAGCTA"
        short_pbs = "GC"
        long_score = calculate_prime_editing_efficiency(spacer, rt_template, long_pbs)
        short_score = calculate_prime_editing_efficiency(spacer, rt_template, short_pbs)
        assert long_score > short_score
