"""Test-driven development: Flux Variability Analysis (FVA)."""
import pytest

from src.metabolic.fba import MetabolicModel


class TestFVA:
    """Test FVA (Flux Variability Analysis) on MetabolicModel."""

    def test_fva_returns_dict_with_min_max(self):
        """FVA should return a dict mapping reaction names to {'min', 'max'}."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.fva()
        assert isinstance(result, dict)
        assert "R1" in result
        assert "R2" in result
        assert "min" in result["R1"]
        assert "max" in result["R1"]
        assert "min" in result["R2"]
        assert "max" in result["R2"]

    def test_fva_min_lte_max(self):
        """FVA min should be <= max for all reactions."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.add_reaction("R3", {"C": -1.0, "D": 1.0})
        model.set_objective("R2")
        result = model.fva()
        for rxn_name, bounds in result.items():
            assert bounds["min"] <= bounds["max"], (
                f"{rxn_name}: min={bounds['min']} > max={bounds['max']}"
            )

    def test_fva_respects_bounds(self):
        """FVA results should respect reaction bounds."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0}, lower_bound=-5.0, upper_bound=10.0)
        model.add_reaction("R2", {"B": -1.0, "C": 1.0}, lower_bound=0.0, upper_bound=8.0)
        model.set_objective("R2")
        result = model.fva()
        for rxn_name, bounds in result.items():
            rxn = model.reactions[rxn_name]
            assert bounds["min"] >= rxn.lower_bound, (
                f"{rxn_name}: min={bounds['min']} < lower_bound={rxn.lower_bound}"
            )
            assert bounds["max"] <= rxn.upper_bound, (
                f"{rxn_name}: max={bounds['max']} > upper_bound={rxn.upper_bound}"
            )

    def test_fva_no_objective_raises(self):
        """FVA with no objective set should raise ValueError."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        with pytest.raises(ValueError):
            model.fva()

    def test_fva_empty_model_returns_empty(self):
        """FVA on empty model should return empty dict."""
        model = MetabolicModel()
        result = model.fva()
        assert result == {}
