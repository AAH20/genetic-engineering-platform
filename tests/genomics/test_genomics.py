"""Test-driven development: Genomics module."""
import pytest

from src.genomics.variant_calling import (
    GenomeAssembly,
    HaplotypeInference,
    Variant,
    assemble_contigs,
    calculate_n50,
    calculate_vaf,
    call_variants,
    phase_variants,
    validate_variant,
)


class TestVariant:
    """Test Variant dataclass."""

    def test_variant_creation(self):
        """Variant should be created with all fields."""
        v = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=30.0)
        assert v.chrom == "chr1"
        assert v.pos == 100
        assert v.ref == "A"
        assert v.alt == "G"
        assert v.quality == 30.0

    def test_variant_default_quality(self):
        """Variant quality should default to 0."""
        v = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        assert v.quality == 0.0

    def test_variant_invalid_ref(self):
        """Variant with invalid ref should raise ValueError."""
        with pytest.raises(ValueError):
            Variant(chrom="chr1", pos=100, ref="X", alt="G")

    def test_variant_invalid_alt(self):
        """Variant with invalid alt should raise ValueError."""
        with pytest.raises(ValueError):
            Variant(chrom="chr1", pos=100, ref="A", alt="X")

    def test_variant_equality(self):
        """Variants with same fields should be equal."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=30.0)
        v2 = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=30.0)
        assert v1 == v2


class TestValidateVariant:
    """Test variant validation."""

    def test_valid_variant(self):
        """Valid ref/alt should pass."""
        assert validate_variant("A", "G") is True

    def test_valid_multi_base(self):
        """Multi-base ref/alt should pass."""
        assert validate_variant("AT", "GC") is True

    def test_invalid_ref(self):
        """Invalid ref should fail."""
        assert validate_variant("X", "G") is False

    def test_invalid_alt(self):
        """Invalid alt should fail."""
        assert validate_variant("A", "X") is False

    def test_empty_ref(self):
        """Empty ref should fail."""
        assert validate_variant("", "G") is False

    def test_empty_alt(self):
        """Empty alt should fail."""
        assert validate_variant("A", "") is False

    def test_case_insensitive(self):
        """Lowercase nucleotides should be valid."""
        assert validate_variant("a", "g") is True


class TestCalculateVAF:
    """Test variant allele frequency calculation."""

    def test_vaf_simple(self):
        """Simple VAF calculation."""
        assert calculate_vaf(5, 10) == 0.5

    def test_vaf_zero_coverage(self):
        """Zero coverage should return 0."""
        assert calculate_vaf(0, 0) == 0.0

    def test_vaf_all_alt(self):
        """All alt reads should return 1.0."""
        assert calculate_vaf(10, 10) == 1.0

    def test_vaf_none_alt(self):
        """No alt reads should return 0.0."""
        assert calculate_vaf(0, 10) == 0.0

    def test_vaf_mixed(self):
        """Mixed reads should calculate correctly."""
        assert calculate_vaf(3, 4) == 0.75


class TestCallVariants:
    """Test variant calling from reads."""

    def test_call_variants_simple(self):
        """Simple variant calling should find variants."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTTCGT",
            "ACGTTCGT",
            "ACGTTCGT",
        ]
        variants = call_variants(reference, reads, min_coverage=3, min_vaf=0.5)
        assert len(variants) >= 1
        pos5_variants = [v for v in variants if v.pos == 5]
        assert len(pos5_variants) >= 1
        assert pos5_variants[0].ref == "A"
        assert pos5_variants[0].alt == "T"

    def test_call_variants_no_variants(self):
        """No variants when all reads match reference."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTACGT",
        ]
        variants = call_variants(reference, reads, min_coverage=3, min_vaf=0.5)
        assert len(variants) == 0

    def test_call_variants_min_coverage(self):
        """Variants below minimum coverage should not be called."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTTCGT",
        ]
        variants = call_variants(reference, reads, min_coverage=3, min_vaf=0.5)
        assert len(variants) == 0

    def test_call_variants_empty_reads(self):
        """Empty reads should return no variants."""
        reference = "ACGTACGT"
        variants = call_variants(reference, [], min_coverage=3, min_vaf=0.5)
        assert len(variants) == 0


