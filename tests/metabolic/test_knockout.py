"""Test-driven development: Knockout simulation for StrainOptimizer."""
import pytest

from src.metabolic.fba import (
    MetabolicModel,
    StrainOptimizer,
)


def _build_model():
    """Build a small metabolic model for knockout tests."""
    model = MetabolicModel()
    model.add_reaction("R1", {"A": -1.0, "B": 1.0}, upper_bound=10.0)
    model.add_reaction("R2", {"B": -1.0, "C": 1.0}, upper_bound=5.0)
    model.add_reaction("R3", {"B": -1.0, "D": 1.0}, upper_bound=8.0)
    model.add_reaction("R4", {"C": -1.0, "E": 1.0}, upper_bound=10.0)
    model.add_reaction("R5", {"E": -1.0}, upper_bound=10.0)
    model.add_reaction("R6", {"D": -1.0}, upper_bound=10.0)
    model.set_objective("R2")
    return model


class TestSimulateKnockout:
    """Test StrainOptimizer.simulate_knockout."""

    def test_simulate_knockout_invalid_reaction_raises(self):
        """simulate_knockout with non-existent reaction should raise ValueError."""
        model = _build_model()
        optimizer = StrainOptimizer(model)
        with pytest.raises(ValueError):
            optimizer.simulate_knockout("R_nonexistent")

    def test_simulate_knockout_returns_dict_with_correct_keys(self):
        """simulate_knockout returns dict with reaction, fluxes, objective_change."""
        model = _build_model()
        optimizer = StrainOptimizer(model)
        result = optimizer.simulate_knockout("R3")
        assert isinstance(result, dict)
        assert "reaction" in result
        assert "original_flux" in result
        assert "knockout_flux" in result
        assert "objective_change" in result

    def test_simulate_knockout_restores_original_bounds(self):
        """simulate_knockout should restore original bounds after simulation."""
        model = _build_model()
        original_lower = model.reactions["R3"].lower_bound
        original_upper = model.reactions["R3"].upper_bound
        optimizer = StrainOptimizer(model)
        optimizer.simulate_knockout("R3")
        assert model.reactions["R3"].lower_bound == original_lower
        assert model.reactions["R3"].upper_bound == original_upper

    def test_simulate_knockout_changes_flux_values(self):
        """simulate_knockout should change flux values when a supplier reaction is knocked out."""
        model = _build_model()
        optimizer = StrainOptimizer(model)
        # Get original flux for R2 (objective)
        result = optimizer.simulate_knockout("R1")
        # Knocking out R1 (supplies B) should reduce R2 flux
        assert result["knockout_flux"] != result["original_flux"]
        assert result["objective_change"] != 0.0


class TestCompareKnockouts:
    """Test StrainOptimizer.compare_knockouts."""

    def test_compare_knockouts_returns_sorted_list(self):
        """compare_knockouts should return results sorted by objective_change."""
        model = _build_model()
        optimizer = StrainOptimizer(model)
        results = optimizer.compare_knockouts(["R3", "R6"])
        assert isinstance(results, list)
        assert len(results) == 2
        # Should be sorted by objective_change (ascending)
        for i in range(len(results) - 1):
            assert results[i]["objective_change"] <= results[i + 1]["objective_change"]

    def test_compare_knockouts_empty_list_returns_empty(self):
        """compare_knockouts with empty list should return empty list."""
        model = _build_model()
        optimizer = StrainOptimizer(model)
        results = optimizer.compare_knockouts([])
        assert results == []
