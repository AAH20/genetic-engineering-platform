"""Sizing and onboarding module for tier recommendations.

Provides tiered sizing (lab / biotech_startup / pharma), cost/timeline
estimates, and onboarding guides for each tier.
"""

from __future__ import annotations

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
    """

    tier: SizingTier
    recommended_cores: int
    recommended_storage_tb: float
    required_services: list[str] = field(default_factory=list)


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


def recommend_tier(
    team_size: int,
    monthly_budget: int,
    compute_cores: int,
    storage_tb: float,
) -> SizingRecommendation:
    """Recommend a deployment tier based on team and resource requirements.

    Evaluates tiers in ascending order and returns the highest matching tier.
    """
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
    )


def estimate_cost(tier: SizingTier) -> int:
    """Estimate monthly cost in USD for a given tier."""
    costs = {
        SizingTier.LAB: 500,
        SizingTier.BIOTECH_STARTUP: 25000,
        SizingTier.PHARMA: 200000,
    }
    return costs[tier]


def estimate_timeline(tier: SizingTier) -> int:
    """Estimate onboarding timeline in weeks for a given tier."""
    timelines = {
        SizingTier.LAB: 1,
        SizingTier.BIOTECH_STARTUP: 6,
        SizingTier.PHARMA: 16,
    }
    return timelines[tier]


class OnboardingGuide:
    """Step-by-step onboarding guide for each deployment tier."""

    def __init__(self, tier: SizingTier) -> None:
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
