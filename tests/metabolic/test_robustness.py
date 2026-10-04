"""Test-driven development: Robustness Analysis and Shadow Prices."""

from src.metabolic.fba import MetabolicModel


class TestRobustnessAnalysis:
    """Test robustness_analysis on MetabolicModel."""

    def test_robustness_returns_dict_with_required_keys(self):
        """robustness_analysis returns dict with flux info and is_robust."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.robustness_analysis("R1")
        assert isinstance(result, dict)
        assert "original_flux" in result
        assert "perturbed_flux" in result
        assert "fold_change" in result
        assert "is_robust" in result

    def test_robustness_no_change_returns_is_robust_true(self):
        """robustness_analysis with no change (fold_change=1.0) should return is_robust=True."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.robustness_analysis("R1", fold_change=1.0)
        assert result["is_robust"] is True

    def test_robustness_large_change_may_return_is_robust_false(self):
        """robustness_analysis with large change (fold_change=0.01) may return is_robust=False."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.robustness_analysis("R1", fold_change=0.01)
        assert result["is_robust"] is False


class TestShadowPrices:
    """Test shadow_prices on MetabolicModel."""

    def test_shadow_prices_returns_dict(self):
        """shadow_prices should return a dict mapping metabolite names to float values."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.shadow_prices()
        assert isinstance(result, dict)

    def test_shadow_prices_empty_model_returns_empty(self):
        """shadow_prices on empty model should return empty dict."""
        model = MetabolicModel()
        result = model.shadow_prices()
        assert result == {}

    def test_shadow_prices_values_are_floats(self):
        """shadow_prices values should be floats."""
        model = MetabolicModel()
        model.add_reaction("R1", {"A": -1.0, "B": 1.0})
        model.add_reaction("R2", {"B": -1.0, "C": 1.0})
        model.set_objective("R2")
        result = model.shadow_prices()
        for met, price in result.items():
            assert isinstance(price, float), f"Shadow price for {met} is not float: {type(price)}"
