"""Test-driven development: Gene Therapy vector design module."""
import pytest

from src.genetherapy.vector_design import (
    DeliveryOptimizer,
    ImmuneResponsePredictor,
    Vector,
    calculate_dose,
    calculate_titer,
    check_capacity,
    optimize_delivery,
    predict_immunogenicity,
    predict_transduction_efficiency,
)


# ---------------------------------------------------------------------------
# Vector class
# ---------------------------------------------------------------------------
class TestVector:
    """Test Vector dataclass construction and attributes."""

    def test_vector_creation(self):
        """Vector should store name, capacity, and serotype."""
        v = Vector(name="AAV2-CMV-GFP", capacity=4.7, serotype="AAV2")
        assert v.name == "AAV2-CMV-GFP"
        assert v.capacity == 4.7
        assert v.serotype == "AAV2"

    def test_vector_default_serotype(self):
        """Vector should allow default serotype."""
        v = Vector(name="TestVector", capacity=5.0)
        assert v.serotype == "AAV2"

    def test_vector_equality(self):
        """Vectors with same attributes should be equal."""
        v1 = Vector(name="V1", capacity=4.7, serotype="AAV2")
        v2 = Vector(name="V1", capacity=4.7, serotype="AAV2")
        assert v1 == v2

    def test_vector_inequality(self):
        """Vectors with different attributes should not be equal."""
        v1 = Vector(name="V1", capacity=4.7, serotype="AAV2")
        v2 = Vector(name="V2", capacity=4.7, serotype="AAV2")
        assert v1 != v2


# ---------------------------------------------------------------------------
# check_capacity
# ---------------------------------------------------------------------------
class TestCheckCapacity:
    """Test transgene capacity checking."""

    def test_transgene_fits(self):
        """Transgene smaller than capacity should fit."""
        assert check_capacity(transgene_size=3.0, vector_capacity=4.7) is True

    def test_transgene_too_large(self):
        """Transgene larger than capacity should not fit."""
        assert check_capacity(transgene_size=5.0, vector_capacity=4.7) is False

    def test_transgene_exact_fit(self):
        """Transgene exactly equal to capacity should fit."""
        assert check_capacity(transgene_size=4.7, vector_capacity=4.7) is True

    def test_zero_capacity(self):
        """Zero capacity should reject any transgene."""
        assert check_capacity(transgene_size=0.1, vector_capacity=0.0) is False

    def test_negative_transgene_size(self):
        """Negative transgene size should not fit."""
        assert check_capacity(transgene_size=-1.0, vector_capacity=4.7) is False


