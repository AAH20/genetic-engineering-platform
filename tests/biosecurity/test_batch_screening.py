"""Tests for batch screening API."""
from src.biosecurity.screening import SequenceScreener


class TestScreenBatch:
    def setup_method(self):
        self.screener = SequenceScreener()

    def test_screen_batch_empty_list(self):
        result = self.screener.screen_batch([])
        assert result == []

    def test_screen_batch_single_sequence(self):
        seq = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = self.screener.screen_batch([seq])
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["is_clean"] is True
        assert result[0]["matches"] == []

    def test_screen_batch_multiple_sequences(self):
        seqs = [
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC",
            "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC",
        ]
        result = self.screener.screen_batch(seqs)
        assert isinstance(result, list)
        assert len(result) == 3

    def test_screen_batch_results_match_individual_calls(self):
        seqs = [
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC",
            "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC",
        ]
        batch_results = self.screener.screen_batch(seqs)
        for i, seq in enumerate(seqs):
            individual = self.screener.screen_sequence(seq)
            assert batch_results[i] == individual

    def test_screen_batch_mixed_clean_and_threat(self):
        clean = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        threat = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        result = self.screener.screen_batch([clean, threat])
        assert result[0]["is_clean"] is True
        assert result[1]["is_clean"] is False
        assert len(result[1]["matches"]) > 0


class TestCalculateRiskBatch:
    def setup_method(self):
        self.screener = SequenceScreener()

    def test_calculate_risk_batch_empty_list(self):
        result = self.screener.calculate_risk_batch([])
        assert result == []

    def test_calculate_risk_batch_returns_correct_scores(self):
        seqs = [
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC",
        ]
        batch_results = self.screener.calculate_risk_batch(seqs)
        assert isinstance(batch_results, list)
        assert len(batch_results) == 2
        for i, seq in enumerate(seqs):
            individual = self.screener.calculate_risk_score(seq)
            assert batch_results[i] == individual

    def test_calculate_risk_batch_scores_in_valid_range(self):
        seqs = [
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
            "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC",
            "ATGTTCGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGCTGC",
        ]
        results = self.screener.calculate_risk_batch(seqs)
        for score in results:
            assert 0.0 <= score <= 1.0

    def test_calculate_risk_batch_threat_scores_higher(self):
        clean = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        threat = "ATGGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTCGCTATCGAGCTGCTGGACTTC"
        results = self.screener.calculate_risk_batch([clean, threat])
        assert results[1] > results[0]
