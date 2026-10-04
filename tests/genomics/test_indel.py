"""Test-driven development: Indel and structural variant calling."""

from src.genomics.variant_calling import (
    call_indels,
    call_structural_variants,
)


class TestCallIndelsNoIndels:
    """call_indels with no indels should return empty list."""

    def test_no_indels_empty_reads(self):
        """Empty reads should return no indels."""
        reference = "ACGTACGT"
        assert call_indels(reference, []) == []

    def test_no_indels_matching_reads(self):
        """Reads matching reference exactly should return no indels."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTACGT",
        ]
        assert call_indels(reference, reads) == []


class TestCallIndelsDeletion:
    """call_indels should detect deletions."""

    def test_deletion_returns_variant(self):
        """Reads with a deletion should return a Variant with correct ref/alt."""
        reference = "ACGTACGT"
        # Deletion of "CG" at positions 3-4 (0-indexed 2-3)
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACTACGT",   # deleted "CG" at pos 3-4
            "ACTACGT",
            "ACTACGT",
        ]
        variants = call_indels(reference, reads, min_coverage=3)
        assert len(variants) >= 1
        del_var = [v for v in variants if v.ref != v.alt and len(v.ref) > len(v.alt)]
        assert len(del_var) >= 1
        # The deleted bases should be "CG" or similar
        assert "CG" in del_var[0].ref or "GT" in del_var[0].ref

    def test_deletion_ref_alt_correct(self):
        """Deletion variant should have ref containing deleted bases and alt shorter."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACTACGT",   # deleted "CG"
            "ACTACGT",
            "ACTACGT",
        ]
        variants = call_indels(reference, reads, min_coverage=3)
        assert len(variants) >= 1
        # Find the deletion variant
        del_variants = [v for v in variants if len(v.ref) > len(v.alt)]
        assert len(del_variants) >= 1
        # ref should be longer than alt for a deletion
        assert len(del_variants[0].ref) > len(del_variants[0].alt)


class TestCallIndelsInsertion:
    """call_indels should detect insertions."""

    def test_insertion_returns_variant(self):
        """Reads with an insertion should return a Variant with correct ref/alt."""
        reference = "ACGTACGT"
        # Insertion of "GG" after position 4
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTGGACGT",  # inserted "GG" after pos 4
            "ACGTGGACGT",
            "ACGTGGACGT",
        ]
        variants = call_indels(reference, reads, min_coverage=3)
        assert len(variants) >= 1
        ins_var = [v for v in variants if len(v.alt) > len(v.ref)]
        assert len(ins_var) >= 1
        # alt should be longer than ref for an insertion
        assert len(ins_var[0].alt) > len(ins_var[0].ref)

    def test_insertion_ref_alt_correct(self):
        """Insertion variant should have alt containing inserted bases."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTGGACGT",  # inserted "GG"
            "ACGTGGACGT",
            "ACGTGGACGT",
        ]
        variants = call_indels(reference, reads, min_coverage=3)
        assert len(variants) >= 1
        ins_variants = [v for v in variants if len(v.alt) > len(v.ref)]
        assert len(ins_variants) >= 1
        # alt should contain the inserted bases
        assert "GG" in ins_variants[0].alt


class TestCallIndelsMinCoverage:
    """call_indels should respect min_coverage parameter."""

    def test_min_coverage_filters_low_support(self):
        """Indels with support below min_coverage should not be called."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTACGT",
            "ACTACGT",   # only 1 read supports deletion
        ]
        variants = call_indels(reference, reads, min_coverage=3)
        assert variants == []

    def test_min_coverage_allows_high_support(self):
        """Indels with support >= min_coverage should be called."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACTACGT",   # 4 reads support deletion
            "ACTACGT",
            "ACTACGT",
            "ACTACGT",
        ]
        variants = call_indels(reference, reads, min_coverage=3)
        assert len(variants) >= 1


class TestCallStructuralVariantsNoSVs:
    """call_structural_variants with no SVs should return empty list."""

    def test_no_svs_empty_reads(self):
        """Empty reads should return no SVs."""
        reference = "ACGTACGT"
        assert call_structural_variants(reference, []) == []

    def test_no_svs_matching_reads(self):
        """Reads matching reference should return no SVs."""
        reference = "ACGTACGT"
        reads = [
            "ACGTACGT",
            "ACGTACGT",
            "ACGTACGT",
        ]
        assert call_structural_variants(reference, reads) == []


class TestCallStructuralVariantsLargeDeletion:
    """call_structural_variants should detect large deletions."""

    def test_large_deletion_returns_dict(self):
        """Large deletion should return dict with type='deletion'."""
        reference = "ACGTACGTACGTACGTACGT"  # 20bp
        # Large deletion of 10bp in the middle
        reads = [
            "ACGTACGTACGTACGTACGT",
            "ACGTACGTACGTACGTACGT",
            "ACGTACGTACGTACGT",      # deleted 10bp from middle
            "ACGTACGTACGTACGT",
            "ACGTACGTACGTACGT",
        ]
        svs = call_structural_variants(reference, reads)
        assert len(svs) >= 1
        del_svs = [sv for sv in svs if sv["type"] == "deletion"]
        assert len(del_svs) >= 1
        assert "start" in del_svs[0]
        assert "end" in del_svs[0]
        assert "size" in del_svs[0]
        assert del_svs[0]["size"] > 0
