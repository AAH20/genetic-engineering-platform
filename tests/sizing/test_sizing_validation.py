"""Validation tests for sizing module."""
import pytest

from src.sizing.sizing import (
    OnboardingGuide,
    SizingTier,
    estimate_cost,
    recommend_tier,
)


class TestRecommendTierValidation:
    def test_team_size_zero_raises(self):
        with pytest.raises(ValueError):
            recommend_tier(
                team_size=0,
                monthly_budget=5000,
                compute_cores=8,
                storage_tb=1,
            )

    def test_negative_budget_raises(self):
        with pytest.raises(ValueError):
            recommend_tier(
                team_size=5,
                monthly_budget=-100,
                compute_cores=8,
                storage_tb=1,
            )

    def test_negative_sample_count_raises(self):
        with pytest.raises(ValueError):
            recommend_tier(
                team_size=5,
                monthly_budget=5000,
                compute_cores=8,
                storage_tb=1,
                sample_count=-1,
            )


class TestEstimateCostValidation:
    def test_negative_team_size_raises(self):
        with pytest.raises(ValueError):
            estimate_cost(SizingTier.LAB, team_size=-1)

    def test_negative_budget_raises(self):
        with pytest.raises(ValueError):
            estimate_cost(SizingTier.LAB, monthly_budget=-100)


class TestOnboardingGuideValidation:
    def test_invalid_tier_raises(self):
        with pytest.raises(ValueError):
            OnboardingGuide("invalid")
