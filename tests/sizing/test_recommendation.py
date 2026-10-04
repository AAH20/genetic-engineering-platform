"""TDD tests for recommendation explanation and tier capabilities."""

from src.sizing.sizing import (
    SizingTier,
    get_tier_capabilities,
    recommend_tier,
    recommend_tier_with_explanation,
)


class TestRecommendTierWithExplanation:
    def test_returns_dict_with_required_keys(self):
        result = recommend_tier_with_explanation(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert isinstance(result, dict)
        assert "tier" in result
        assert "cost" in result
        assert "timeline" in result
        assert "explanation" in result

    def test_includes_explanation_string(self):
        result = recommend_tier_with_explanation(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert isinstance(result["explanation"], str)
        assert len(result["explanation"]) > 0

    def test_tier_matches_recommend_tier(self):
        result = recommend_tier_with_explanation(
            team_size=15,
            monthly_budget=50000,
            compute_cores=64,
            storage_tb=10,
        )
        expected = recommend_tier(
            team_size=15,
            monthly_budget=50000,
            compute_cores=64,
            storage_tb=10,
        )
        assert result["tier"] == expected.tier

    def test_cost_matches_estimate(self):
        result = recommend_tier_with_explanation(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert result["cost"] > 0

    def test_timeline_matches_estimate(self):
        result = recommend_tier_with_explanation(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert result["timeline"] > 0

    def test_lab_tier_explanation(self):
        result = recommend_tier_with_explanation(
            team_size=3,
            monthly_budget=5000,
            compute_cores=8,
            storage_tb=1,
        )
        assert result["tier"] == SizingTier.LAB
        assert "lab" in result["explanation"].lower()

    def test_pharma_tier_explanation(self):
        result = recommend_tier_with_explanation(
            team_size=100,
            monthly_budget=500000,
            compute_cores=512,
            storage_tb=100,
        )
        assert result["tier"] == SizingTier.PHARMA
        assert "pharma" in result["explanation"].lower()


class TestGetTierCapabilities:
    def test_returns_dict_with_capability_keys(self):
        caps = get_tier_capabilities(SizingTier.LAB)
        assert isinstance(caps, dict)
        assert "max_samples" in caps
        assert "max_compute_cores" in caps
        assert "max_storage_tb" in caps
        assert "max_team_size" in caps
        assert "services" in caps

    def test_lab_tier_correct_limits(self):
        caps = get_tier_capabilities(SizingTier.LAB)
        assert caps["max_samples"] == 1000
        assert caps["max_compute_cores"] == 8
        assert caps["max_storage_tb"] == 1.0
        assert caps["max_team_size"] == 10
        assert "app" in caps["services"]
        assert "postgres" in caps["services"]

    def test_pharma_tier_highest_limits(self):
        lab = get_tier_capabilities(SizingTier.LAB)
        startup = get_tier_capabilities(SizingTier.BIOTECH_STARTUP)
        pharma = get_tier_capabilities(SizingTier.PHARMA)

        assert pharma["max_samples"] > startup["max_samples"] > lab["max_samples"]
        assert pharma["max_compute_cores"] > startup["max_compute_cores"] > lab["max_compute_cores"]
        assert pharma["max_storage_tb"] > startup["max_storage_tb"] > lab["max_storage_tb"]
        assert pharma["max_team_size"] > startup["max_team_size"] > lab["max_team_size"]

    def test_pharma_has_compliance_services(self):
        caps = get_tier_capabilities(SizingTier.PHARMA)
        assert "compliance" in caps["services"]
        assert "audit" in caps["services"]

    def test_lab_no_compliance_services(self):
        caps = get_tier_capabilities(SizingTier.LAB)
        assert "compliance" not in caps["services"]
        assert "audit" not in caps["services"]
