"""TDD tests for reverse strand off-target search."""
from src.crispr.grna_design import find_off_target_sites_both_strands


class TestFindOffTargetSitesBothStrands:
    """Test off-target search on both strands."""

    def test_forward_strand_match(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "GAGTCCGAGCAGAAGAAGAA"
        result = find_off_target_sites_both_strands(grna, genome)
        assert len(result) >= 1
        assert any(r["mismatches"] == 0 for r in result)

    def test_reverse_strand_match(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        # Reverse complement of gRNA
        rc = "TTCTTCTTCTGCTCGGACTC"
        genome = rc
        result = find_off_target_sites_both_strands(grna, genome)
        assert len(result) >= 1
        assert any(r["strand"] == "reverse" for r in result)

    def test_both_strands_match(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        rc = "TTCTTCTTCTGCTCGGACTC"
        genome = grna + "ACGT" + rc
        result = find_off_target_sites_both_strands(grna, genome)
        strands = {r["strand"] for r in result}
        assert "forward" in strands
        assert "reverse" in strands

    def test_empty_genome(self):
        result = find_off_target_sites_both_strands("GAGTCCGAGCAGAAGAAGAA", "")
        assert result == []

    def test_no_match(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "TTTTTTTTTTTTTTTTTTTT"
        result = find_off_target_sites_both_strands(grna, genome)
        assert result == []

    def test_result_has_strand_key(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = grna
        result = find_off_target_sites_both_strands(grna, genome)
        assert "strand" in result[0]

    def test_max_mismatches_respected(self):
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "GAGTCCGAGCAGAAGAAGAC"  # 1 mismatch
        result = find_off_target_sites_both_strands(grna, genome, max_mismatches=0)
        assert result == []
