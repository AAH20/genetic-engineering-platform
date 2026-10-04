"""Test-driven development: AI/ML protein language model persistence and caching."""
import os
import time

import numpy as np

from src.aiml.protein_lm import ProteinLanguageModel


class TestSave:
    """Test ProteinLanguageModel.save()."""

    def test_save_creates_file(self, tmp_path):
        """save() should create a file at the given path."""
        model = ProteinLanguageModel(name="test-model")
        save_path = str(tmp_path / "model.json")
        model.save(save_path)
        assert os.path.exists(save_path)

    def test_save_creates_nonempty_file(self, tmp_path):
        """save() should write a non-empty JSON file."""
        model = ProteinLanguageModel(name="test-model")
        save_path = str(tmp_path / "model.json")
        model.save(save_path)
        assert os.path.getsize(save_path) > 0


class TestLoad:
    """Test ProteinLanguageModel.load()."""

    def test_load_returns_protein_language_model(self, tmp_path):
        """load() should return a ProteinLanguageModel instance."""
        model = ProteinLanguageModel(name="test-model")
        save_path = str(tmp_path / "model.json")
        model.save(save_path)
        loaded = ProteinLanguageModel.load(save_path)
        assert isinstance(loaded, ProteinLanguageModel)

    def test_load_preserves_name(self, tmp_path):
        """load() should preserve the model name."""
        model = ProteinLanguageModel(name="my-special-model")
        save_path = str(tmp_path / "model.json")
        model.save(save_path)
        loaded = ProteinLanguageModel.load(save_path)
        assert loaded.name == "my-special-model"


class TestSaveLoadRoundtrip:
    """Test save/load roundtrip preserves model state."""

    def test_roundtrip_preserves_name(self, tmp_path):
        """save then load should preserve the model name."""
        original = ProteinLanguageModel(name="roundtrip-test", max_length=512)
        save_path = str(tmp_path / "model.json")
        original.save(save_path)
        loaded = ProteinLanguageModel.load(save_path)
        assert loaded.name == "roundtrip-test"

    def test_roundtrip_preserves_max_length(self, tmp_path):
        """save then load should preserve max_length."""
        original = ProteinLanguageModel(name="test", max_length=256)
        save_path = str(tmp_path / "model.json")
        original.save(save_path)
        loaded = ProteinLanguageModel.load(save_path)
        assert loaded.max_length == 256

    def test_roundtrip_model_can_embed(self, tmp_path):
        """A loaded model should be able to generate embeddings."""
        original = ProteinLanguageModel(name="test")
        save_path = str(tmp_path / "model.json")
        original.save(save_path)
        loaded = ProteinLanguageModel.load(save_path)
        result = loaded.embed("ACDEFGHIKLMNPQRSTVWY")
        assert isinstance(result, np.ndarray)
        assert result.shape[0] > 0


class TestEmbedCached:
    """Test ProteinLanguageModel.embed_cached()."""

    def test_embed_cached_returns_same_as_embed(self):
        """embed_cached() should return the same result as embed()."""
        model = ProteinLanguageModel()
        seq = "ACDEFGHIKLMNPQRSTVWY"
        cached_result = model.embed_cached(seq)
        direct_result = model.embed(seq)
        np.testing.assert_array_almost_equal(cached_result, direct_result)

    def test_embed_cached_caches_results(self):
        """Second call to embed_cached() should be faster (cache hit)."""
        model = ProteinLanguageModel()
        seq = "ACDEFGHIKLMNPQRSTVWY" * 10  # longer sequence for measurable time

        # First call — computes and caches
        start = time.perf_counter()
        result1 = model.embed_cached(seq)
        elapsed_first = time.perf_counter() - start

        # Second call — should be a cache hit
        start = time.perf_counter()
        result2 = model.embed_cached(seq)
        elapsed_second = time.perf_counter() - start

        # Results should be identical
        np.testing.assert_array_almost_equal(result1, result2)
        # Second call should be faster (dict lookup vs computation)
        assert elapsed_second < elapsed_first * 0.9

    def test_embed_cached_different_sequences(self):
        """Different sequences should produce different cached results."""
        model = ProteinLanguageModel()
        seq1 = "ACDEFGHIKLMNPQRSTVWY"
        seq2 = "WVTSRQPNMLKIHGFEDCA"
        result1 = model.embed_cached(seq1)
        result2 = model.embed_cached(seq2)
        # Different sequences should produce different embeddings
        assert not np.allclose(result1, result2)

    def test_embed_cached_returns_list(self):
        """embed_cached() should return a list of floats."""
        model = ProteinLanguageModel()
        result = model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        assert isinstance(result, list)
        assert all(isinstance(x, float) for x in result)
