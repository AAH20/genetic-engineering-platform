"""Test-driven development: FASTA I/O for genomics module."""
import pytest

from src.genomics.variant_calling import (
    Variant,
    read_fasta,
    variants_to_fasta,
    write_fasta,
)


class TestWriteFasta:
    """Test write_fasta function."""

    def test_write_fasta_creates_file_with_correct_content(self, tmp_path):
        """write_fasta should create a file with correct FASTA content."""
        sequences = {"seq1": "ACGT", "seq2": "TGCA"}
        filepath = tmp_path / "test.fasta"
        write_fasta(sequences, str(filepath))

        content = filepath.read_text()
        assert ">seq1\nACGT\n" in content
        assert ">seq2\nTGCA\n" in content

    def test_write_fasta_empty_dict(self, tmp_path):
        """write_fasta with empty dict should create an empty file."""
        filepath = tmp_path / "empty.fasta"
        write_fasta({}, str(filepath))

        assert filepath.read_text() == ""


class TestReadFasta:
    """Test read_fasta function."""

    def test_read_fasta_returns_correct_dict(self, tmp_path):
        """read_fasta should return a dict mapping headers to sequences."""
        filepath = tmp_path / "test.fasta"
        filepath.write_text(">seq1\nACGT\n>seq2\nTGCA\n")

        result = read_fasta(str(filepath))
        assert result == {"seq1": "ACGT", "seq2": "TGCA"}

    def test_read_fasta_multiline_sequence(self, tmp_path):
        """read_fasta should handle multi-line sequences."""
        filepath = tmp_path / "test.fasta"
        filepath.write_text(">seq1\nACGT\nTGCA\n>seq2\nAAAA\n")

        result = read_fasta(str(filepath))
        assert result == {"seq1": "ACGTTGCA", "seq2": "AAAA"}

    def test_read_fasta_file_not_found(self):
        """read_fasta with nonexistent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_fasta("/nonexistent/path/file.fasta")


class TestFastaRoundtrip:
    """Test write_fasta/read_fasta roundtrip."""

    def test_roundtrip_preserves_data(self, tmp_path):
        """write_fasta followed by read_fasta should preserve data."""
        original = {"chr1": "ACGTACGT", "chr2": "TGCATGCA", "chr3": "AAAACCCC"}
        filepath = tmp_path / "roundtrip.fasta"

        write_fasta(original, str(filepath))
        result = read_fasta(str(filepath))

        assert result == original

    def test_roundtrip_single_sequence(self, tmp_path):
        """Roundtrip with single sequence should work."""
        original = {"seq1": "ACGT"}
        filepath = tmp_path / "single.fasta"

        write_fasta(original, str(filepath))
        result = read_fasta(str(filepath))

        assert result == original


class TestVariantsToFasta:
    """Test variants_to_fasta function."""

    def test_variants_to_fasta_returns_valid_fasta_string(self):
        """variants_to_fasta should return a valid FASTA-formatted string."""
        variants = [
            Variant(chrom="chr1", pos=100, ref="A", alt="G"),
            Variant(chrom="chr1", pos=200, ref="C", alt="T"),
        ]
        result = variants_to_fasta(variants)

        assert ">ref_100_A_G\n" in result
        assert ">ref_200_C_T\n" in result
        assert result.count(">") == 2

    def test_variants_to_fasta_empty_list_returns_empty_string(self):
        """variants_to_fasta with empty list should return empty string."""
        result = variants_to_fasta([])
        assert result == ""

    def test_variants_to_fasta_custom_reference_name(self):
        """variants_to_fasta should use custom reference name in header."""
        variants = [
            Variant(chrom="chr1", pos=100, ref="A", alt="G"),
        ]
        result = variants_to_fasta(variants, reference_name="myref")

        assert ">myref_100_A_G\n" in result