# ---------------------------------------------------------------------------
# calculate_titer
# ---------------------------------------------------------------------------
class TestCalculateTiter:
    """Test viral titer estimation."""

    def test_titer_positive(self):
        """Titer should be a positive value."""
        titer = calculate_titer(vector_type="AAV", transgene_size=3.0, purity=0.9)
        assert titer > 0

    def test_titer_higher_purity_higher_titer(self):
        """Higher purity should yield higher titer."""
        titer_low = calculate_titer(vector_type="AAV", transgene_size=3.0, purity=0.5)
        titer_high = calculate_titer(vector_type="AAV", transgene_size=3.0, purity=0.95)
        assert titer_high > titer_low

    def test_titer_lentivirus_lower_than_aav(self):
        """Lentivirus typically has lower titer than AAV."""
        titer_aav = calculate_titer(vector_type="AAV", transgene_size=3.0, purity=0.9)
        titer_lv = calculate_titer(vector_type="Lentivirus", transgene_size=3.0, purity=0.9)
        assert titer_aav > titer_lv

    def test_titer_zero_purity(self):
        """Zero purity should yield zero titer."""
        titer = calculate_titer(vector_type="AAV", transgene_size=3.0, purity=0.0)
        assert titer == 0.0

    def test_titer_invalid_vector_type(self):
        """Unknown vector type should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_titer(vector_type="Unknown", transgene_size=3.0, purity=0.9)


# ---------------------------------------------------------------------------
# ImmuneResponsePredictor
# ---------------------------------------------------------------------------
class TestImmuneResponsePredictor:
    """Test immune response prediction."""

    def test_predictor_creation(self):
        """Predictor should instantiate."""
        predictor = ImmuneResponsePredictor()
        assert predictor is not None

    def test_immunogenicity_score_range(self):
        """Immunogenicity score should be between 0 and 1."""
        predictor = ImmuneResponsePredictor()
        score = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=30, prior_exposure=False
        )
        assert 0.0 <= score <= 1.0

    def test_prior_exposure_increases_immunogenicity(self):
        """Prior exposure should increase immunogenicity score."""
        predictor = ImmuneResponsePredictor()
        score_no = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=30, prior_exposure=False
        )
        score_yes = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=30, prior_exposure=True
        )
        assert score_yes > score_no

    def test_younger_patient_lower_immunogenicity(self):
        """Younger patients should have lower immunogenicity."""
        predictor = ImmuneResponsePredictor()
        score_young = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=5, prior_exposure=False
        )
        score_old = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=70, prior_exposure=False
        )
        assert score_young < score_old

    def test_aav9_lower_immunogenicity_than_aav2(self):
        """AAV9 generally has lower immunogenicity than AAV2."""
        predictor = ImmuneResponsePredictor()
        score_aav2 = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=30, prior_exposure=False
        )
        score_aav9 = predictor.predict_immunogenicity(
            serotype="AAV9", patient_age=30, prior_exposure=False
        )
        assert score_aav9 < score_aav2


# ---------------------------------------------------------------------------
# predict_immunogenicity (standalone function)
# ---------------------------------------------------------------------------
class TestPredictImmunogenicityFunction:
    """Test standalone predict_immunogenicity function."""

    def test_returns_float(self):
        """Should return a float."""
        score = predict_immunogenicity(serotype="AAV2", patient_age=30, prior_exposure=False)
        assert isinstance(score, float)

    def test_prior_exposure_effect(self):
        """Prior exposure should increase score."""
        score_no = predict_immunogenicity(serotype="AAV2", patient_age=30, prior_exposure=False)
        score_yes = predict_immunogenicity(serotype="AAV2", patient_age=30, prior_exposure=True)
        assert score_yes > score_no


# ---------------------------------------------------------------------------
# predict_transduction_efficiency
# ---------------------------------------------------------------------------
class TestPredictTransductionEfficiency:
    """Test transduction efficiency prediction."""

    def test_efficiency_range(self):
        """Efficiency should be between 0 and 1."""
        eff = predict_transduction_efficiency(serotype="AAV9", target_tissue="liver")
        assert 0.0 <= eff <= 1.0

    def test_aav9_liver_high_efficiency(self):
        """AAV9 should have high efficiency for liver."""
        eff = predict_transduction_efficiency(serotype="AAV9", target_tissue="liver")
        assert eff > 0.5

    def test_aav2_muscle_high_efficiency(self):
        """AAV2 should have high efficiency for muscle."""
        eff = predict_transduction_efficiency(serotype="AAV2", target_tissue="muscle")
        assert eff > 0.5

    def test_unknown_serotype_low_efficiency(self):
        """Unknown serotype should have low efficiency."""
        eff = predict_transduction_efficiency(serotype="Unknown", target_tissue="liver")
        assert eff < 0.3

    def test_unknown_tissue_low_efficiency(self):
        """Unknown tissue should have low efficiency."""
        eff = predict_transduction_efficiency(serotype="AAV9", target_tissue="unknown_tissue")
        assert eff < 0.3


# ---------------------------------------------------------------------------
# DeliveryOptimizer
# ---------------------------------------------------------------------------
class TestDeliveryOptimizer:
    """Test delivery optimization."""

    def test_optimizer_creation(self):
        """Optimizer should instantiate."""
        optimizer = DeliveryOptimizer()
        assert optimizer is not None

    def test_optimize_delivery_returns_route(self):
        """Should return a valid delivery route."""
        optimizer = DeliveryOptimizer()
        route = optimizer.optimize_delivery(
            target_tissue="liver", vector_type="AAV9", patient_age=30
        )
        assert isinstance(route, str)
        assert len(route) > 0

    def test_optimize_delivery_liver_iv(self):
        """Liver targeting with AAV9 should suggest IV delivery."""
        optimizer = DeliveryOptimizer()
        route = optimizer.optimize_delivery(
            target_tissue="liver", vector_type="AAV9", patient_age=30
        )
        assert "IV" in route or "intravenous" in route.lower()

    def test_optimize_delivery_cns_intrathecal(self):
        """CNS targeting should suggest intrathecal delivery."""
        optimizer = DeliveryOptimizer()
        route = optimizer.optimize_delivery(
            target_tissue="brain", vector_type="AAV9", patient_age=30
        )
        assert "intrathecal" in route.lower() or "IT" in route

    def test_optimize_delivery_muscle_im(self):
        """Muscle targeting should suggest IM delivery."""
        optimizer = DeliveryOptimizer()
        route = optimizer.optimize_delivery(
            target_tissue="muscle", vector_type="AAV2", patient_age=30
        )
        assert "IM" in route or "intramuscular" in route.lower()


# ---------------------------------------------------------------------------
# optimize_delivery (standalone function)
# ---------------------------------------------------------------------------
class TestOptimizeDeliveryFunction:
    """Test standalone optimize_delivery function."""

    def test_returns_string(self):
        """Should return a string."""
        route = optimize_delivery(target_tissue="liver", vector_type="AAV9", patient_age=30)
        assert isinstance(route, str)

    def test_valid_routes(self):
        """Should return one of the known delivery routes."""
        valid_routes = {
            "IV", "IM", "IT", "SC",
            "intravenous", "intramuscular", "intrathecal", "subcutaneous",
        }
        route = optimize_delivery(target_tissue="liver", vector_type="AAV9", patient_age=30)
        assert route in valid_routes or any(r in route.lower() for r in valid_routes)


# ---------------------------------------------------------------------------
# calculate_dose
# ---------------------------------------------------------------------------
class TestCalculateDose:
    """Test dose calculation."""

    def test_dose_positive(self):
        """Dose should be positive."""
        dose = calculate_dose(patient_weight=70.0, target_tissue="liver", vector_type="AAV9")
        assert dose > 0

    def test_dose_scales_with_weight(self):
        """Heavier patients should receive higher doses."""
        dose_light = calculate_dose(patient_weight=50.0, target_tissue="liver", vector_type="AAV9")
        dose_heavy = calculate_dose(patient_weight=100.0, target_tissue="liver", vector_type="AAV9")
        assert dose_heavy > dose_light

    def test_dose_proportional_to_weight(self):
        """Dose should be proportional to patient weight."""
        dose_50 = calculate_dose(patient_weight=50.0, target_tissue="liver", vector_type="AAV9")
        dose_100 = calculate_dose(patient_weight=100.0, target_tissue="liver", vector_type="AAV9")
        ratio = dose_100 / dose_50
        assert 1.8 <= ratio <= 2.2

    def test_dose_cns_higher_than_muscle(self):
        """CNS targeting typically requires higher doses than muscle."""
        dose_cns = calculate_dose(
            patient_weight=70.0, target_tissue="brain", vector_type="AAV9"
        )
        dose_muscle = calculate_dose(
            patient_weight=70.0, target_tissue="muscle", vector_type="AAV2"
        )
        assert dose_cns > dose_muscle

    def test_dose_zero_weight(self):
        """Zero weight should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_dose(patient_weight=0.0, target_tissue="liver", vector_type="AAV9")

    def test_dose_negative_weight(self):
        """Negative weight should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_dose(patient_weight=-10.0, target_tissue="liver", vector_type="AAV9")


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------
class TestIntegration:
    """Integration tests combining multiple components."""

    def test_full_pipeline(self):
        """Full gene therapy design pipeline should work end-to-end."""
        # Create vector
        vector = Vector(name="AAV9-Lux", capacity=4.7, serotype="AAV9")

        # Check capacity
        assert check_capacity(transgene_size=3.0, vector_capacity=vector.capacity) is True

        # Calculate titer
        titer = calculate_titer(vector_type="AAV", transgene_size=3.0, purity=0.9)
        assert titer > 0

        # Predict immune response
        predictor = ImmuneResponsePredictor()
        imm_score = predictor.predict_immunogenicity(
            serotype=vector.serotype, patient_age=30, prior_exposure=False
        )
        assert 0.0 <= imm_score <= 1.0

        # Optimize delivery
        optimizer = DeliveryOptimizer()
        route = optimizer.optimize_delivery(
            target_tissue="liver", vector_type="AAV9", patient_age=30
        )
        assert isinstance(route, str)

        # Calculate dose
        dose = calculate_dose(patient_weight=70.0, target_tissue="liver", vector_type="AAV9")
        assert dose > 0

    def test_standalone_functions_match_class_methods(self):
        """Standalone functions should produce same results as class methods."""
        # Immunogenicity
        predictor = ImmuneResponsePredictor()
        class_score = predictor.predict_immunogenicity(
            serotype="AAV2", patient_age=30, prior_exposure=False
        )
        func_score = predict_immunogenicity(
            serotype="AAV2", patient_age=30, prior_exposure=False
        )
        assert class_score == func_score

        # Delivery
        optimizer = DeliveryOptimizer()
        class_route = optimizer.optimize_delivery(
            target_tissue="liver", vector_type="AAV9", patient_age=30
        )
        func_route = optimize_delivery(
            target_tissue="liver", vector_type="AAV9", patient_age=30
        )
        assert class_route == func_route
