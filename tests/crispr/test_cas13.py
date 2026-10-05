"""TDD tests for Cas13 RNA-targeting gRNA design."""
from src.crispr.grna_design import design_grna_cas13, validate_cas13_grna


class TestCas13Validation:
    """Test Cas13 gRNA validation."""

    def test_valid_28nt_sequence(self):
        assert validate_cas13_grna("GAGUCCGAGCAGAAGAAGAA" + "ACGU") is True

    def test_valid_24nt_sequence(self):
        assert validate_cas13_grna("GAGUCCGAGCAGAAGAAGAA" + "ACGU") is True

    def test_too_short(self):
        assert validate_cas13_grna("GAGUCCGAGCAGAAGAAG") is False

    def test_too_long(self):
        assert validate_cas13_grna("GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUACGU") is False

    def test_invalid_characters(self):
        assert validate_cas13_grna("GAGUCCGAGCAGAAGAAGAA" + "ACGX") is False

    def test_empty(self):
        assert validate_cas13_grna("") is False

    def test_contains_t(self):
        # Cas13 targets RNA, so T should not be present
        assert validate_cas13_grna("GAGTCCGAGCAGAAGAAGAA" + "ACGU") is False


class TestCas13Design:
    """Test Cas13 gRNA design with PFS."""

    def test_design_with_pfs(self):
        # Cas13 uses 3' PFS (protospacer flanking site)
        target = "GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUAC" + "A"
        result = design_grna_cas13(target)
        assert result is not None
        assert result["pfs"] == "A"

    def test_design_with_pfs_c(self):
        target = "GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUAC" + "C"
        result = design_grna_cas13(target)
        assert result is not None

    def test_design_with_pfs_g(self):
        target = "GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUAC" + "G"
        result = design_grna_cas13(target)
        assert result is not None

    def test_no_pfs_returns_none(self):
        # Target where position 28 is "C" (doesn't match default PFS "A")
        target = "GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUC"
        result = design_grna_cas13(target)
        assert result is None

    def test_empty_target(self):
        assert design_grna_cas13("") is None

    def test_result_has_efficiency(self):
        target = "GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUAC" + "A"
        result = design_grna_cas13(target)
        assert "efficiency" in result
        assert 0.0 <= result["efficiency"] <= 1.0

    def test_result_has_off_targets(self):
        target = "GAGUCCGAGCAGAAGAAGAA" + "ACGUACGUAC" + "A"
        result = design_grna_cas13(target)
        assert "off_targets" in result
        assert isinstance(result["off_targets"], list)
