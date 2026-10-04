"""Test-driven development: CRISPR guide RNA design module."""

from src.crispr.grna_design import (
    calculate_efficiency_score,
    calculate_gc_content,
    design_grna,
    find_off_target_sites,
    validate_grna_sequence,
)


class TestGuideRNAValidation:
    """Test guide RNA sequence validation."""

    def test_valid_grna_sequence(self):
        """A valid gRNA sequence should pass validation."""
        seq = "GAGTCCGAGCAGAAGAAGAA"
        assert validate_grna_sequence(seq) is True

    def test_invalid_characters(self):
        """gRNA with invalid characters should fail."""
        seq = "GAGTCCGAGCAGAAGAAGAX"
        assert validate_grna_sequence(seq) is False

    def test_too_short(self):
        """gRNA shorter than 20nt should fail."""
        seq = "GAGTCCGAGCAGAAGAAG"
        assert validate_grna_sequence(seq) is False

    def test_too_long(self):
        """gRNA longer than 20nt should fail."""
        seq = "GAGTCCGAGCAGAAGAAGAAG"
        assert validate_grna_sequence(seq) is False

    def test_empty_sequence(self):
        """Empty sequence should fail."""
        assert validate_grna_sequence("") is False

    def test_lowercase_sequence(self):
        """Lowercase sequence should be accepted (normalized)."""
        seq = "gagtccgagcagaagaagaa"
        assert validate_grna_sequence(seq) is True


class TestGCContent:
    """Test GC content calculation."""

    def test_gc_content_50_percent(self):
        """GC content of 50% should be calculated correctly."""
        seq = "GAGTCCGAGCAGAAGAAGAA"
        gc = calculate_gc_content(seq)
        assert 0.45 <= gc <= 0.55

    def test_gc_content_all_gc(self):
        """All GC sequence should return 1.0."""
        seq = "GCGCGCGCGCGCGCGCGCGC"
        assert calculate_gc_content(seq) == 1.0

    def test_gc_content_no_gc(self):
        """No GC sequence should return 0.0."""
        seq = "ATATATATATATATATATAT"
        assert calculate_gc_content(seq) == 0.0

    def test_gc_content_empty(self):
        """Empty sequence should return 0.0."""
        assert calculate_gc_content("") == 0.0


class TestEfficiencyScore:
    """Test gRNA efficiency scoring."""

    def test_efficiency_score_range(self):
        """Efficiency score should be between 0 and 1."""
        seq = "GAGTCCGAGCAGAAGAAGAA"
        score = calculate_efficiency_score(seq)
        assert 0.0 <= score <= 1.0

    def test_high_gc_higher_score(self):
        """Higher GC content should generally yield higher scores."""
        high_gc = "GCGCGCGCGCGCGCGCGCGC"
        low_gc = "ATATATATATATATATATAT"
        high_score = calculate_efficiency_score(high_gc)
        low_score = calculate_efficiency_score(low_gc)
        assert high_score > low_score

    def test_perfect_grna_score(self):
        """A perfect gRNA should have a high score."""
        # Rule Set 2 optimal: G at position 20, no poly-T
        seq = "GAGTCCGAGCAGAAGAAGAG"
        score = calculate_efficiency_score(seq)
        assert score > 0.3


class TestOffTargetPrediction:
    """Test off-target site prediction."""

    def test_no_off_targets(self):
        """gRNA with no similar sites should return empty list."""
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "ATATATATATATATATATAT" * 100
        off_targets = find_off_target_sites(grna, genome, max_mismatches=3)
        assert len(off_targets) == 0

    def test_exact_match_found(self):
        """Exact match should be found as off-target."""
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "ATAT" + grna + "ATAT"
        off_targets = find_off_target_sites(grna, genome, max_mismatches=0)
        assert len(off_targets) >= 1

    def test_mismatch_tolerance(self):
        """Off-targets with mismatches should be found."""
        grna = "GAGTCCGAGCAGAAGAAGAA"
        # One mismatch at position 5
        mutated = "GAGTCCGAGCAGAAGAAGAT"
        genome = "ATAT" + mutated + "ATAT"
        off_targets = find_off_target_sites(grna, genome, max_mismatches=1)
        assert len(off_targets) >= 1

    def test_off_target_score(self):
        """Off-targets should have scores."""
        grna = "GAGTCCGAGCAGAAGAAGAA"
        genome = "ATAT" + grna + "ATAT"
        off_targets = find_off_target_sites(grna, genome, max_mismatches=0)
        for ot in off_targets:
            assert "score" in ot
            assert 0.0 <= ot["score"] <= 1.0


class TestGuideRNADesign:
    """Test full gRNA design pipeline."""

    def test_design_grna_returns_result(self):
        """Design pipeline should return a valid gRNA."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna(target, pam="NGG")
        assert result is not None
        assert "sequence" in result
        assert "efficiency" in result
        assert "off_targets" in result

    def test_design_grna_with_ngg_pam(self):
        """Design with NGG PAM should find valid targets."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna(target, pam="NGG")
        assert result["sequence"] == "GAGTCCGAGCAGAAGAAGAA"

    def test_design_grna_no_valid_target(self):
        """Design with no valid target should return None."""
        target = "ATATATATATATATATATAT"
        result = design_grna(target, pam="NGG")
        assert result is None

    def test_design_grna_efficiency_threshold(self):
        """Design should respect efficiency threshold."""
        target = "GAGTCCGAGCAGAAGAAGAAGGG"
        result = design_grna(target, pam="NGG", min_efficiency=0.0)
        assert result is not None
