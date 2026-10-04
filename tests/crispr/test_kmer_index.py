"""TDD tests for k-mer indexed off-target search."""
from src.crispr.grna_design import build_kmer_index, find_off_target_sites_indexed


class TestBuildKmerIndex:
    """Test k-mer index construction."""

    def test_build_index_empty_genome(self):
        index = build_kmer_index("", k=8)
        assert index == {}

    def test_build_index_short_genome(self):
        index = build_kmer_index("ACGT", k=8)
        assert index == {}

    def test_build_index_exact_k(self):
        index = build_kmer_index("ACGTACGT", k=8)
        assert "ACGTACGT" in index
        assert index["ACGTACGT"] == [0]

    def test_build_index_multiple_positions(self):
        index = build_kmer_index("ACGTACGTACGT", k=8)
        assert "ACGTACGT" in index
        assert len(index["ACGTACGT"]) == 2

    def test_build_index_overlapping(self):
        index = build_kmer_index("AAAA", k=2)
        assert "AA" in index
        assert len(index["AA"]) == 3


class TestFindOffTargetSitesIndexed:
    """Test indexed off-target search."""

    def test_empty_genome(self):
        result = find_off_target_sites_indexed("GAGTCCGAGCAGAAGAAGAA", "", k=8)
        assert result == []

    def test_exact_match(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "GAGTCCGAGCAGAAGAAGAA"
        result = find_off_target_sites_indexed(grna, genome, k=8)
        assert len(result) == 1
        assert result[0]["mismatches"] == 0

    def test_one_mismatch(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "GAGTCCGAGCAGAAGAAGAC"  # last base differs
        result = find_off_target_sites_indexed(grna, genome, k=8)
        assert len(result) >= 1

    def test_no_match(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "TTTTTTTTTTTTTTTTTTTT"
        result = find_off_target_sites_indexed(grna, genome, k=8)
        assert result == []

    def test_multiple_matches(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = grna + "ACGT" + grna
        result = find_off_target_sites_indexed(grna, genome, k=8)
        assert len(result) == 2

    def test_result_has_required_keys(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = grna
        result = find_off_target_sites_indexed(grna, genome, k=8)
        assert "position" in result[0]
        assert "sequence" in result[0]
        assert "mismatches" in result[0]
        assert "score" in result[0]

    def test_max_mismatches_respected(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "GAGTCCGAGCAGAAGAAGAC"  # 1 mismatch
        result = find_off_target_sites_indexed(grna, genome, max_mismatches=0, k=8)
        assert result == []
