"""TDD tests for GPR rules and exchange reactions."""
import pytest
from src.metabolic.fba import MetabolicModel, Reaction


class TestGPRRules:
    """Test Gene-Protein-Reaction rules."""

    def test_add_gpr_rule(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_gpr_rule("R1", "gene1")
        assert model.reactions["R1"].gpr_rule == "gene1"

    def test_add_gpr_rule_and(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_gpr_rule("R1", "gene1 and gene2")
        assert model.reactions["R1"].gpr_rule == "gene1 and gene2"

    def test_add_gpr_rule_or(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_gpr_rule("R1", "gene1 or gene2")
        assert model.reactions["R1"].gpr_rule == "gene1 or gene2"

    def test_add_gpr_rule_complex(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_gpr_rule("R1", "(gene1 and gene2) or gene3")
        assert model.reactions["R1"].gpr_rule == "(gene1 and gene2) or gene3"

    def test_add_gpr_rule_invalid_reaction(self):
        model = MetabolicModel()
        with pytest.raises(ValueError):
            model.add_gpr_rule("R_nonexistent", "gene1")

    def test_get_reactions_by_gene(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_reaction("R2", {"B": -1, "C": 1})
        model.add_gpr_rule("R1", "gene1")
        model.add_gpr_rule("R2", "gene2")
        assert model.get_reactions_by_gene("gene1") == ["R1"]
        assert model.get_reactions_by_gene("gene2") == ["R2"]

    def test_get_reactions_by_gene_multiple(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_reaction("R2", {"B": -1, "C": 1})
        model.add_gpr_rule("R1", "gene1 or gene2")
        model.add_gpr_rule("R2", "gene2")
        assert "R1" in model.get_reactions_by_gene("gene2")
        assert "R2" in model.get_reactions_by_gene("gene2")

    def test_get_reactions_by_gene_not_found(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_gpr_rule("R1", "gene1")
        assert model.get_reactions_by_gene("gene_nonexistent") == []

    def test_knockout_gene(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_reaction("R2", {"B": -1, "C": 1})
        model.add_gpr_rule("R1", "gene1")
        model.add_gpr_rule("R2", "gene2")
        model.set_objective("R2")
        model.solve_fba()
        original_flux = model.calculate_flux("R2")
        model.knockout_gene("gene1")
        assert model.reactions["R1"].lower_bound == 0.0
        assert model.reactions["R1"].upper_bound == 0.0
        model._solution = None
        knockout_flux = model.calculate_flux("R2")
        assert knockout_flux != original_flux

    def test_knockout_gene_invalid(self):
        model = MetabolicModel()
        with pytest.raises(ValueError):
            model.knockout_gene("gene_nonexistent")


class TestExchangeReactions:
    """Test exchange reactions for nutrient uptake and secretion."""

    def test_add_exchange_reaction(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_exchange_reaction("EX_A", "A", lower_bound=-10.0)
        assert "EX_A" in model.reactions
        assert model.reactions["EX_A"].stoichiometry == {"A": 1}

    def test_add_exchange_reaction_default_bounds(self):
        model = MetabolicModel()
        model.add_exchange_reaction("EX_A", "A")
        assert model.reactions["EX_A"].lower_bound == -10.0
        assert model.reactions["EX_A"].upper_bound == 1000.0

    def test_add_exchange_reaction_secretion(self):
        model = MetabolicModel()
        model.add_exchange_reaction("EX_C", "C", lower_bound=0.0)
        assert model.reactions["EX_C"].lower_bound == 0.0

    def test_add_exchange_reaction_new_metabolite(self):
        model = MetabolicModel()
        model.add_exchange_reaction("EX_X", "X_new")
        assert "X_new" in model.metabolites
        assert "EX_X" in model.reactions

    def test_exchange_enables_uptake(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_reaction("R2", {"B": -1, "C": 1})
        model.add_exchange_reaction("EX_A", "A", lower_bound=-10.0)
        model.add_exchange_reaction("EX_C", "C", lower_bound=0.0)
        model.set_objective("EX_C")
        fluxes = model.solve_fba()
        assert fluxes["EX_C"] > 0.0

    def test_exchange_uptake_limit(self):
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1, "B": 1})
        model.add_reaction("R2", {"B": -1, "C": 1})
        model.add_exchange_reaction("EX_A", "A", lower_bound=-5.0)
        model.add_exchange_reaction("EX_C", "C", lower_bound=0.0)
        model.set_objective("EX_C")
        fluxes = model.solve_fba()
        assert fluxes["EX_C"] > 0.0