class TestGenomeAssembly:
    """Test GenomeAssembly class."""

    def test_assembly_creation(self):
        """GenomeAssembly should be created with contigs."""
        assembly = GenomeAssembly(contigs=["ACGT", "TGCA"])
        assert len(assembly.contigs) == 2

    def test_assembly_empty(self):
        """Empty GenomeAssembly should have no contigs."""
        assembly = GenomeAssembly()
        assert len(assembly.contigs) == 0

    def test_add_contig(self):
        """Adding a contig should increase count."""
        assembly = GenomeAssembly()
        assembly.add_contig("ACGT")
        assert len(assembly.contigs) == 1
        assert assembly.contigs[0] == "ACGT"

    def test_total_length(self):
        """Total length should sum all contig lengths."""
        assembly = GenomeAssembly(contigs=["ACGT", "TGCA"])
        assert assembly.total_length() == 8


class TestAssembleContigs:
    """Test greedy overlap assembly."""

    def test_assemble_no_overlap(self):
        """Non-overlapping reads should remain separate."""
        reads = ["ACGT", "TGCA", "GCTA"]
        contigs = assemble_contigs(reads, min_overlap=3)
        assert len(contigs) == 3

    def test_assemble_with_overlap(self):
        """Overlapping reads should be assembled."""
        reads = ["ACGTACGT", "ACGTACGT"]
        contigs = assemble_contigs(reads, min_overlap=3)
        assert len(contigs) == 1
        assert contigs[0] == "ACGTACGT"

    def test_assemble_multiple(self):
        """Multiple overlapping reads should assemble into one contig."""
        reads = ["ACGTACGT", "CGTACGTA", "GTACGTAC"]
        contigs = assemble_contigs(reads, min_overlap=3)
        assert len(contigs) >= 1

    def test_assemble_empty(self):
        """Empty reads should return empty list."""
        contigs = assemble_contigs([], min_overlap=3)
        assert contigs == []

    def test_assemble_partial_overlap(self):
        """Partially overlapping reads should assemble."""
        reads = ["ACGTACGT", "ACGTACGT"]
        contigs = assemble_contigs(reads, min_overlap=4)
        assert len(contigs) == 1


class TestCalculateN50:
    """Test N50 calculation."""

    def test_n50_simple(self):
        """Simple N50 calculation."""
        contigs = ["ACGT", "TGCA", "GCTA"]
        n50 = calculate_n50(contigs)
        assert n50 == 4

    def test_n50_empty(self):
        """Empty contigs should return 0."""
        assert calculate_n50([]) == 0

    def test_n50_single(self):
        """Single contig should return its length."""
        assert calculate_n50(["ACGTACGT"]) == 8

    def test_n50_varied_lengths(self):
        """N50 with varied lengths."""
        contigs = ["A" * 10, "A" * 5, "A" * 3, "A" * 2]
        n50 = calculate_n50(contigs)
        assert n50 == 10


class TestHaplotypeInference:
    """Test HaplotypeInference class."""

    def test_haplotype_creation(self):
        """HaplotypeInference should be created with variants."""
        v = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        hi = HaplotypeInference(variants=[v])
        assert len(hi.variants) == 1

    def test_haplotype_empty(self):
        """Empty HaplotypeInference should have no variants."""
        hi = HaplotypeInference()
        assert len(hi.variants) == 0

    def test_add_variant(self):
        """Adding a variant should increase count."""
        hi = HaplotypeInference()
        v = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        hi.add_variant(v)
        assert len(hi.variants) == 1


class TestPhaseVariants:
    """Test variant phasing."""

    def test_phase_simple(self):
        """Simple phasing should group variants."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        v2 = Variant(chrom="chr1", pos=200, ref="C", alt="T")
        reads = [
            "A" * 99 + "G" + "C" * 99 + "T",
            "A" * 99 + "G" + "C" * 99 + "T",
        ]
        haplotypes = phase_variants([v1, v2], reads)
        assert len(haplotypes) >= 1

    def test_phase_no_reads(self):
        """No reads should return empty dict."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        haplotypes = phase_variants([v1], [])
        assert haplotypes == {}

    def test_phase_no_variants(self):
        """No variants should return empty dict."""
        reads = ["ACGT", "ACGT"]
        haplotypes = phase_variants([], reads)
        assert haplotypes == {}

    def test_phase_single_variant(self):
        """Single variant should be phased."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G")
        reads = [
            "A" * 99 + "G",
            "A" * 99 + "G",
        ]
        haplotypes = phase_variants([v1], reads)
        assert len(haplotypes) >= 1
