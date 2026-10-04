"""TDD tests for gene therapy titer optimization."""
import pytest

from src.genetherapy.vector_design import compare_vector_types, optimize_titer


class TestOptimizeTiter:
    """Test titer optimization across vector types."""

    def test_optimize_small_transgene(self):
        result = optimize_titer(2.0, 0.9)
        assert result is not None
        assert "best_vector" in result
        assert "titer" in result
        assert result["titer"] > 0

    def test_optimize_large_transgene(self):
        result = optimize_titer(4.5, 0.9)
        assert result is not None
        assert result["titer"] > 0

    def test_optimize_returns_all_titers(self):
        result = optimize_titer(2.0, 0.9)
        assert "all_titers" in result
        assert isinstance(result["all_titers"], dict)
        assert len(result["all_titers"]) == 3

    def test_optimize_best_is_max(self):
        result = optimize_titer(2.0, 0.9)
        assert result["titer"] == max(result["all_titers"].values())

    def test_optimize_invalid_size(self):
        with pytest.raises(ValueError):
            optimize_titer(-1.0, 0.9)

    def test_optimize_invalid_purity(self):
        with pytest.raises(ValueError):
            optimize_titer(2.0, 1.5)


class TestCompareVectorTypes:
    """Test vector type comparison."""

    def test_compare_returns_dict(self):
        result = compare_vector_types(2.0, 0.9)
        assert isinstance(result, dict)
        assert len(result) == 3

    def test_compare_includes_all_types(self):
        result = compare_vector_types(2.0, 0.9)
        assert "AAV" in result
        assert "Lentivirus" in result
        assert "Adenovirus" in result

    def test_compare_titers_positive(self):
        result = compare_vector_types(2.0, 0.9)
        for titer in result.values():
            assert titer > 0

    def test_compare_large_transgene(self):
        result = compare_vector_types(4.5, 0.9)
        assert isinstance(result, dict)
