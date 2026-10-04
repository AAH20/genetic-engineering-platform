"""Tests for DNA watermarking via synonymous codon substitution."""

from src.biosecurity.screening import embed_watermark, verify_watermark


class TestEmbedWatermark:
    def test_embed_returns_string(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        result = embed_watermark(seq, "1011")
        assert isinstance(result, str)

    def test_embed_preserves_length(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        result = embed_watermark(seq, "1011")
        assert len(result) == len(seq)

    def test_embed_empty_watermark_returns_original(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        result = embed_watermark(seq, "")
        assert result == seq

    def test_embed_does_not_change_non_watermarkable_codons(self):
        seq = "AAAGCTTCTCGTCCTGGTGTTCTT"
        result = embed_watermark(seq, "1011")
        assert result[:3] == "AAA"

    def test_embed_changes_watermarkable_codons(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        result = embed_watermark(seq, "1011")
        assert result != seq


class TestVerifyWatermark:
    def test_verify_correct_watermark_returns_true(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        watermarked = embed_watermark(seq, "1011")
        assert verify_watermark(watermarked, "1011") is True

    def test_verify_wrong_watermark_returns_false(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        watermarked = embed_watermark(seq, "1011")
        assert verify_watermark(watermarked, "0100") is False

    def test_verify_non_watermarked_sequence_returns_false(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        assert verify_watermark(seq, "1011") is False

    def test_verify_empty_watermark_returns_true(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        assert verify_watermark(seq, "") is True


class TestEmbedPreservesAminoAcids:
    """Verify that watermarking preserves the amino acid sequence."""

    # Standard genetic code for the codons used in watermark groups
    CODON_TABLE = {
        "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
        "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
        "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
        "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
        "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
        "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
        "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
        "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    }

    def _translate(self, seq: str) -> str:
        protein = []
        for i in range(0, len(seq) - 2, 3):
            codon = seq[i : i + 3]
            aa = self.CODON_TABLE.get(codon, "X")
            protein.append(aa)
        return "".join(protein)

    def test_embed_preserves_amino_acid_sequence(self):
        seq = "GCTTCTCGTCCTGGTGTTCTT"
        watermarked = embed_watermark(seq, "1011")
        assert self._translate(watermarked) == self._translate(seq)

    def test_embed_preserves_amino_acid_sequence_longer(self):
        seq = "GCTTCTCGTCCTGGTGTTCTTGCTTCTCGTCCTGGTGTTCTT"
        watermarked = embed_watermark(seq, "10110101")
        assert self._translate(watermarked) == self._translate(seq)
