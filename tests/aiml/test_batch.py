"""Test-driven development: batch processing for AI/ML protein language model."""
import numpy as np

from src.aiml.protein_lm import ProteinLanguageModel, VariantEffectPredictor

# ---------------------------------------------------------------------------
# embed_batch
# ---------------------------------------------------------------------------

class TestEmbedBatch:
    """Test batch embedding generation."""

    def test_embed_batch_empty_list(self):
        """embed_batch with empty list should return empty list."""
        model = ProteinLanguageModel()
        result = model.embed_batch([])
        assert result == []

    def test_embed_batch_single_sequence(self):
        """embed_batch with one sequence should return list of one embedding."""
        model = ProteinLanguageModel()
        result = model.embed_batch(["ACDEFGHIKLMNPQRSTVWY"])
        assert len(result) == 1
        assert isinstance(result[0], np.ndarray)

    def test_embed_batch_multiple_sequences(self):
        """embed_batch with multiple sequences should return all embeddings."""
        model = ProteinLanguageModel()
        seqs = ["ACDEFGHIKLMNPQRSTVWY", "WWWWWWWWWWWWWWWWWWWW", "GGGGGGGGGGGGGGGGGG"]
        result = model.embed_batch(seqs)
        assert len(result) == 3
        for emb in result:
            assert isinstance(emb, np.ndarray)

    def test_embed_batch_matches_individual_embed(self):
        """embed_batch results should match individual embed() calls."""
        model = ProteinLanguageModel()
        seqs = ["ACDEFGHIKLMNPQRSTVWY", "WWWWWWWWWWWWWWWWWWWW"]
        batch_result = model.embed_batch(seqs)
        for i, seq in enumerate(seqs):
            individual = model.embed(seq)
            np.testing.assert_array_equal(batch_result[i], individual)


# ---------------------------------------------------------------------------
# predict_variant_effect_batch
# ---------------------------------------------------------------------------

class TestPredictVariantEffectBatch:
    """Test batch variant effect prediction."""

    def test_variant_effect_batch_empty_list(self):
        """predict_variant_effect_batch with empty list should return empty list."""
        model = ProteinLanguageModel()
        result = model.predict_variant_effect_batch([])
        assert result == []

    def test_variant_effect_batch_returns_correct_scores(self):
        """predict_variant_effect_batch should return correct scores for each variant."""
        model = ProteinLanguageModel()
        variants = [
            {"wild_type": "ACDEFGHIKLMNPQRSTVWY", "mutant": "ACDEFGHIKLMNPQRSTVWA", "position": 19},
            {"wild_type": "ACDEFGHIKLMNPQRSTVWY", "mutant": "ACDEFGHIKLMNPQRSTVWF", "position": 19},
        ]
        result = model.predict_variant_effect_batch(variants)
        assert len(result) == 2
        for score in result:
            assert 0.0 <= score <= 1.0

    def test_variant_effect_batch_matches_individual_calls(self):
        """Batch results should match individual predict_variant_effect calls."""
        model = ProteinLanguageModel()
        variants = [
            {"wild_type": "ACDEFGHIKLMNPQRSTVWY", "mutant": "ACDEFGHIKLMNPQRSTVWA", "position": 19},
            {"wild_type": "ACDEFGHIKLMNPQRSTVWY", "mutant": "ACDEFGHIKLMNPQRSTVWF", "position": 19},
        ]
        batch_result = model.predict_variant_effect_batch(variants)
        for i, v in enumerate(variants):
            individual = model.predict_variant_effect(v["wild_type"], v["mutant"], v["position"])
            assert batch_result[i] == individual


# ---------------------------------------------------------------------------
# predict_pathogenicity_batch
# ---------------------------------------------------------------------------

class TestPredictPathogenicityBatch:
    """Test batch pathogenicity prediction."""

    def test_pathogenicity_batch_empty_list(self):
        """predict_pathogenicity_batch with empty list should return empty list."""
        predictor = VariantEffectPredictor()
        result = predictor.predict_pathogenicity_batch([])
        assert result == []

    def test_pathogenicity_batch_returns_correct_scores(self):
        """predict_pathogenicity_batch should return correct scores for each variant."""
        predictor = VariantEffectPredictor()
        variants = [
            {"sequence": "ACDEFGHIKLMNPQRSTVWY", "position": 5, "ref": "G", "alt": "W"},
            {"sequence": "ACDEFGHIKLMNPQRSTVWY", "position": 3, "ref": "D", "alt": "E"},
        ]
        result = predictor.predict_pathogenicity_batch(variants)
        assert len(result) == 2
        for score in result:
            assert 0.0 <= score <= 1.0

    def test_pathogenicity_batch_matches_individual_calls(self):
        """Batch results should match individual predict_pathogenicity calls."""
        predictor = VariantEffectPredictor()
        variants = [
            {"sequence": "ACDEFGHIKLMNPQRSTVWY", "position": 5, "ref": "G", "alt": "W"},
            {"sequence": "ACDEFGHIKLMNPQRSTVWY", "position": 3, "ref": "D", "alt": "E"},
        ]
        batch_result = predictor.predict_pathogenicity_batch(variants)
        for i, v in enumerate(variants):
            individual = predictor.predict_pathogenicity(
                v["sequence"], v["position"], v["ref"], v["alt"],
            )
            assert batch_result[i] == individual
