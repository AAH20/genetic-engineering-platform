"""Test-driven development: Variant filtering by VAF, quality, and type."""

from src.genomics.variant_calling import (
    Variant,
    filter_variants_by_quality,
    filter_variants_by_type,
    filter_variants_by_vaf,
)


class TestFilterVariantsByVaf:
    """Test filter_variants_by_vaf function."""

    def test_vaf_empty_list_returns_empty(self):
        """filter_variants_by_vaf with empty list returns []."""
        result = filter_variants_by_vaf([])
        assert result == []

    def test_vaf_filters_low_vaf_variants(self):
        """filter_variants_by_vaf filters out variants below threshold."""
        low_vaf = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=3.0)
        high_vaf = Variant(chrom="chr1", pos=200, ref="C", alt="T", quality=50.0)
        result = filter_variants_by_vaf([low_vaf, high_vaf], min_vaf=0.05)
        assert low_vaf not in result
        assert high_vaf in result

    def test_vaf_keeps_high_vaf_variants(self):
        """filter_variants_by_vaf keeps variants at or above threshold."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=10.0)
        v2 = Variant(chrom="chr1", pos=200, ref="C", alt="T", quality=80.0)
        result = filter_variants_by_vaf([v1, v2], min_vaf=0.05)
        assert v1 in result
        assert v2 in result


class TestFilterVariantsByQuality:
    """Test filter_variants_by_quality function."""

    def test_quality_filters_low_quality(self):
        """filter_variants_by_quality filters out low quality variants."""
        low_q = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=20.0)
        high_q = Variant(chrom="chr1", pos=200, ref="C", alt="T", quality=50.0)
        result = filter_variants_by_quality([low_q, high_q], min_quality=30.0)
        assert low_q not in result
        assert high_q in result

    def test_quality_keeps_high_quality(self):
        """filter_variants_by_quality keeps variants at or above threshold."""
        v1 = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=40.0)
        v2 = Variant(chrom="chr1", pos=200, ref="C", alt="T", quality=100.0)
        result = filter_variants_by_quality([v1, v2], min_quality=30.0)
        assert v1 in result
        assert v2 in result


class TestFilterVariantsByType:
    """Test filter_variants_by_type function."""

    def test_type_filters_by_type(self):
        """filter_variants_by_type filters variants by SNV, INDEL, or SV."""
        snv = Variant(chrom="chr1", pos=100, ref="A", alt="G", quality=50.0)
        indel = Variant(chrom="chr1", pos=200, ref="A", alt="AT", quality=50.0)
        sv = Variant(
            chrom="chr1",
            pos=300,
            ref="A",
            alt="A" + "T" * 50,
            quality=50.0,
        )

        snv_result = filter_variants_by_type([snv, indel, sv], variant_type="SNV")
        assert snv in snv_result
        assert indel not in snv_result
        assert sv not in snv_result

        indel_result = filter_variants_by_type([snv, indel, sv], variant_type="INDEL")
        assert snv not in indel_result
        assert indel in indel_result
        assert sv not in indel_result

        sv_result = filter_variants_by_type([snv, indel, sv], variant_type="SV")
        assert snv not in sv_result
        assert indel not in sv_result
        assert sv in sv_result
