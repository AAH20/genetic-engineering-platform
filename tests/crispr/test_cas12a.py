"""TDD tests for Cas12a (Cpf1) gRNA design."""
from src.crispr.grna_design import design_grna_cas12a, validate_cas12a_grna


class TestCas12aValidation:
    """Test Cas12a gRNA validation."""

    def test_valid_24nt_sequence(self):
        assert validate_cas12a_grna("GAGTCCGAGCAGAAGAAGAA" + "ACGT") is True

    def test_valid_20nt_sequence(self):
        assert validate_cas12a_grna("GAGTCCGAGCAGAAGAAGAA") is True

    def test_too_short(self):
        assert validate_cas12a_grna("GAGTCCGAGCAGAAGAAG") is False

    def test_too_long(self):
        assert validate_cas12a_grna("GAGTCCGAGCAGAAGAAGAA" + "ACGTACGTACGT") is False

    def test_invalid_characters(self):
        assert validate_cas12a_grna("GAGTCCGAGCAGAAGAAGAA" + "ACGX") is False

    def test_empty(self):
        assert validate_cas12a_grna("") is False


class TestCas12aDesign:
    """Test Cas12a gRNA design with TTTV PAM."""

    def test_design_with_tttv_pam(self):
        # Cas12a uses 5' TTTV PAM
        target = "TTTG" + "GAGTCCGAGCAGAAGAAGAA" + "ACGT"
        result = design_grna_cas12a(target)
        assert result is not None
        assert result["pam"] == "TTTV"
        assert len(result["sequence"]) == 20

    def test_design_with_ttta_pam(self):
        target = "TTTA" + "GAGTCCGAGCAGAAGAAGAA" + "ACGT"
        result = design_grna_cas12a(target)
        assert result is not None

    def test_design_with_tttg_pam(self):
        target = "TTTG" + "GAGTCCGAGCAGAAGAAGAA" + "ACGT"
        result = design_grna_cas12a(target)
        assert result is not None

    def test_no_pam_returns_none(self):
        target = "GAGTCCGAGCAGAAGAAGAA" + "ACGT"
        result = design_grna_cas12a(target)
        assert result is None

    def test_empty_target(self):
        assert design_grna_cas12a("") is None

    def test_result_has_efficiency(self):
        target = "TTTG" + "GAGTCCGAGCAGAAGAAGAA" + "ACGT"
        result = design_grna_cas12a(target)
        assert "efficiency" in result
        assert 0.0 <= result["efficiency"] <= 1.0

    def test_result_has_off_targets(self):
        target = "TTTG" + "GAGTCCGAGCAGAAGAAGAA" + "ACGT"
        result = design_grna_cas12a(target)
        assert "off_targets" in result
        assert isinstance(result["off_targets"], list)
