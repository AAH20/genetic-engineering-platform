"""Test-driven development: base editing gRNA design module."""
from src.crispr.grna_design import (
    calculate_base_editing_efficiency,
    design_base_editor_grna,
)


class TestDesignBaseEditorGRNATests:
    """Test design_base_editor_grna function."""

    def test_cbe_returns_dict_with_editing_window(self):
        """CBE design should return dict with editing_window key."""
        # Target with C in editing window (positions 4-8) and NGG PAM
        target = "ATGCGTCTCATCGAGTCCGAGCAGAAGAAGAA" + "GGG"
        result = design_base_editor_grna(target, editor_type="CBE", pam="NGG")
        assert result is not None
        assert isinstance(result, dict)
        assert "editing_window" in result
        assert "sequence" in result
        assert "efficiency" in result
        assert "pam" in result
        assert "editor_type" in result
        assert "conversion_type" in result

    def test_abe_returns_dict_with_conversion_type_a_to_g(self):
        """ABE design should return dict with conversion_type='A->G'."""
        # Target with A in editing window (positions 4-7) and NGG PAM
        target = "GAGTAGGAGCAGAAGAAGAA" + "GGG"
        result = design_base_editor_grna(target, editor_type="ABE", pam="NGG")
        assert result is not None
        assert isinstance(result, dict)
        assert result["conversion_type"] == "A->G"

    def test_no_editable_base_returns_none(self):
        """Design with no editable base in window should return None."""
        # Target with no C in editing window for CBE
        target = "GAGTGTGAGCAGAAGAAGAA" + "GGG"
        result = design_base_editor_grna(target, editor_type="CBE", pam="NGG")
        assert result is None


class TestCalculateBaseEditingEfficiencyTests:
    """Test calculate_base_editing_efficiency function."""

    def test_returns_float_in_range(self):
        """Efficiency should be a float between 0 and 1."""
        seq = "GAGTCCGAGCAGAAGAAGAA"
        score = calculate_base_editing_efficiency(seq, editor_type="CBE")
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_cbe_checks_c_in_window(self):
        """CBE efficiency should be higher when C is present in editing window."""
        # Sequence with C in editing window (positions 4-8)
        seq_with_c = "GAGTCCGAGCAGAAGAAGAA"
        # Sequence without C in editing window
        seq_without_c = "GAGTGTGAGCAGAAGAAGAA"
        score_with = calculate_base_editing_efficiency(seq_with_c, editor_type="CBE")
        score_without = calculate_base_editing_efficiency(seq_without_c, editor_type="CBE")
        assert score_with > score_without

    def test_abe_checks_a_in_window(self):
        """ABE efficiency should be higher when A is present in editing window."""
        # Sequence with A in editing window (positions 4-7)
        seq_with_a = "GAGTAGGAGCAGAAGAAGAA"
        # Sequence without A in editing window
        seq_without_a = "GAGTGGGAGCAGAAGAAGAA"
        score_with = calculate_base_editing_efficiency(seq_with_a, editor_type="ABE")
        score_without = calculate_base_editing_efficiency(seq_without_a, editor_type="ABE")
        assert score_with > score_without
