"""Test-driven development: input validation for AI/ML protein language model module."""
import pytest

from src.aiml.protein_lm import (
    ProteinLanguageModel,
    VariantEffectPredictor,
)


class TestEmbedValidation:
    """Test input validation for ProteinLanguageModel.embed()."""

    def test_embed_invalid_amino_acid_raises_value_error(self):
        """embed() should raise ValueError for invalid amino acids."""
        model = ProteinLanguageModel()
        with pytest.raises(ValueError, match="Invalid amino acid"):
            model.embed("ACDEFGHIKLMNPQRSTVWYZ")  # Z is invalid

    def test_embed_empty_sequence_raises_value_error(self):
        """embed() should raise ValueError for empty sequence."""
        model = ProteinLanguageModel()
        with pytest.raises(ValueError, match="empty"):
            model.embed("")


class TestPredictVariantEffectValidation:
    """Test input validation for ProteinLanguageModel.predict_variant_effect()."""

    def test_predict_variant_effect_negative_position_raises_value_error(self):
        """predict_variant_effect() should raise ValueError for negative position."""
        model = ProteinLanguageModel()
        with pytest.raises(ValueError, match="position"):
            model.predict_variant_effect("ACDEFGHIKLMNPQRSTVWY", "ACDEFGHIKLMNPQRSTVWA", -1)

    def test_predict_variant_effect_position_exceeds_length_raises_value_error(self):
        """predict_variant_effect() should raise ValueError for position > sequence length."""
        model = ProteinLanguageModel()
        with pytest.raises(ValueError, match="position"):
            model.predict_variant_effect("ACDEFGHIKLMNPQRSTVWY", "ACDEFGHIKLMNPQRSTVWA", 25)

    def test_predict_variant_effect_empty_wild_type_raises_value_error(self):
        """predict_variant_effect() should raise ValueError for empty wild_type."""
        model = ProteinLanguageModel()
        with pytest.raises(ValueError, match="empty"):
            model.predict_variant_effect("", "A", 0)

    def test_predict_variant_effect_empty_mutant_raises_value_error(self):
        """predict_variant_effect() should raise ValueError for empty mutant."""
        model = ProteinLanguageModel()
        with pytest.raises(ValueError, match="empty"):
            model.predict_variant_effect("A", "", 0)


class TestPredictPathogenicityValidation:
    """Test input validation for VariantEffectPredictor.predict_pathogenicity()."""

    def test_predict_pathogenicity_negative_position_raises_value_error(self):
        """predict_pathogenicity() should raise ValueError for negative position."""
        predictor = VariantEffectPredictor()
        with pytest.raises(ValueError, match="position"):
            predictor.predict_pathogenicity("ACDEFGHIKLMNPQRSTVWY", -1, "A", "G")

    def test_predict_pathogenicity_position_exceeds_length_raises_value_error(self):
        """predict_pathogenicity() should raise ValueError for position > sequence length."""
        predictor = VariantEffectPredictor()
        with pytest.raises(ValueError, match="position"):
            predictor.predict_pathogenicity("ACDEFGHIKLMNPQRSTVWY", 25, "A", "G")

    def test_predict_pathogenicity_empty_sequence_raises_value_error(self):
        """predict_pathogenicity() should raise ValueError for empty sequence."""
        predictor = VariantEffectPredictor()
        with pytest.raises(ValueError, match="empty"):
            predictor.predict_pathogenicity("", 0, "A", "G")
