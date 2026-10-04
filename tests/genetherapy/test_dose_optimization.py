"""TDD tests for dose optimization and treatment cost calculation."""

from src.genetherapy.vector_design import (
    calculate_treatment_cost,
    optimize_dose,
)


class TestOptimizeDose:
    """Test dose optimization for gene therapy."""

    def test_returns_dict_with_required_keys(self):
        """optimize_dose should return a dict with dose, volume, expected_efficiency, moi."""
        result = optimize_dose(
            patient_weight=70.0,
            target_tissue="liver",
            vector_type="AAV",
        )
        assert isinstance(result, dict)
        assert "dose" in result
        assert "volume" in result
        assert "expected_efficiency" in result
        assert "moi" in result

    def test_higher_target_efficiency_returns_higher_dose(self):
        """Higher target efficiency should result in a higher dose."""
        result_low = optimize_dose(
            patient_weight=70.0,
            target_tissue="liver",
            vector_type="AAV",
            target_efficiency=0.5,
        )
        result_high = optimize_dose(
            patient_weight=70.0,
            target_tissue="liver",
            vector_type="AAV",
            target_efficiency=0.9,
        )
        assert result_high["dose"] > result_low["dose"]

    def test_larger_patient_returns_higher_dose(self):
        """Larger patient weight should result in a higher dose."""
        result_small = optimize_dose(
            patient_weight=50.0,
            target_tissue="liver",
            vector_type="AAV",
        )
        result_large = optimize_dose(
            patient_weight=100.0,
            target_tissue="liver",
            vector_type="AAV",
        )
        assert result_large["dose"] > result_small["dose"]


class TestCalculateTreatmentCost:
    """Test treatment cost estimation."""

    def test_returns_positive_float(self):
        """calculate_treatment_cost should return a positive float."""
        result = calculate_treatment_cost(dose=1e12, vector_type="AAV")
        assert isinstance(result, float)
        assert result > 0.0

    def test_more_doses_returns_higher_cost(self):
        """More doses should result in higher total cost."""
        result_single = calculate_treatment_cost(dose=1e12, vector_type="AAV", num_doses=1)
        result_triple = calculate_treatment_cost(dose=1e12, vector_type="AAV", num_doses=3)
        assert result_triple > result_single

    def test_aav_cost_higher_than_lentivirus(self):
        """AAV should cost more than Lentivirus for the same dose."""
        result_aav = calculate_treatment_cost(dose=1e12, vector_type="AAV")
        result_lenti = calculate_treatment_cost(dose=1e12, vector_type="Lentivirus")
        assert result_aav > result_lenti
