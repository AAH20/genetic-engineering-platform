"""Test-driven development: batch gRNA design functions."""
from src.crispr.grna_design import design_grna_batch, design_grna_multiple_pams


class TestDesignGrnaBatch:
    """Test design_grna_batch for multiple targets."""

    def test_empty_list_returns_empty(self):
        """Empty target list should return empty list."""
        result = design_grna_batch([])
        assert result == []

    def test_single_target_returns_one_result(self):
        """Single target should return list with one result."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_batch([target])
        assert len(result) == 1
        assert result[0] is not None
        assert "sequence" in result[0]
        assert "efficiency" in result[0]

    def test_multiple_targets_returns_all_results(self):
        """Multiple targets should return results for each."""
        targets = [
            "GAGTCCGAGCAGAAGAAGAAGGG",
            "GAGTCCGAGCAGAAGAAGAACGG",
            "GAGTCCGAGCAGAAGAAGAATGG",
        ]
        result = design_grna_batch(targets)
        assert len(result) == 3
        for r in result:
            assert r is not None
            assert "sequence" in r
            assert "efficiency" in r

    def test_invalid_targets_return_none(self):
        """Invalid targets should produce None in results."""
        targets = [
            "GAGTCCGAGCAGAAGAAGAAGGG",
            "ATATATATATATATATATAT",
            "GAGTCCGAGCAGAAGAAGAACGG",
        ]
        result = design_grna_batch(targets)
        assert len(result) == 3
        assert result[0] is not None
        assert result[1] is None
        assert result[2] is not None

    def test_custom_pam(self):
        """Batch design should accept custom PAM."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_batch([target], pam="NGG")
        assert len(result) == 1
        assert result[0] is not None
        assert result[0]["pam"] == "NGG"

    def test_min_efficiency_threshold(self):
        """Batch design should respect min_efficiency threshold."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_batch([target], min_efficiency=0.0)
        assert len(result) == 1
        assert result[0] is not None


class TestDesignGrnaMultiplePams:
    """Test design_grna_multiple_pams for multiple PAM variants."""

    def test_empty_pams_returns_empty_dict(self):
        """Empty PAM list should return empty dict."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_multiple_pams(target, [])
        assert result == {}

    def test_returns_dict_with_all_pam_keys(self):
        """Result should have a key for each PAM."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        pams = ["NGG", "NAG", "NNAGAA"]
        result = design_grna_multiple_pams(target, pams)
        assert isinstance(result, dict)
        for pam in pams:
            assert pam in result

    def test_single_pam(self):
        """Single PAM should return dict with one entry."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_multiple_pams(target, ["NGG"])
        assert len(result) == 1
        assert "NGG" in result
        assert result["NGG"] is not None
        assert "sequence" in result["NGG"]

    def test_multiple_pams_all_valid(self):
        """Multiple valid PAMs should all produce results."""
        # Target has both NGG and NAG PAM sites
        target = "GAGTCCGAGCAGAAGAAGAAGGGGAGTCCGAGCAGAAGAAGAAAAG"
        pams = ["NGG", "NAG"]
        result = design_grna_multiple_pams(target, pams)
        assert len(result) == 2
        for pam in pams:
            assert result[pam] is not None
            assert "sequence" in result[pam]
            assert result[pam]["pam"] == pam
