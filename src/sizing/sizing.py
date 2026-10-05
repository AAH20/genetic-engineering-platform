"""Sizing and onboarding module for tier recommendations.

Provides tiered sizing (lab / biotech_startup / pharma), cost/timeline
estimates, and onboarding guides for each tier.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum


class SizingTier(str, Enum):
    """Deployment tiers for the genetic engineering platform."""

    LAB = "lab"
    BIOTECH_STARTUP = "biotech_startup"
    PHARMA = "pharma"


@dataclass
class SizingRecommendation:
    """Recommendation result for a given set of requirements.

    Attributes:
        tier: Recommended deployment tier.
        recommended_cores: Suggested CPU core count.
        recommended_storage_tb: Suggested storage in terabytes.
        required_services: List of service names that should be deployed.
        cost: Estimated monthly cost in USD.
        timeline: Estimated onboarding timeline in days.
    """

    tier: SizingTier
    recommended_cores: int
    recommended_storage_tb: float
    required_services: list[str] = field(default_factory=list)
    cost: int = 0
    timeline: int = 0


@dataclass
class _TierProfile:
    min_team: int
    min_budget: int
    min_cores: int
    min_storage_tb: float
    cores: int
    storage_tb: float
    services: list[str]


_TIER_PROFILES: dict[SizingTier, _TierProfile] = {
    SizingTier.LAB: _TierProfile(
        min_team=1, min_budget=0, min_cores=1, min_storage_tb=0.1,
        cores=8, storage_tb=1.0,
        services=["app", "postgres"],
    ),
    SizingTier.BIOTECH_STARTUP: _TierProfile(
        min_team=10, min_budget=20000, min_cores=16, min_storage_tb=5.0,
        cores=64, storage_tb=10.0,
        services=["app", "postgres", "redis", "gpu"],
    ),
    SizingTier.PHARMA: _TierProfile(
        min_team=50, min_budget=200000, min_cores=128, min_storage_tb=50.0,
        cores=512, storage_tb=100.0,
        services=["app", "postgres", "redis", "gpu", "compliance", "audit"],
    ),
}


_TIER_CAPABILITIES: dict[SizingTier, dict] = {
    SizingTier.LAB: {
        "max_samples": 1000,
        "max_compute_cores": 8,
        "max_storage_tb": 1.0,
        "max_team_size": 10,
        "services": ["app", "postgres"],
    },
    SizingTier.BIOTECH_STARTUP: {
        "max_samples": 100000,
        "max_compute_cores": 64,
        "max_storage_tb": 10.0,
        "max_team_size": 50,
        "services": ["app", "postgres", "redis", "gpu"],
    },
    SizingTier.PHARMA: {
        "max_samples": 10000000,
        "max_compute_cores": 512,
        "max_storage_tb": 100.0,
        "max_team_size": 500,
        "services": ["app", "postgres", "redis", "gpu", "compliance", "audit"],
    },
}


def recommend_tier_with_explanation(
    team_size: int,
    monthly_budget: int,
    compute_cores: int,
    storage_tb: float,
    sample_count: int = 0,
) -> dict:
    """Recommend a tier and return a dict with explanation.

    Returns dict with 'tier', 'cost', 'timeline', 'explanation' keys.
    """
    rec = recommend_tier(team_size, monthly_budget, compute_cores, storage_tb, sample_count)
    explanation = (
        f"Recommended {rec.tier.value} tier for team of {team_size} "
        f"with budget ${monthly_budget}/month, {compute_cores} cores, "
        f"{storage_tb}TB storage."
    )
    return {
        "tier": rec.tier,
        "cost": rec.cost,
        "timeline": rec.timeline,
        "explanation": explanation,
    }


def get_tier_capabilities(tier: SizingTier) -> dict:
    """Return capabilities of a tier (max_samples, max_compute, etc.)."""
    if tier not in _TIER_CAPABILITIES:
        raise ValueError(f"Invalid tier: {tier!r}")
    return dict(_TIER_CAPABILITIES[tier])


def recommend_tier(
    team_size: int,
    monthly_budget: int,
    compute_cores: int,
    storage_tb: float,
    sample_count: int = 0,
) -> SizingRecommendation:
    """Recommend a deployment tier based on team and resource requirements.

    Evaluates tiers in ascending order and returns the highest matching tier.
    """
    if team_size <= 0:
        raise ValueError("team_size must be positive")
    if monthly_budget < 0:
        raise ValueError("monthly_budget must be non-negative")
    if sample_count < 0:
        raise ValueError("sample_count must be non-negative")

    tier_order = [SizingTier.LAB, SizingTier.BIOTECH_STARTUP, SizingTier.PHARMA]
    matched = SizingTier.LAB

    for tier in tier_order:
        profile = _TIER_PROFILES[tier]
        if (
            team_size >= profile.min_team
            and monthly_budget >= profile.min_budget
            and compute_cores >= profile.min_cores
            and storage_tb >= profile.min_storage_tb
        ):
            matched = tier

    profile = _TIER_PROFILES[matched]
    return SizingRecommendation(
        tier=matched,
        recommended_cores=profile.cores,
        recommended_storage_tb=profile.storage_tb,
        required_services=list(profile.services),
        cost=estimate_cost(matched),
        timeline=estimate_timeline(matched, team_size=team_size),
    )


def estimate_cost(
    tier: SizingTier,
    team_size: int = 0,
    monthly_budget: int = 0,
) -> int:
    """Estimate monthly cost in USD for a given tier."""
    if team_size < 0:
        raise ValueError("team_size must be non-negative")
    if monthly_budget < 0:
        raise ValueError("monthly_budget must be non-negative")

    costs = {
        SizingTier.LAB: 500,
        SizingTier.BIOTECH_STARTUP: 25000,
        SizingTier.PHARMA: 200000,
    }
    return costs[tier]


def estimate_timeline(tier: SizingTier, team_size: int = 0) -> int:
    """Estimate onboarding timeline in days for a given tier.

    Larger teams can parallelize work, reducing the timeline.
    """
    if team_size < 0:
        raise ValueError("team_size must be non-negative")

    base_days = {
        SizingTier.LAB: 7,
        SizingTier.BIOTECH_STARTUP: 42,
        SizingTier.PHARMA: 112,
    }
    return max(1, base_days[tier] - team_size)


def compare_tiers(tier1: SizingTier, tier2: SizingTier) -> dict:
    """Compare two tiers across cost, timeline, and capabilities.

    Returns a dict with comparison results for each dimension.
    """
    cost1 = estimate_cost(tier1)
    cost2 = estimate_cost(tier2)
    timeline1 = estimate_timeline(tier1)
    timeline2 = estimate_timeline(tier2)
    services1 = set(_TIER_PROFILES[tier1].services)
    services2 = set(_TIER_PROFILES[tier2].services)

    return {
        "cost": {
            "tier1": cost1,
            "tier2": cost2,
            "equal": cost1 == cost2,
            "difference": cost1 - cost2,
        },
        "timeline": {
            "tier1": timeline1,
            "tier2": timeline2,
            "equal": timeline1 == timeline2,
            "difference": timeline1 - timeline2,
        },
        "capabilities": {
            "tier1_only": sorted(services1 - services2),
            "tier2_only": sorted(services2 - services1),
            "equal": services1 == services2,
        },
    }


class OnboardingGuide:
    """Step-by-step onboarding guide for each deployment tier."""

    def __init__(self, tier: SizingTier) -> None:
        if not isinstance(tier, SizingTier):
            raise ValueError(f"Invalid tier: {tier!r}")
        self.tier = tier

    def get_prerequisites(self) -> list[str]:
        """List prerequisites for onboarding."""
        base = ["Python 3.10+", "Docker", "Git"]
        if self.tier in (SizingTier.BIOTECH_STARTUP, SizingTier.PHARMA):
            base.append("Cloud provider account (AWS/GCP/Azure)")
        if self.tier == SizingTier.PHARMA:
            base.append("GxP compliance documentation")
        return base

    def get_steps(self) -> list[str]:
        """Return ordered onboarding steps for the tier."""
        if self.tier == SizingTier.LAB:
            return [
                "Install Python dependencies with pip install -e '.[dev]'",
                "Run docker-compose up -d to start local services",
                "Execute pytest to verify all tests pass",
                "Run examples/basic_usage.py for a smoke test",
            ]
        elif self.tier == SizingTier.BIOTECH_STARTUP:
            return [
                "Provision cloud Kubernetes cluster",
                "Configure Terraform for infrastructure-as-code",
                "Deploy app, postgres, redis, and gpu services",
                "Set up CI/CD pipeline with GitHub Actions",
                "Configure monitoring and alerting",
                "Run integration tests against deployed environment",
            ]
        else:
            return [
                "Complete GxP validation protocol",
                "Provision compliant cloud infrastructure",
                "Deploy with audit logging enabled",
                "Configure role-based access control (RBAC)",
                "Execute IQ/OQ/PQ validation suites",
                "Complete regulatory submission documentation",
            ]

    def get_architecture(self) -> list[str]:
        """Return architecture components for the tier."""
        if self.tier == SizingTier.LAB:
            return ["Single-node deployment", "Local SQLite/PostgreSQL", "Docker Compose"]
        elif self.tier == SizingTier.BIOTECH_STARTUP:
            return ["Multi-node K8s", "Managed PostgreSQL", "Redis cache", "GPU node pool"]
        else:
            return [
                "Multi-region K8s",
                "HA PostgreSQL cluster",
                "Redis Sentinel",
                "GPU fleet",
                "Compliance service",
                "Immutable audit log",
            ]

    def to_dict(self) -> dict:
        """Return guide data as a dict."""
        return {
            "tier": self.tier.value,
            "prerequisites": self.get_prerequisites(),
            "steps": self.get_steps(),
            "architecture": self.get_architecture(),
        }

    def to_json(self) -> str:
        """Return guide data as a JSON string."""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict) -> OnboardingGuide:
        """Create an OnboardingGuide from a dict."""
        tier = SizingTier(data["tier"])
        return cls(tier)


def recommend_all_tiers(
    team_size: int,
    monthly_budget: int,
    compute_cores: int,
    storage_tb: float,
) -> list[SizingRecommendation]:
    """Return recommendations for all tiers."""
    if team_size <= 0:
        raise ValueError("team_size must be positive")
    if monthly_budget < 0:
        raise ValueError("monthly_budget must be non-negative")

    tier_order = [SizingTier.LAB, SizingTier.BIOTECH_STARTUP, SizingTier.PHARMA]
    return [
        SizingRecommendation(
            tier=tier,
            recommended_cores=_TIER_PROFILES[tier].cores,
            recommended_storage_tb=_TIER_PROFILES[tier].storage_tb,
            required_services=list(_TIER_PROFILES[tier].services),
            cost=estimate_cost(tier),
            timeline=estimate_timeline(tier, team_size=team_size),
        )
        for tier in tier_order
    ]
