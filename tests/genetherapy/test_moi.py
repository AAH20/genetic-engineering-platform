"""Test-driven development: MOI and transduction efficiency calculations."""
import pytest

from src.genetherapy.vector_design import (
    calculate_moi,
    calculate_required_volume,
    calculate_transduction_efficiency,
)


# ---------------------------------------------------------------------------
# calculate_moi
# ---------------------------------------------------------------------------
class TestCalculateMoi:
    """Test multiplicity of infection calculation."""

    def test_returns_correct_moi(self):
        """MOI should equal vector_dose / cell_count."""
        result = calculate_moi(vector_dose=1e6, cell_count=1e5)
        assert result == pytest.approx(10.0)

    def test_zero_cell_count_raises_value_error(self):
        """Zero cell_count should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_moi(vector_dose=1e6, cell_count=0)


# ---------------------------------------------------------------------------
# calculate_transduction_efficiency
# ---------------------------------------------------------------------------
class TestCalculateTransductionEfficiency:
    """Test transduction efficiency based on MOI."""

    def test_returns_float_in_range(self):
        """Efficiency should be a float between 0 and 1."""
        result = calculate_transduction_efficiency(moi=1.0)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_moi_zero_returns_zero(self):
        """MOI of 0 should return efficiency of 0."""
        result = calculate_transduction_efficiency(moi=0.0)
        assert result == 0.0

    def test_high_moi_returns_above_09(self):
        """High MOI should return efficiency > 0.9."""
        result = calculate_transduction_efficiency(moi=5.0)
        assert result > 0.9


# ---------------------------------------------------------------------------
# calculate_required_volume
# ---------------------------------------------------------------------------
class TestCalculateRequiredVolume:
    """Test required injection volume calculation."""

    def test_returns_positive_float(self):
        """Volume should be a positive float."""
        result = calculate_required_volume(titer=1e12, target_dose=1e11, cell_count=1e6)
        assert isinstance(result, float)
        assert result > 0.0

    def test_zero_titer_raises_value_error(self):
        """Zero titer should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_required_volume(titer=0.0, target_dose=1e11, cell_count=1e6)
