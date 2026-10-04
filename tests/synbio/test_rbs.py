"""Test-driven development: RBS calculator and designer."""

from src.synbio.genetic_circuits import calculate_rbs_strength, design_rbs


class TestCalculateRbsStrength:
    """Test calculate_rbs_strength returns float in [0,1]."""

    def test_returns_float(self):
        result = calculate_rbs_strength("AGGAGG", start_position=0)
        assert isinstance(result, float)

    def test_in_range(self):
        result = calculate_rbs_strength("AGGAGG", start_position=0)
        assert 0.0 <= result <= 1.0

    def test_strong_rbs(self):
        result = calculate_rbs_strength("AGGAGG", start_position=0)
        assert result > 0.5

    def test_weak_rbs(self):
        result = calculate_rbs_strength("GCGCGC", start_position=0)
        assert result < 0.5

    def test_empty_sequence(self):
        result = calculate_rbs_strength("", start_position=0)
        assert 0.0 <= result <= 1.0


class TestDesignRbs:
    """Test design_rbs returns string."""

    def test_returns_string(self):
        result = design_rbs("MKVLAAALLL", host="E.coli")
        assert isinstance(result, str)

    def test_ecoli_contains_aggagg(self):
        result = design_rbs("MKVLAAALLL", host="E.coli")
        assert "AGGAGG" in result

    def test_different_hosts_differ(self):
        ecoli_result = design_rbs("MKVLAAALLL", host="E.coli")
        subtilis_result = design_rbs("MKVLAAALLL", host="B.subtilis")
        assert ecoli_result != subtilis_result

    def test_empty_protein(self):
        result = design_rbs("", host="E.coli")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_cerevisiae_host(self):
        result = design_rbs("MKVLAAALLL", host="S.cerevisiae")
        assert isinstance(result, str)
        assert len(result) > 0
