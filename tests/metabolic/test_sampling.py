"""Test-driven development: Flux Sampling (hit-and-run) and flux range."""
import pytest

from src.metabolic.fba import MetabolicModel


def _build_toy_model():
    """Build a small toy metabolic model for sampling tests."""
    model = MetabolicModel()
    model.add_reaction("R1", {"A": -1.0, "B": 1.0}, lower_bound=0.0, upper_bound=10.0)
    model.add_reaction("R2", {"B": -1.0, "C": 1.0}, lower_bound=0.0, upper_bound=8.0)
    model.add_reaction("R3", {"C": -1.0, "D": 1.0}, lower_bound=0.0, upper_bound=5.0)
    model.add_reaction("R4", {"D": -1.0}, lower_bound=0.0, upper_bound=10.0)
    model.set_objective("R2")
    return model


class TestSampleFluxSpace:
    """Test MetabolicModel.sample_flux_space (hit-and-run sampling)."""

    def test_sample_zero_returns_empty(self):
        """sample_flux_space(n_samples=0) should return an empty list."""
        model = _build_toy_model()
        result = model.sample_flux_space(n_samples=0)
        assert result == []

    def test_sample_returns_list_of_dicts(self):
        """sample_flux_space should return a list of flux dicts."""
        model = _build_toy_model()
        result = model.sample_flux_space(n_samples=5, seed=42)
        assert isinstance(result, list)
        assert len(result) == 5
        for point in result:
            assert isinstance(point, dict)
            for rxn_name in model.reactions:
                assert rxn_name in point

    def test_sample_reproducible_with_seed(self):
        """sample_flux_space with the same seed should produce identical results."""
        model = _build_toy_model()
        result1 = model.sample_flux_space(n_samples=10, seed=123)
        result2 = model.sample_flux_space(n_samples=10, seed=123)
        assert result1 == result2

    def test_sample_respects_bounds(self):
        """All sampled flux values should respect reaction bounds."""
        model = _build_toy_model()
        result = model.sample_flux_space(n_samples=20, seed=42)
        for point in result:
            for rxn_name, flux in point.items():
                rxn = model.reactions[rxn_name]
                assert flux >= rxn.lower_bound - 1e-9, (
                    f"{rxn_name}: flux {flux} < lower_bound {rxn.lower_bound}"
                )
                assert flux <= rxn.upper_bound + 1e-9, (
                    f"{rxn_name}: flux {flux} > upper_bound {rxn.upper_bound}"
                )


class TestGetFluxRange:
    """Test MetabolicModel.get_flux_range (FVA-based min/max)."""

    def test_get_flux_range_returns_dict_with_min_max(self):
        """get_flux_range should return a dict with 'min' and 'max' keys."""
        model = _build_toy_model()
        result = model.get_flux_range("R1")
        assert isinstance(result, dict)
        assert "min" in result
        assert "max" in result

    def test_get_flux_range_min_lte_max(self):
        """get_flux_range min should be <= max."""
        model = _build_toy_model()
        result = model.get_flux_range("R1")
        assert result["min"] <= result["max"]

    def test_get_flux_range_invalid_reaction_raises(self):
        """get_flux_range for a non-existent reaction should raise ValueError."""
        model = _build_toy_model()
        with pytest.raises(ValueError):
            model.get_flux_range("R_nonexistent")
