"""TDD tests for cost and timeline estimation in sizing module."""

from src.sizing.sizing import (
    SizingTier,
    compare_tiers,
    estimate_cost,
    estimate_timeline,
    recommend_tier,
)


class TestSizingRecommendationCostTimeline:
    """SizingRecommendation should include cost and timeline fields."""

    def test_recommendation_has_cost_field(self):
        rec = recommend_tier(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert hasattr(rec, "cost")
        assert rec.cost > 0

    def test_recommendation_has_timeline_field(self):
        rec = recommend_tier(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert hasattr(rec, "timeline")
        assert rec.timeline > 0

    def test_recommendation_cost_matches_estimate(self):
        rec = recommend_tier(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        expected_cost = estimate_cost(rec.tier)
        assert rec.cost == expected_cost

    def test_recommendation_timeline_matches_estimate(self):
        rec = recommend_tier(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        expected_timeline = estimate_timeline(rec.tier, team_size=5)
        assert rec.timeline == expected_timeline


class TestEstimateTimelineWithTeamSize:
    """estimate_timeline should account for team size."""

    def test_returns_positive_integer(self):
        result = estimate_timeline(SizingTier.LAB, team_size=5)
        assert isinstance(result, int)
        assert result > 0

    def test_larger_team_returns_fewer_days(self):
        small_team = estimate_timeline(SizingTier.BIOTECH_STARTUP, team_size=5)
        large_team = estimate_timeline(SizingTier.BIOTECH_STARTUP, team_size=20)
        assert large_team < small_team

    def test_timeline_increases_with_tier(self):
        lab = estimate_timeline(SizingTier.LAB, team_size=10)
        startup = estimate_timeline(SizingTier.BIOTECH_STARTUP, team_size=10)
        pharma = estimate_timeline(SizingTier.PHARMA, team_size=10)
        assert lab < startup < pharma


class TestCompareTiers:
    """compare_tiers should compare two tiers across cost, timeline, and capabilities."""

    def test_returns_dict(self):
        result = compare_tiers(SizingTier.LAB, SizingTier.BIOTECH_STARTUP)
        assert isinstance(result, dict)

    def test_has_comparison_keys(self):
        result = compare_tiers(SizingTier.LAB, SizingTier.BIOTECH_STARTUP)
        assert "cost" in result
        assert "timeline" in result
        assert "capabilities" in result

    def test_same_tier_returns_equal(self):
        result = compare_tiers(SizingTier.LAB, SizingTier.LAB)
        assert result["cost"]["equal"] is True
        assert result["timeline"]["equal"] is True
        assert result["capabilities"]["equal"] is True

    def test_different_tiers_not_equal(self):
        result = compare_tiers(SizingTier.LAB, SizingTier.PHARMA)
        assert result["cost"]["equal"] is False
        assert result["timeline"]["equal"] is False
