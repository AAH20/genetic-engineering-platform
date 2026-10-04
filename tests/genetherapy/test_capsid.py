"""Test-driven development: Capsid engineering predictions module."""
import pytest

from src.genetherapy.vector_design import (
    predict_capsid_antibody_binding,
    predict_capsid_stability,
    suggest_immune_evasion,
)


# ---------------------------------------------------------------------------
# predict_capsid_stability
# ---------------------------------------------------------------------------
class TestPredictCapsidStability:
    """Test capsid stability prediction."""

    def test_returns_float_in_range(self):
        """Stability score should be a float between 0 and 1."""
        score = predict_capsid_stability(serotype="AAV2")
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_aav2_stability(self):
        """AAV2 should have stability of 0.7."""
        score = predict_capsid_stability(serotype="AAV2")
        assert score == 0.7

    def test_aav5_stability(self):
        """AAV5 should have stability of 0.6."""
        score = predict_capsid_stability(serotype="AAV5")
        assert score == 0.6

    def test_aav8_stability(self):
        """AAV8 should have stability of 0.75."""
        score = predict_capsid_stability(serotype="AAV8")
        assert score == 0.75

    def test_aav9_stability(self):
        """AAV9 should have stability of 0.8."""
        score = predict_capsid_stability(serotype="AAV9")
        assert score == 0.8

    def test_lentivirus_stability(self):
        """Lentivirus should have stability of 0.5."""
        score = predict_capsid_stability(serotype="Lentivirus")
        assert score == 0.5


# ---------------------------------------------------------------------------
# predict_capsid_antibody_binding
# ---------------------------------------------------------------------------
class TestPredictCapsidAntibodyBinding:
    """Test capsid antibody binding prediction."""

    def test_returns_float_in_range(self):
        """Antibody binding probability should be a float between 0 and 1."""
        prob = predict_capsid_antibody_binding(serotype="AAV2", patient_age=30)
        assert isinstance(prob, float)
        assert 0.0 <= prob <= 1.0

    def test_aav2_higher_than_aav9(self):
        """AAV2 should have higher antibody binding than AAV9."""
        prob_aav2 = predict_capsid_antibody_binding(serotype="AAV2", patient_age=30)
        prob_aav9 = predict_capsid_antibody_binding(serotype="AAV9", patient_age=30)
        assert prob_aav2 > prob_aav9

    def test_older_patient_higher_binding(self):
        """Older patients should have higher pre-existing immunity."""
        prob_young = predict_capsid_antibody_binding(serotype="AAV2", patient_age=5)
        prob_old = predict_capsid_antibody_binding(serotype="AAV2", patient_age=60)
        assert prob_old > prob_young


# ---------------------------------------------------------------------------
# suggest_immune_evasion
# ---------------------------------------------------------------------------
class TestSuggestImmuneEvasion:
    """Test immune evasion strategy suggestions."""

    def test_returns_list_of_strings(self):
        """Should return a list of strings."""
        strategies = suggest_immune_evasion(serotype="AAV2", patient_age=30)
        assert isinstance(strategies, list)
        assert all(isinstance(s, str) for s in strategies)

    def test_includes_immunosuppression_for_high_immunogenicity(self):
        """High immunogenicity serotypes should include immunosuppression."""
        strategies = suggest_immune_evasion(serotype="AAV2", patient_age=30)
        assert "immunosuppression" in strategies

    def test_includes_capsid_switch_for_high_immunogenicity(self):
        """High immunogenicity serotypes should include capsid_switch."""
        strategies = suggest_immune_evasion(serotype="AAV2", patient_age=30)
        assert "capsid_switch" in strategies

    def test_includes_empty_capsid_decoy(self):
        """Should include empty_capsid_decoy strategy."""
        strategies = suggest_immune_evasion(serotype="AAV2", patient_age=30)
        assert "empty_capsid_decoy" in strategies

    def test_includes_plasmapheresis(self):
        """Should include plasmapheresis strategy."""
        strategies = suggest_immune_evasion(serotype="AAV2", patient_age=30)
        assert "plasmapheresis" in strategies

    def test_low_immunogenicity_fewer_strategies(self):
        """Low immunogenicity serotypes should have fewer strategies."""
        strategies_high = suggest_immune_evasion(serotype="AAV2", patient_age=30)
        strategies_low = suggest_immune_evasion(serotype="AAV9", patient_age=30)
        assert len(strategies_high) >= len(strategies_low)
