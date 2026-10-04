"""Test-driven development: Chromosome-aware phasing and haplotype diversity."""

from src.genomics.variant_calling import (
    Variant,
    calculate_haplotype_diversity,
    phase_variants_by_chromosome,
)


class TestPhaseVariantsByChromosome:
    """Test chromosome-aware variant phasing."""

    def test_empty_variants_returns_empty_dict(self):
        """Empty variant list should return empty dict."""
        result = phase_variants_by_chromosome([], ["ACGT", "ACGT"])
        assert result == {}

    def test_groups_by_chromosome(self):
        """Variants on different chromosomes should be grouped separately."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        v2 = Variant(chrom="chr2", pos=200, ref="C", alt="T")
        reads = [
            "A" * 99 + "G" + "C" * 99 + "T",
            "A" * 99 + "G" + "C" * 99 + "T",
        ]
        result = phase_variants_by_chromosome([v1, v2], reads)
        assert "chr1" in result
        assert "chr2" in result
        assert len(result["chr1"]) == 1
        assert len(result["chr2"]) == 1
        assert result["chr1"][0] == v1
        assert result["chr2"][0] == v2

    def test_single_chromosome_returns_single_key(self):
        """Variants on one chromosome should return single key."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        v2 = Variant(chrom="chr1", pos=200, ref="C", alt="T")
        reads = [
            "A" * 99 + "G" + "C" * 99 + "T",
            "A" * 99 + "G" + "C" * 99 + "T",
        ]
        result = phase_variants_by_chromosome([v1, v2], reads)
        assert len(result) == 1
        assert "chr1" in result
        assert len(result["chr1"]) == 2


class TestCalculateHaplotypeDiversity:
    """Test haplotype diversity calculation."""

    def test_one_haplotype_returns_zero(self):
        """Single haplotype should have zero diversity."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        haplotypes = {0: [v1]}
        assert calculate_haplotype_diversity(haplotypes) == 0.0

    def test_two_equal_haplotypes_returns_half(self):
        """Two equally frequent haplotypes should have diversity 0.5."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        v2 = Variant(chrom="chr1", pos=200, ref="C", alt="T")
        haplotypes = {0: [v1], 1: [v2]}
        assert calculate_haplotype_diversity(haplotypes) == 0.5

    def test_many_haplotypes_returns_high_diversity(self):
        """Many haplotypes should have diversity > 0.5."""
        haplotypes = {}
        for i in range(10):
            v = Variant(chrom="chr1", pos=100 + i, ref="A", alt="G")
            haplotypes[i] = [v]
        result = calculate_haplotype_diversity(haplotypes)
        assert result > 0.5
