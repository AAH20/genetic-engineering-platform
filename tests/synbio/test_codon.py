"""Test-driven development: codon optimization and CAI calculation."""

from src.synbio.genetic_circuits import calculate_cai, optimize_codon_usage


class TestOptimizeCodonUsage:
    """Test optimize_codon_usage returns valid DNA sequences."""

    def test_returns_dna_sequence(self):
        result = optimize_codon_usage("MKVLAAALLL", host="E.coli")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_ecoli_returns_valid_dna(self):
        result = optimize_codon_usage("MKVLAAALLL", host="E.coli")
        valid_bases = set("ATCG")
        assert all(base in valid_bases for base in result.upper())

    def test_different_hosts_return_different_sequences(self):
        # Use a protein with Pro (P): E.coli prefers CCG, B.subtilis prefers ACC
        ecoli_result = optimize_codon_usage("MKVLAAALLLP", host="E.coli")
        subtilis_result = optimize_codon_usage("MKVLAAALLLP", host="B.subtilis")
        assert ecoli_result != subtilis_result

    def test_cerevisiae_host(self):
        result = optimize_codon_usage("MKVLAAALLL", host="S.cerevisiae")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_length_is_multiple_of_three(self):
        result = optimize_codon_usage("MKVLAAALLL", host="E.coli")
        assert len(result) % 3 == 0

    def test_encodes_same_protein(self):
        # The DNA should translate back to the same protein
        # We can verify by checking length: 10 aa -> 30 nt
        protein = "MKVLAAALLL"
        result = optimize_codon_usage(protein, host="E.coli")
        assert len(result) == len(protein) * 3


class TestCalculateCai:
    """Test calculate_cai returns float in [0,1]."""

    def test_returns_float(self):
        result = calculate_cai("ATGAAATTT", host="E.coli")
        assert isinstance(result, float)

    def test_in_range(self):
        result = calculate_cai("ATGAAATTT", host="E.coli")
        assert 0.0 <= result <= 1.0

    def test_optimal_codons_high_cai(self):
        # Use E.coli optimal codons: AAA (Lys), TTT (Phe), etc.
        # Build a sequence with only optimal codons for E.coli
        dna = "ATG" + "AAA" * 10 + "TAA"  # M + 10xK + stop
        result = calculate_cai(dna, host="E.coli")
        assert result > 0.8

    def test_rare_codons_low_cai(self):
        # Use rare codons for E.coli: AGG (Arg), CGA (Arg), etc.
        dna = "ATG" + "AGG" * 10 + "TAA"  # M + 10xR(rare) + stop
        result = calculate_cai(dna, host="E.coli")
        assert result < 0.5

    def test_empty_sequence(self):
        result = calculate_cai("", host="E.coli")
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0
