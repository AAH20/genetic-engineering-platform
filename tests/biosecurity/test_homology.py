"""Tests for homology checking functions."""
from src.biosecurity.screening import (
    batch_check_homology,
    check_homology_both_strands,
)


class TestCheckHomologyBothStrands:
    """Tests for check_homology_both_strands function."""

    def test_no_homology_returns_is_homologous_false(self):
        reference = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        sequence = "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGC"
        result = check_homology_both_strands(sequence, reference)
        assert result["is_homologous"] is False

    def test_forward_homology_returns_strand_forward(self):
        reference = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        sequence = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = check_homology_both_strands(sequence, reference)
        assert result["strand"] == "forward"
        assert result["is_homologous"] is True

    def test_reverse_homology_returns_strand_reverse(self):
        reference = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
        sequence = "".join(comp.get(c, c) for c in reversed(reference))
        result = check_homology_both_strands(sequence, reference)
        assert result["strand"] == "reverse"
        assert result["is_homologous"] is True


class TestBatchCheckHomology:
    """Tests for batch_check_homology function."""

    def test_empty_list_returns_empty_list(self):
        reference = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        result = batch_check_homology([], reference)
        assert result == []

    def test_returns_list_of_results(self):
        reference = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        sequences = [
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
            "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGC",
        ]
        result = batch_check_homology(sequences, reference)
        assert isinstance(result, list)
        assert len(result) == 2

    def test_results_match_individual_calls(self):
        reference = "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC"
        sequences = [
            "ATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
            "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGC",
        ]
        batch_results = batch_check_homology(sequences, reference)
        individual_results = [
            check_homology_both_strands(seq, reference) for seq in sequences
        ]
        assert batch_results == individual_results
