"""Test-driven development: embedding similarity for AI/ML module."""
import pytest

from src.aiml.protein_lm import ProteinLanguageModel


class TestCosineSimilarity:
    """Test cosine_similarity method."""

    def test_identical_sequences_returns_one(self):
        """Identical sequences should have cosine similarity of 1.0."""
        model = ProteinLanguageModel()
        seq = "ACDEFGHIKLMNPQRSTVWY"
        result = model.cosine_similarity(seq, seq)
        assert result == pytest.approx(1.0)

    def test_different_sequences_returns_less_than_one(self):
        """Different sequences should have cosine similarity < 1.0."""
        model = ProteinLanguageModel()
        seq1 = "ACDEFGHIKLMNPQRSTVWY"
        seq2 = "WWWWWWWWWWWWWWWWWWWW"
        result = model.cosine_similarity(seq1, seq2)
        assert result < 1.0

    def test_empty_sequences_returns_zero(self):
        """Empty sequences should return 0.0."""
        model = ProteinLanguageModel()
        result = model.cosine_similarity("", "")
        assert result == 0.0

    def test_one_empty_sequence_returns_zero(self):
        """One empty sequence should return 0.0."""
        model = ProteinLanguageModel()
        result = model.cosine_similarity("ACDEFGHIKLMNPQRSTVWY", "")
        assert result == 0.0

    def test_result_in_valid_range(self):
        """Cosine similarity should be in [-1, 1]."""
        model = ProteinLanguageModel()
        seq1 = "ACDEFGHIKLMNPQRSTVWY"
        seq2 = "WWWWWWWWWWWWWWWWWWWW"
        result = model.cosine_similarity(seq1, seq2)
        assert -1.0 <= result <= 1.0


class TestFindSimilar:
    """Test find_similar method."""

    def test_empty_candidates_returns_empty_list(self):
        """Empty candidates list should return empty list."""
        model = ProteinLanguageModel()
        result = model.find_similar("ACDEFGHIKLMNPQRSTVWY", [])
        assert result == []

    def test_returns_top_k_results(self):
        """Should return exactly top_k results."""
        model = ProteinLanguageModel()
        candidates = [
            "ACDEFGHIKLMNPQRSTVWY",
            "WWWWWWWWWWWWWWWWWWWW",
            "GGGGGGGGGGGGGGGGGGGG",
            "ACDEFGHIKLMNPQRSTVWA",
            "ACDEFGHIKLMNPQRSTVWG",
        ]
        result = model.find_similar("ACDEFGHIKLMNPQRSTVWY", candidates, top_k=3)
        assert len(result) == 3

    def test_results_sorted_by_similarity(self):
        """Results should be sorted by similarity (descending)."""
        model = ProteinLanguageModel()
        candidates = [
            "ACDEFGHIKLMNPQRSTVWY",
            "WWWWWWWWWWWWWWWWWWWW",
            "GGGGGGGGGGGGGGGGGGGG",
        ]
        result = model.find_similar("ACDEFGHIKLMNPQRSTVWY", candidates, top_k=3)
        similarities = [sim for _, sim in result]
        assert similarities == sorted(similarities, reverse=True)

    def test_default_top_k(self):
        """Default top_k should be 5."""
        model = ProteinLanguageModel()
        candidates = [
            "ACDEFGHIKLMNPQRSTVWY",
            "WWWWWWWWWWWWWWWWWWWW",
            "GGGGGGGGGGGGGGGGGGGG",
            "ACDEFGHIKLMNPQRSTVWA",
            "ACDEFGHIKLMNPQRSTVWG",
            "ACDEFGHIKLMNPQRSTVWC",
            "ACDEFGHIKLMNPQRSTVWD",
        ]
        result = model.find_similar("ACDEFGHIKLMNPQRSTVWY", candidates)
        assert len(result) == 5

    def test_returns_tuples(self):
        """Results should be (sequence, similarity) tuples."""
        model = ProteinLanguageModel()
        candidates = ["ACDEFGHIKLMNPQRSTVWY", "WWWWWWWWWWWWWWWWWWWW"]
        result = model.find_similar("ACDEFGHIKLMNPQRSTVWY", candidates, top_k=2)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], float)
