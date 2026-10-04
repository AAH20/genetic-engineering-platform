"""Test-driven development: promoter strength prediction and design."""
from src.synbio.genetic_circuits import design_promoter, predict_promoter_strength


class TestPredictPromoterStrength:
    """Test predict_promoter_strength returns float in [0,1]."""

    def test_returns_float(self):
        result = predict_promoter_strength("TTGACATATAAT")
        assert isinstance(result, float)

    def test_in_range(self):
        result = predict_promoter_strength("TTGACATATAAT")
        assert 0.0 <= result <= 1.0

    def test_strong_promoter(self):
        # Consensus -35 (TTGACA) and -10 (TATAAT) with optimal 17bp spacing
        strong = "TTGACAAAAAAAAAAAAAAAAATATAAT"
        result = predict_promoter_strength(strong)
        assert result > 0.5

    def test_weak_promoter(self):
        # No consensus -35 or -10 boxes
        weak = "GCGCGCGCGCGCGCGCGCGCGCGCGCGCGC"
        result = predict_promoter_strength(weak)
        assert result < 0.5

    def test_empty_sequence(self):
        result = predict_promoter_strength("")
        assert 0.0 <= result <= 1.0


class TestDesignPromoter:
    """Test design_promoter returns string."""

    def test_returns_string(self):
        result = design_promoter(host="E.coli")
        assert isinstance(result, str)

    def test_ecli_contains_boxes(self):
        result = design_promoter(host="E.coli")
        assert "TTGACA" in result  # -35 box
        assert "TATAAT" in result  # -10 box

    def test_different_hosts_differ(self):
        ecoli_result = design_promoter(host="E.coli")
        subtilis_result = design_promoter(host="B.subtilis")
        assert ecoli_result != subtilis_result

    def test_default_host(self):
        result = design_promoter()
        assert isinstance(result, str)
        assert len(result) > 0
