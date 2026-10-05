"""TDD tests for secondary structure prediction."""
import pytest

from src.protein.protein_engineering import predict_secondary_structure


class TestPredictSecondaryStructure:
    """Test secondary structure prediction."""

    def test_returns_dict_with_required_keys(self):
        """predict_secondary_structure returns dict with required keys."""
        result = predict_secondary_structure("ACDEFGHIKLMNPQRSTVWY")
        assert isinstance(result, dict)
        assert "helix_fraction" in result
        assert "sheet_fraction" in result
        assert "coil_fraction" in result

    def test_fractions_sum_to_one(self):
        """predict_secondary_structure fractions sum to ~1.0."""
        result = predict_secondary_structure("ACDEFGHIKLMNPQRSTVWY")
        total = result["helix_fraction"] + result["sheet_fraction"] + result["coil_fraction"]
        assert total == pytest.approx(1.0)

    def test_helix_rich_sequence(self):
        """predict_secondary_structure with helix-rich sequence returns high helix_fraction."""
        seq = "AELMQ" * 10  # all helix-favoring
        result = predict_secondary_structure(seq)
        assert result["helix_fraction"] > 0.5

    def test_sheet_rich_sequence(self):
        """predict_secondary_structure with sheet-rich sequence returns high sheet_fraction."""
        seq = "VIYFW" * 10  # all sheet-favoring
        result = predict_secondary_structure(seq)
        assert result["sheet_fraction"] > 0.5

    def test_empty_sequence(self):
        """predict_secondary_structure with empty sequence returns zero fractions."""
        result = predict_secondary_structure("")
        assert result["helix_fraction"] == 0.0
        assert result["sheet_fraction"] == 0.0
        assert result["coil_fraction"] == 0.0
