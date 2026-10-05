"""TDD tests for serialization/export of OnboardingGuide and recommend_all_tiers."""
import json

import pytest

from src.sizing.sizing import (
    OnboardingGuide,
    SizingRecommendation,
    SizingTier,
    recommend_all_tiers,
)


class TestOnboardingGuideToDict:
    def test_returns_dict_with_tier(self):
        guide = OnboardingGuide(SizingTier.LAB)
        result = guide.to_dict()
        assert isinstance(result, dict)
        assert result["tier"] == SizingTier.LAB.value

    def test_contains_prerequisites(self):
        guide = OnboardingGuide(SizingTier.LAB)
        result = guide.to_dict()
        assert "prerequisites" in result
        assert "Python 3.10+" in result["prerequisites"]

    def test_contains_steps(self):
        guide = OnboardingGuide(SizingTier.LAB)
        result = guide.to_dict()
        assert "steps" in result
        assert len(result["steps"]) > 0

    def test_contains_architecture(self):
        guide = OnboardingGuide(SizingTier.LAB)
        result = guide.to_dict()
        assert "architecture" in result
        assert len(result["architecture"]) > 0


class TestOnboardingGuideToJson:
    def test_returns_valid_json_string(self):
        guide = OnboardingGuide(SizingTier.BIOTECH_STARTUP)
        result = guide.to_json()
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
        assert parsed["tier"] == SizingTier.BIOTECH_STARTUP.value

    def test_json_preserves_steps(self):
        guide = OnboardingGuide(SizingTier.PHARMA)
        result = guide.to_json()
        parsed = json.loads(result)
        assert parsed["steps"] == guide.get_steps()


class TestOnboardingGuideFromDict:
    def test_creates_guide_from_dict(self):
        data = {"tier": SizingTier.LAB.value}
        guide = OnboardingGuide.from_dict(data)
        assert isinstance(guide, OnboardingGuide)
        assert guide.tier == SizingTier.LAB

    def test_created_guide_has_same_content(self):
        data = {"tier": SizingTier.PHARMA.value}
        guide = OnboardingGuide.from_dict(data)
        assert guide.get_steps() == OnboardingGuide(SizingTier.PHARMA).get_steps()

    def test_invalid_tier_raises(self):
        with pytest.raises(ValueError):
            OnboardingGuide.from_dict({"tier": "invalid"})


class TestOnboardingGuideRoundtrip:
    def test_to_dict_from_dict_roundtrip(self):
        for tier in (SizingTier.LAB, SizingTier.BIOTECH_STARTUP, SizingTier.PHARMA):
            guide = OnboardingGuide(tier)
            data = guide.to_dict()
            restored = OnboardingGuide.from_dict(data)
            assert restored.tier == guide.tier
            assert restored.get_steps() == guide.get_steps()
            assert restored.get_prerequisites() == guide.get_prerequisites()
            assert restored.get_architecture() == guide.get_architecture()

    def test_to_json_from_dict_roundtrip(self):
        guide = OnboardingGuide(SizingTier.BIOTECH_STARTUP)
        parsed = json.loads(guide.to_json())
        restored = OnboardingGuide.from_dict(parsed)
        assert restored.tier == guide.tier
        assert restored.get_steps() == guide.get_steps()


class TestRecommendAllTiers:
    def test_returns_list_of_recommendations(self):
        result = recommend_all_tiers(
            team_size=5,
            monthly_budget=10000,
            compute_cores=8,
            storage_tb=1.0,
        )
        assert isinstance(result, list)
        assert all(isinstance(r, SizingRecommendation) for r in result)

    def test_returns_all_tiers(self):
        result = recommend_all_tiers(
            team_size=5,
            monthly_budget=10000,
            compute_cores=8,
            storage_tb=1.0,
        )
        assert len(result) == 3
        assert {r.tier for r in result} == {
            SizingTier.LAB,
            SizingTier.BIOTECH_STARTUP,
            SizingTier.PHARMA,
        }

    def test_tiers_in_ascending_order(self):
        result = recommend_all_tiers(
            team_size=5,
            monthly_budget=10000,
            compute_cores=8,
            storage_tb=1.0,
        )
        assert result[0].tier == SizingTier.LAB
        assert result[1].tier == SizingTier.BIOTECH_STARTUP
        assert result[2].tier == SizingTier.PHARMA

    def test_each_recommendation_has_cost_and_timeline(self):
        result = recommend_all_tiers(
            team_size=5,
            monthly_budget=10000,
            compute_cores=8,
            storage_tb=1.0,
        )
        for rec in result:
            assert rec.cost > 0
            assert rec.timeline > 0

    def test_validation_errors(self):
        with pytest.raises(ValueError):
            recommend_all_tiers(team_size=0, monthly_budget=1000, compute_cores=8, storage_tb=1.0)
        with pytest.raises(ValueError):
            recommend_all_tiers(team_size=5, monthly_budget=-1, compute_cores=8, storage_tb=1.0)
