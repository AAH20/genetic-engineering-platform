"""Test-driven development: terminator efficiency prediction and design."""
from src.synbio.genetic_circuits import design_terminator, predict_terminator_efficiency


class TestPredictTerminatorEfficiency:
    """Test predict_terminator_efficiency returns float in [0,1]."""

    def test_returns_float(self):
        result = predict_terminator_efficiency("GGGCCCAAATTT")
        assert isinstance(result, float)

    def test_in_range(self):
        result = predict_terminator_efficiency("GGGCCCAAATTT")
        assert 0.0 <= result <= 1.0

    def test_strong_terminator(self):
        # Strong terminator: GC-rich stem, U-rich tail
        result = predict_terminator_efficiency("GGGCCCAAATTTTTTT")
        assert result > 0.5

    def test_weak_terminator(self):
        # Weak terminator: AT-rich, no U-rich tail
        result = predict_terminator_efficiency("ATATATATATAT")
        assert result < 0.5

    def test_empty_sequence(self):
        result = predict_terminator_efficiency("")
        assert 0.0 <= result <= 1.0


class TestDesignTerminator:
    """Test design_terminator returns string."""

    def test_returns_string(self):
        result = design_terminator(host="E.coli")
        assert isinstance(result, str)

    def test_ecoli_contains_u_rich_tail(self):
        result = design_terminator(host="E.coli")
        # U-rich tail means T-rich in DNA (T is DNA equivalent of U)
        assert "TTTT" in result

    def test_different_hosts_differ(self):
        ecoli_result = design_terminator(host="E.coli")
        subtilis_result = design_terminator(host="B.subtilis")
        assert ecoli_result != subtilis_result

    def test_default_host(self):
        result = design_terminator()
        assert isinstance(result, str)
        assert len(result) > 0
