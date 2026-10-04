"""Regression tests for bug fixes discovered by property-based testing."""


class TestVAFRegression:
    """VAF must always be in [0, 1] even when alt_count > total_count."""

    def test_vaf_clamped_above_one(self):
        from src.genomics.variant_calling import calculate_vaf
        assert calculate_vaf(2, 1) == 1.0

    def test_vaf_clamped_below_zero(self):
        from src.genomics.variant_calling import calculate_vaf
        assert calculate_vaf(-1, 10) == 0.0

    def test_vaf_normal_case(self):
        from src.genomics.variant_calling import calculate_vaf
        assert calculate_vaf(3, 10) == 0.3

    def test_vaf_zero_total(self):
        from src.genomics.variant_calling import calculate_vaf
        assert calculate_vaf(0, 0) == 0.0
