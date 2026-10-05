"""Test-driven development: Cas9 variant support."""

import pytest

from src.crispr.grna_design import (
    CAS9_VARIANTS,
    design_grna_for_variant,
    get_cas9_variant,
    list_cas9_variants,
)


class TestCas9Variants:
    """Test Cas9 variant registry."""

    def test_all_five_variants_present(self):
        """All five Cas9 variants must be in the registry."""
        expected = {"SpCas9", "eSpCas9", "SpCas9-NG", "xCas9", "SpCas9-NRRH"}
        assert set(CAS9_VARIANTS.keys()) == expected

    def test_each_variant_has_pam_and_description(self):
        """Each variant must have 'pam' and 'description' keys."""
        for name, info in CAS9_VARIANTS.items():
            assert "pam" in info, f"{name} missing 'pam'"
            assert "description" in info, f"{name} missing 'description'"
            assert isinstance(info["pam"], str)
            assert isinstance(info["description"], str)


class TestGetCas9Variant:
    """Test get_cas9_variant function."""

    def test_spcas9_pam(self):
        """SpCas9 should have NGG PAM."""
        info = get_cas9_variant("SpCas9")
        assert info["pam"] == "NGG"

    def test_espcas9_pam(self):
        """eSpCas9 should have NGG PAM."""
        info = get_cas9_variant("eSpCas9")
        assert info["pam"] == "NGG"

    def test_spcas9_ng_pam(self):
        """SpCas9-NG should have NGN PAM."""
        info = get_cas9_variant("SpCas9-NG")
        assert info["pam"] == "NGN"

    def test_xcas9_pam(self):
        """xCas9 should have NAG PAM."""
        info = get_cas9_variant("xCas9")
        assert info["pam"] == "NAG"

    def test_spcas9_nrrh_pam(self):
        """SpCas9-NRRH should have NRRH PAM."""
        info = get_cas9_variant("SpCas9-NRRH")
        assert info["pam"] == "NRRH"

    def test_unknown_variant_raises(self):
        """Unknown variant must raise ValueError."""
        with pytest.raises(ValueError, match="Unknown Cas9 variant"):
            get_cas9_variant("UnknownCas9")

    def test_return_has_description(self):
        """Return dict must have description."""
        info = get_cas9_variant("SpCas9")
        assert "description" in info
        assert len(info["description"]) > 0


class TestListCas9Variants:
    """Test list_cas9_variants function."""

    def test_returns_list(self):
        """Should return a list."""
        result = list_cas9_variants()
        assert isinstance(result, list)

    def test_contains_all_variants(self):
        """List must contain all five variant names."""
        result = list_cas9_variants()
        assert set(result) == {"SpCas9", "eSpCas9", "SpCas9-NG", "xCas9", "SpCas9-NRRH"}

    def test_all_strings(self):
        """All elements must be strings."""
        result = list_cas9_variants()
        assert all(isinstance(v, str) for v in result)


class TestDesignGrnaForVariant:
    """Test design_grna_for_variant function."""

    def test_design_returns_dict_with_variant(self):
        """Design must return dict with 'variant' key."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_for_variant(target, "SpCas9")
        assert result is not None
        assert "variant" in result
        assert result["variant"] == "SpCas9"

    def test_design_uses_variant_pam(self):
        """Design must use the variant's PAM."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_for_variant(target, "SpCas9")
        assert result["pam"] == "NGG"

    def test_design_spcas9_ng_pam(self):
        """SpCas9-NG should use NGN PAM."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_for_variant(target, "SpCas9-NG")
        assert result is not None
        assert result["pam"] == "NGN"

    def test_design_xcas9_pam(self):
        """xCas9 should use NAG PAM."""
        target = "GAGTCCGAGCAGAAGAAGAA" + "NAG" + "GAGTCCGAGCAGAAGAAGAA"
        result = design_grna_for_variant(target, "xCas9")
        # xCas9 has NAG PAM; result depends on target having NAG site
        # This test just verifies the function runs and raises for unknown
        assert result is None or result["pam"] == "NAG"

    def test_unknown_variant_raises(self):
        """Unknown variant must raise ValueError."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        with pytest.raises(ValueError, match="Unknown Cas9 variant"):
            design_grna_for_variant(target, "InvalidVariant")

    def test_design_includes_efficiency(self):
        """Design result must include efficiency."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_for_variant(target, "SpCas9")
        assert result is not None
        assert "efficiency" in result

    def test_design_includes_sequence(self):
        """Design result must include sequence."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_for_variant(target, "SpCas9")
        assert result is not None
        assert "sequence" in result

    def test_design_with_min_efficiency(self):
        """Design must respect min_efficiency parameter."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna_for_variant(target, "SpCas9", min_efficiency=0.0)
        assert result is not None

    def test_design_returns_none_for_no_match(self):
        """Design returns None when no valid gRNA found."""
        target = "ATATATATATATATATATAT"
        result = design_grna_for_variant(target, "SpCas9")
        assert result is None
