"""TDD tests for GenBank I/O of gene therapy vectors."""

import pytest

from src.genetherapy.vector_design import (
    Vector,
    read_genbank,
    vector_to_genbank,
    write_genbank,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_sequence(length: int) -> str:
    """Return a deterministic DNA sequence of the given length."""
    bases = "ACGT"
    return "".join(bases[i % 4] for i in range(length))


# ---------------------------------------------------------------------------
# vector_to_genbank
# ---------------------------------------------------------------------------
class TestVectorToGenbank:
    """Test conversion of a single Vector to GenBank format."""

    def test_returns_string(self):
        """Should return a string."""
        v = Vector(name="AAV2-GFP", capacity=4.7, serotype="AAV2")
        result = vector_to_genbank(v)
        assert isinstance(result, str)

    def test_contains_locus_line(self):
        """Output should contain a LOCUS line with the vector name."""
        v = Vector(name="TestVec", capacity=5.0, serotype="AAV9")
        result = vector_to_genbank(v)
        assert "LOCUS" in result
        assert "TestVec" in result

    def test_contains_capacity(self):
        """Output should contain the capacity value."""
        v = Vector(name="CapVec", capacity=6.2, serotype="AAV5")
        result = vector_to_genbank(v)
        assert "6.2" in result

    def test_contains_serotype_in_definition(self):
        """Output should contain the serotype in the DEFINITION line."""
        v = Vector(name="SerVec", capacity=4.7, serotype="AAV8")
        result = vector_to_genbank(v)
        assert "DEFINITION" in result
        assert "AAV8" in result

    def test_ends_with_double_slash(self):
        """Output should end with the GenBank terminator '//'."""
        v = Vector(name="TermVec", capacity=4.7, serotype="AAV2")
        result = vector_to_genbank(v)
        assert result.rstrip().endswith("//")

    def test_contains_origin_section(self):
        """Output should contain an ORIGIN section."""
        v = Vector(name="OriVec", capacity=4.7, serotype="AAV2")
        result = vector_to_genbank(v)
        assert "ORIGIN" in result

    def test_sequence_line_wrapping(self):
        """Sequence lines should be at most 60 characters each."""
        v = Vector(name="WrapVec", capacity=4.7, serotype="AAV2")
        result = vector_to_genbank(v)
        origin_idx = result.index("ORIGIN")
        seq_section = result[origin_idx + len("ORIGIN") :]
        # Strip the trailing // and blank lines
        seq_lines = [
            line.strip()
            for line in seq_section.splitlines()
            if line.strip() and line.strip() != "//"
        ]
        for line in seq_lines:
            # Remove the leading position number (e.g. "        1 ")
            parts = line.split(" ", 1)
            if len(parts) == 2:
                seq_part = parts[1].replace(" ", "")
                assert len(seq_part) <= 60


# ---------------------------------------------------------------------------
# write_genbank
# ---------------------------------------------------------------------------
class TestWriteGenbank:
    """Test writing vectors to a GenBank file."""

    def test_creates_file(self, tmp_path):
        """Should create the file at the given path."""
        v = Vector(name="WriteVec", capacity=4.7, serotype="AAV2")
        filepath = str(tmp_path / "test.gb")
        write_genbank([v], filepath)
        assert (tmp_path / "test.gb").exists()

    def test_file_contains_locus(self, tmp_path):
        """Written file should contain LOCUS line."""
        v = Vector(name="LocusVec", capacity=4.7, serotype="AAV2")
        filepath = str(tmp_path / "locus.gb")
        write_genbank([v], filepath)
        content = (tmp_path / "locus.gb").read_text()
        assert "LOCUS" in content
        assert "LocusVec" in content

    def test_multiple_vectors_multiple_loci(self, tmp_path):
        """Writing N vectors should produce N LOCUS lines."""
        vectors = [
            Vector(name="V1", capacity=4.7, serotype="AAV2"),
            Vector(name="V2", capacity=5.0, serotype="AAV9"),
            Vector(name="V3", capacity=6.0, serotype="Lentivirus"),
        ]
        filepath = str(tmp_path / "multi.gb")
        write_genbank(vectors, filepath)
        content = (tmp_path / "multi.gb").read_text()
        assert content.count("LOCUS") == 3

    def test_file_ends_with_double_slash(self, tmp_path):
        """File content should end with //."""
        v = Vector(name="EndVec", capacity=4.7, serotype="AAV2")
        filepath = str(tmp_path / "end.gb")
        write_genbank([v], filepath)
        content = (tmp_path / "end.gb").read_text()
        assert content.rstrip().endswith("//")


# ---------------------------------------------------------------------------
# read_genbank
# ---------------------------------------------------------------------------
class TestReadGenbank:
    """Test reading vectors from a GenBank file."""

    def test_returns_list_of_vectors(self, tmp_path):
        """Should return a list of Vector objects."""
        v = Vector(name="ReadVec", capacity=4.7, serotype="AAV2")
        filepath = str(tmp_path / "read.gb")
        write_genbank([v], filepath)
        result = read_genbank(filepath)
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Vector)

    def test_preserves_name(self, tmp_path):
        """Read vector should preserve the name."""
        v = Vector(name="NameVec", capacity=4.7, serotype="AAV2")
        filepath = str(tmp_path / "name.gb")
        write_genbank([v], filepath)
        result = read_genbank(filepath)
        assert result[0].name == "NameVec"

    def test_preserves_capacity(self, tmp_path):
        """Read vector should preserve the capacity."""
        v = Vector(name="CapRead", capacity=5.3, serotype="AAV9")
        filepath = str(tmp_path / "cap.gb")
        write_genbank([v], filepath)
        result = read_genbank(filepath)
        assert result[0].capacity == 5.3

    def test_preserves_serotype(self, tmp_path):
        """Read vector should preserve the serotype."""
        v = Vector(name="SerRead", capacity=4.7, serotype="AAV5")
        filepath = str(tmp_path / "ser.gb")
        write_genbank([v], filepath)
        result = read_genbank(filepath)
        assert result[0].serotype == "AAV5"

    def test_multiple_vectors(self, tmp_path):
        """Should return all vectors from the file."""
        vectors = [
            Vector(name="MR1", capacity=4.7, serotype="AAV2"),
            Vector(name="MR2", capacity=5.0, serotype="AAV9"),
        ]
        filepath = str(tmp_path / "multi_read.gb")
        write_genbank(vectors, filepath)
        result = read_genbank(filepath)
        assert len(result) == 2
        assert result[0].name == "MR1"
        assert result[1].name == "MR2"

    def test_nonexistent_file_raises(self):
        """Reading a non-existent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_genbank("/nonexistent/path/to/file.gb")


# ---------------------------------------------------------------------------
# Roundtrip
# ---------------------------------------------------------------------------
class TestRoundtrip:
    """Test write_genbank / read_genbank roundtrip preserves data."""

    def test_single_vector_roundtrip(self, tmp_path):
        """Single vector should survive a write-read roundtrip."""
        original = Vector(name="RT1", capacity=4.7, serotype="AAV9")
        filepath = str(tmp_path / "rt1.gb")
        write_genbank([original], filepath)
        loaded = read_genbank(filepath)
        assert len(loaded) == 1
        assert loaded[0].name == original.name
        assert loaded[0].capacity == original.capacity
        assert loaded[0].serotype == original.serotype

    def test_multiple_vectors_roundtrip(self, tmp_path):
        """Multiple vectors should all survive a roundtrip."""
        originals = [
            Vector(name="RT-A", capacity=4.7, serotype="AAV2"),
            Vector(name="RT-B", capacity=5.0, serotype="AAV5"),
            Vector(name="RT-C", capacity=6.2, serotype="Lentivirus"),
        ]
        filepath = str(tmp_path / "rt_multi.gb")
        write_genbank(originals, filepath)
        loaded = read_genbank(filepath)
        assert len(loaded) == len(originals)
        for orig, rt in zip(originals, loaded):
            assert rt.name == orig.name
            assert rt.capacity == orig.capacity
            assert rt.serotype == orig.serotype

    def test_vector_equality_after_roundtrip(self, tmp_path):
        """Vector loaded from file should equal the original."""
        original = Vector(name="EqVec", capacity=4.7, serotype="AAV8")
        filepath = str(tmp_path / "eq.gb")
        write_genbank([original], filepath)
        loaded = read_genbank(filepath)
        assert loaded[0] == original
