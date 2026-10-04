"""Test-driven development: Metabolic Engineering module."""
import pytest

from src.metabolic.fba import (
    MetabolicModel,
    PathwayDesigner,
    StrainOptimizer,
)


class TestMetabolicModel:
    """Test MetabolicModel class."""

    def test_add_reaction(self):
        """Adding a reaction should store it in the model."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        assert "R1" in model.reactions
        assert model.reactions["R1"].stoichiometry == {"A": -1.0, "B": 1.0}

    def test_add_reaction_with_bounds(self):
        """Adding a reaction with custom bounds should store them."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0}, lower_bound=-10.0, upper_bound=10.0)
        assert model.reactions["R1"].lower_bound == -10.0
        assert model.reactions["R1"].upper_bound == 10.0

    def test_add_duplicate_reaction_raises(self):
        """Adding a duplicate reaction should raise ValueError."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        with pytest.raises(ValueError):
            model.add_reaction("R1", {"B": -1.0, "C": 1.0})

    def test_set_objective(self):
        """Setting objective should store the reaction ID."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.set_objective("R1")
        assert model.objective == "R1"

    def test_set_objective_invalid_reaction_raises(self):
        """Setting objective for non-existent reaction should raise."""
        model = MetabolicModel()
        with pytest.raises(ValueError):
            model.set_objective("R_nonexistent")

    def test_solve_fba_empty_model(self):
        """Solving FBA on empty model should return empty dict."""
        model = MetabolicModel()
        result = model.solve_fba()
        assert result == {}

    def test_solve_fba_returns_fluxes(self):
        """Solving FBA should return fluxes for all reactions."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.solve_fba()
        assert "R1" in result
        assert "R2" in result

    def test_solve_fba_maximizes_objective(self):
        """FBA should maximize the objective reaction flux."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0}, upper_bound=10.0)
        model.add_reaction("R2", {"B": -1.0, "C": 1.0}, upper_bound=5.0)
        model.add_reaction("R3", {"C": -1.0, "D": 1.0}, upper_bound=10.0)
        model.add_reaction("R4", {"D": -1.0}, upper_bound=10.0)
        model.set_objective("R2")
        result = model.solve_fba()
        assert result["R2"] == 5.0

    def test_calculate_flux(self):
        """calculate_flux should return the flux for a reaction."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0}, upper_bound=5.0)
        model.add_reaction("R3", {"C": -1.0, "D": 1.0})
        model.add_reaction("R4", {"D": -1.0})
        model.set_objective("R2")
        model.solve_fba()
        flux = model.calculate_flux("R2")
        assert flux == 5.0

    def test_calculate_flux_no_solve(self):
        """calculate_flux should auto-solve if not already solved."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0}, upper_bound=5.0)
        model.add_reaction("R3", {"C": -1.0, "D": 1.0})
        model.add_reaction("R4", {"D": -1.0})
        model.set_objective("R2")
        flux = model.calculate_flux("R2")
        assert flux == 5.0

    def test_calculate_flux_invalid_reaction_raises(self):
        """calculate_flux for non-existent reaction should raise."""
        model = MetabolicModel()
        with pytest.raises(ValueError):
            model.calculate_flux("R_nonexistent")


class TestPathwayDesigner:
    """Test PathwayDesigner class."""

    def test_design_pathway(self):
        """Should find a path from substrate to product."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.add_reaction("R3", {"C": -1.0, "D": 1.0})
        designer = PathwayDesigner(model)
        pathway = designer.design_pathway("A", "D")
        assert pathway == ["R1", "R2", "R3"]

    def test_design_pathway_no_path(self):
        """Should return empty list when no path exists."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"C": -1.0, "D": 1.0})
        designer = PathwayDesigner(model)
        pathway = designer.design_pathway("A", "D")
        assert pathway == []

    def test_design_pathway_same_metabolite(self):
        """Path from a metabolite to itself should be empty."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        designer = PathwayDesigner(model)
        pathway = designer.design_pathway("A", "A")
        assert pathway == []

    def test_calculate_pathway_yield(self):
        """Should calculate theoretical yield correctly."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 2.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        designer = PathwayDesigner(model)
        pathway = ["R1", "R2"]
        yield_val = designer.calculate_pathway_yield(pathway)
        assert yield_val == 2.0

    def test_calculate_pathway_yield_empty(self):
        """Empty pathway should have zero yield."""
        model = MetabolicModel()
        designer = PathwayDesigner(model)
        yield_val = designer.calculate_pathway_yield([])
        assert yield_val == 0.0


class TestStrainOptimizer:
    """Test StrainOptimizer class."""

    def test_optimize_knockouts(self):
        """Should identify beneficial knockouts."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.add_reaction("R3", {"B": -1.0, "D": 1.0})
        model.add_reaction("R4", {"C": -1.0, "E": 1.0})
        model.add_reaction("R5", {"E": -1.0})
        model.add_reaction("R6", {"D": -1.0})
        model.set_objective("R2")
        optimizer = StrainOptimizer(model)
        knockouts = optimizer.optimize_knockouts()
        assert "R3" in knockouts

    def test_optimize_knockouts_no_improvement(self):
        """Should return empty list when no knockouts help."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        optimizer = StrainOptimizer(model)
        knockouts = optimizer.optimize_knockouts()
        assert knockouts == []

    def test_optimize_knockouts_empty_model(self):
        """Should return empty list for empty model."""
        model = MetabolicModel()
        optimizer = StrainOptimizer(model)
        knockouts = optimizer.optimize_knockouts()
        assert knockouts == []
