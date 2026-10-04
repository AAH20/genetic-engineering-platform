"""Test-driven development: VCF export for variant calling."""

from src.genomics.variant_calling import Variant, to_vcf


class TestToVCFEmpty:
    """Test to_vcf with empty variant list."""

    def test_empty_list_returns_header_only(self):
        """Empty variant list should return VCF header lines only."""
        result = to_vcf([])
        lines = result.strip().split("\n")
        assert lines[0] == "##fileformat=VCFv4.2"
        assert lines[1] == "##contig=<ID=ref,length=0>"
        assert lines[2] == "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO"
        assert len(lines) == 3


class TestToVCFSingleVariant:
    """Test to_vcf with a single variant."""

    def test_single_variant_returns_correct_line(self):
        """One variant should produce one data line."""
        v = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=50.0)
        result = to_vcf([v])
        lines = result.strip().split("\n")
        assert len(lines) == 4  # 3 header + 1 data
        data_line = lines[3]
        fields = data_line.split("\t")
        assert fields[0] == "chr1"
        assert fields[1] == "100"
        assert fields[2] == "."
        assert fields[3] == "A"
        assert fields[4] == "G"
        assert fields[5] == "50"
        assert fields[6] == "."
        assert fields[7] == "."


class TestToVCFMultipleVariants:
    """Test to_vcf with multiple variants."""

    def test_multiple_variants_returns_all_lines(self):
        """Multiple variants should produce multiple data lines."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=50.0)
        v2 = Variant(chrom="chr1", pos=200, ref="C", alt="T", quality=30.0)
        result = to_vcf([v1, v2])
        lines = result.strip().split("\n")
        assert len(lines) == 5  # 3 header + 2 data
        assert lines[3].split("\t")[1] == "100"
        assert lines[4].split("\t")[1] == "200"


class TestToVCFContigHeader:
    """Test contig header generation."""

    def test_contig_header_with_correct_length(self):
        """Contig header should have correct length based on variants."""
        v = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=50.0)
        result = to_vcf([v])
        lines = result.strip().split("\n")
        contig_line = lines[1]
        assert "##contig=<ID=ref,length=100>" in contig_line

    def test_contig_header_custom_reference_name(self):
        """Contig header should use custom reference name."""
        v = Variant(chrom="chr1", pos=50, ref="A", alt="G", quality=50.0)
        result = to_vcf([v], reference_name="chr2")
        lines = result.strip().split("\n")
        contig_line = lines[1]
        assert "##contig=<ID=chr2,length=50>" in contig_line


class TestToVCFMultiBase:
    """Test to_vcf with multi-base ref/alt."""

    def test_multi_base_ref_alt(self):
        """Multi-base ref/alt should be handled correctly."""
        v = Variant(chrom="chr1", pos=100, ref="AT", alt="GC", quality=50.0)
        result = to_vcf([v])
        lines = result.strip().split("\n")
        data_line = lines[3]
        fields = data_line.split("\t")
        assert fields[3] == "AT"
        assert fields[4] == "GC"
