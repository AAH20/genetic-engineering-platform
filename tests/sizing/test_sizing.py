"""TDD tests for sizing and onboarding module."""
import pytest

from src.sizing.sizing import (
    OnboardingGuide,
    SizingTier,
    estimate_cost,
    estimate_timeline,
    recommend_tier,
)


class TestSizingTier:
    def test_tier_values(self):
        assert SizingTier.LAB.value == "lab"
        assert SizingTier.BIOTECH_STARTUP.value == "biotech_startup"
        assert SizingTier.PHARMA.value == "pharma"

    def test_tier_from_string(self):
        assert SizingTier("lab") == SizingTier.LAB
        assert SizingTier("biotech_startup") == SizingTier.BIOTECH_STARTUP
        assert SizingTier("pharma") == SizingTier.PHARMA

    def test_tier_invalid(self):
        with pytest.raises(ValueError):
            SizingTier("invalid")


class TestRecommendTier:
    def test_lab_tier(self):
        rec = recommend_tier(
            team_size=3,
            monthly_budget=5000,
            compute_cores=8,
            storage_tb=1,
        )
        assert rec.tier == SizingTier.LAB

    def test_biotech_startup_tier(self):
        rec = recommend_tier(
            team_size=15,
            monthly_budget=50000,
            compute_cores=64,
            storage_tb=10,
        )
        assert rec.tier == SizingTier.BIOTECH_STARTUP

    def test_pharma_tier(self):
        rec = recommend_tier(
            team_size=100,
            monthly_budget=500000,
            compute_cores=512,
            storage_tb=100,
        )
        assert rec.tier == SizingTier.PHARMA

    def test_recommendation_has_resources(self):
        rec = recommend_tier(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert rec.recommended_cores > 0
        assert rec.recommended_storage_tb > 0

    def test_recommendation_has_services(self):
        rec = recommend_tier(
            team_size=5,
            monthly_budget=10000,
            compute_cores=16,
            storage_tb=2,
        )
        assert len(rec.required_services) > 0


class TestEstimateCost:
    def test_lab_cost(self):
        cost = estimate_cost(SizingTier.LAB)
        assert cost > 0
        assert cost < 10000

    def test_startup_cost(self):
        cost = estimate_cost(SizingTier.BIOTECH_STARTUP)
        assert cost > 10000

    def test_pharma_cost(self):
        cost = estimate_cost(SizingTier.PHARMA)
        assert cost > 100000

    def test_cost_increases_with_tier(self):
        lab = estimate_cost(SizingTier.LAB)
        startup = estimate_cost(SizingTier.BIOTECH_STARTUP)
        pharma = estimate_cost(SizingTier.PHARMA)
        assert lab < startup < pharma


class TestEstimateTimeline:
    def test_lab_timeline(self):
        weeks = estimate_timeline(SizingTier.LAB)
        assert weeks >= 1

    def test_startup_timeline(self):
        weeks = estimate_timeline(SizingTier.BIOTECH_STARTUP)
        assert weeks >= 4

    def test_pharma_timeline(self):
        weeks = estimate_timeline(SizingTier.PHARMA)
        assert weeks >= 12

    def test_timeline_increases_with_tier(self):
        lab = estimate_timeline(SizingTier.LAB)
        startup = estimate_timeline(SizingTier.BIOTECH_STARTUP)
        pharma = estimate_timeline(SizingTier.PHARMA)
        assert lab < startup < pharma


class TestOnboardingGuide:
    def test_guide_for_lab(self):
        guide = OnboardingGuide(SizingTier.LAB)
        steps = guide.get_steps()
        assert len(steps) > 0
        assert any("install" in s.lower() for s in steps)

    def test_guide_for_startup(self):
        guide = OnboardingGuide(SizingTier.BIOTECH_STARTUP)
        steps = guide.get_steps()
        assert len(steps) > 0
        assert any("cloud" in s.lower() or "deploy" in s.lower() for s in steps)

    def test_guide_for_pharma(self):
        guide = OnboardingGuide(SizingTier.PHARMA)
        steps = guide.get_steps()
        assert len(steps) > 0
        assert any("compliance" in s.lower() or "gxp" in s.lower() for s in steps)

    def test_guide_has_prerequisites(self):
        guide = OnboardingGuide(SizingTier.LAB)
        prereqs = guide.get_prerequisites()
        assert len(prereqs) > 0

    def test_guide_has_architecture(self):
        guide = OnboardingGuide(SizingTier.BIOTECH_STARTUP)
        arch = guide.get_architecture()
        assert len(arch) > 0
