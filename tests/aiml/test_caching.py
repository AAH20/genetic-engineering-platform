"""Test-driven development: cache management for AI/ML protein language model."""
import numpy as np

from src.aiml.protein_lm import ProteinLanguageModel


class TestClearCache:
    """Test clear_cache() empties the embedding cache."""

    def test_clear_cache_empties_cache(self):
        """After clear_cache(), get_cache_stats() should report size=0."""
        model = ProteinLanguageModel()
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        assert model.get_cache_stats()["size"] > 0
        model.clear_cache()
        assert model.get_cache_stats()["size"] == 0

    def test_clear_cache_resets_hits_and_misses(self):
        """clear_cache() should also reset hit/miss counters."""
        model = ProteinLanguageModel()
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        model.clear_cache()
        stats = model.get_cache_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0


class TestGetCacheStats:
    """Test get_cache_stats() returns correct counters."""

    def test_stats_after_clear_returns_size_zero(self):
        """get_cache_stats() after clear_cache() returns size=0."""
        model = ProteinLanguageModel()
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        model.clear_cache()
        stats = model.get_cache_stats()
        assert stats["size"] == 0

    def test_stats_initial_state(self):
        """Fresh model should have size=0, hits=0, misses=0."""
        model = ProteinLanguageModel()
        stats = model.get_cache_stats()
        assert stats == {"size": 0, "hits": 0, "misses": 0}

    def test_stats_tracks_misses(self):
        """First-time embed increments misses."""
        model = ProteinLanguageModel()
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        stats = model.get_cache_stats()
        assert stats["misses"] == 1
        assert stats["size"] == 1

    def test_stats_tracks_hits(self):
        """Repeated embed of same sequence increments hits, not misses."""
        model = ProteinLanguageModel()
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        stats = model.get_cache_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["size"] == 1

    def test_stats_multiple_sequences(self):
        """Stats accumulate across multiple unique sequences."""
        model = ProteinLanguageModel()
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        model.embed_cached("WWWWWWWWWWWWWWWWWWWW")
        model.embed_cached("ACDEFGHIKLMNPQRSTVWY")
        stats = model.get_cache_stats()
        assert stats["size"] == 2
        assert stats["misses"] == 2
        assert stats["hits"] == 1


class TestEmbedBatchCached:
    """Test embed_batch_cached() with caching."""

    def test_returns_correct_embeddings(self):
        """embed_batch_cached() returns correct embedding values."""
        model = ProteinLanguageModel()
        seq = "ACDEFGHIKLMNPQRSTVWY"
        result = model.embed_batch_cached([seq])
        assert len(result) == 1
        assert isinstance(result[0], list)
        assert len(result[0]) == model.embedding_dim
        # Should match direct embed()
        direct = model.embed(seq).tolist()
        np.testing.assert_allclose(result[0], direct, rtol=1e-10)

    def test_multiple_sequences(self):
        """embed_batch_cached() handles multiple sequences."""
        model = ProteinLanguageModel()
        seqs = ["ACDEFGHIKLMNPQRSTVWY", "WWWWWWWWWWWWWWWWWWWW"]
        result = model.embed_batch_cached(seqs)
        assert len(result) == 2
        for r in result:
            assert isinstance(r, list)
            assert len(r) == model.embedding_dim

    def test_cache_hit_on_second_call(self):
        """Second call with same sequence should use cache (hit)."""
        model = ProteinLanguageModel()
        seq = "ACDEFGHIKLMNPQRSTVWY"
        model.embed_batch_cached([seq])
        stats1 = model.get_cache_stats()
        assert stats1["misses"] == 1
        assert stats1["hits"] == 0

        model.embed_batch_cached([seq])
        stats2 = model.get_cache_stats()
        assert stats2["hits"] == 1
        assert stats2["misses"] == 1
        assert stats2["size"] == 1

    def test_stats_after_embed_show_correct_counts(self):
        """get_cache_stats() reflects accurate counts after embed_batch_cached."""
        model = ProteinLanguageModel()
        seqs = ["ACDEFGHIKLMNPQRSTVWY", "WWWWWWWWWWWWWWWWWWWW"]
        model.embed_batch_cached(seqs)
        model.embed_batch_cached(seqs)
        stats = model.get_cache_stats()
        assert stats["size"] == 2
        assert stats["misses"] == 2
        assert stats["hits"] == 2
