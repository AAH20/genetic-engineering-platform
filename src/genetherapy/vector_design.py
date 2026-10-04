"""Gene Therapy vector design, immune response prediction, and delivery optimization.

Implements:
- Vector dataclass for AAV and lentiviral vectors
- Capacity checking for transgene packaging
- Viral titer estimation
- Immune response prediction based on serotype and patient factors
- Transduction efficiency prediction
- Delivery route optimization
- Dose calculation based on patient weight and target tissue
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Vector dataclass
# ---------------------------------------------------------------------------
@dataclass
class Vector:
    """Represents a viral vector for gene therapy.

    Attributes:
        name: Vector name/identifier.
        capacity: Packaging capacity in kilobases (kb).
        serotype: Viral serotype (e.g., AAV2, AAV9, Lentivirus).
    """

    name: str
    capacity: float
    serotype: str = "AAV2"


# ---------------------------------------------------------------------------
# Capacity checking
# ---------------------------------------------------------------------------
def check_capacity(transgene_size: float, vector_capacity: float) -> bool:
    """Check if a transgene fits within a vector's packaging capacity.

    Args:
        transgene_size: Size of the transgene in kilobases (kb).
        vector_capacity: Packaging capacity of the vector in kb.

    Returns:
        True if the transgene fits, False otherwise.
    """
    if transgene_size < 0:
        return False
    return transgene_size <= vector_capacity


# ---------------------------------------------------------------------------
# Titer calculation
# ---------------------------------------------------------------------------
# Base titers for different vector types (vg/mL)
BASE_TITERS = {
    "AAV": 1e13,
    "Lentivirus": 1e8,
    "Adenovirus": 1e12,
}


def calculate_titer(vector_type: str, transgene_size: float, purity: float) -> float:
    """Estimate viral titer based on vector type, transgene size, and purity.

    Args:
        vector_type: Type of viral vector (AAV, Lentivirus, Adenovirus).
        transgene_size: Size of the transgene in kb.
        purity: Preparation purity as a fraction (0.0 to 1.0).

    Returns:
        Estimated titer in viral genomes per mL (vg/mL).

    Raises:
        ValueError: If vector_type is not recognized.
    """
    if vector_type not in BASE_TITERS:
        raise ValueError(f"Unknown vector type: {vector_type}")

    base = BASE_TITERS[vector_type]
    # Larger transgenes reduce packaging efficiency
    size_factor = max(0.1, 1.0 - (transgene_size / 10.0))
    return base * size_factor * purity


# ---------------------------------------------------------------------------
# Immune response prediction
# ---------------------------------------------------------------------------
# Serotype immunogenicity scores (0-1, higher = more immunogenic)
SEROTYPE_IMMUNOGENICITY = {
    "AAV2": 0.6,
    "AAV5": 0.4,
    "AAV8": 0.35,
    "AAV9": 0.25,
    "Lentivirus": 0.15,
}


def predict_immunogenicity(
    serotype: str, patient_age: int, prior_exposure: bool
) -> float:
    """Predict immune response score based on serotype and patient factors.

    Args:
        serotype: Viral serotype.
        patient_age: Patient age in years.
        prior_exposure: Whether the patient has prior exposure to the serotype.

    Returns:
        Immunogenicity score between 0.0 and 1.0.
    """
    base = SEROTYPE_IMMUNOGENICITY.get(serotype, 0.5)

    # Age factor: younger patients have less developed immune systems
    # but also less prior exposure. Use a curve that peaks around 30-50.
    if patient_age < 18:
        age_factor = 0.7 + (patient_age / 18.0) * 0.3
    else:
        age_factor = 1.0

    # Prior exposure significantly increases immunogenicity
    exposure_factor = 1.5 if prior_exposure else 1.0

    score = base * age_factor * exposure_factor
    return min(1.0, max(0.0, score))


class ImmuneResponsePredictor:
    """Predicts immune response to viral vector gene therapy."""

    def predict_immunogenicity(
        self, serotype: str, patient_age: int, prior_exposure: bool
    ) -> float:
        """Predict immune response score.

        Args:
            serotype: Viral serotype.
            patient_age: Patient age in years.
            prior_exposure: Whether the patient has prior exposure.

        Returns:
            Immunogenicity score between 0.0 and 1.0.
        """
        return predict_immunogenicity(serotype, patient_age, prior_exposure)


# ---------------------------------------------------------------------------
# Transduction efficiency prediction
# ---------------------------------------------------------------------------
# Serotype-tissue transduction efficiency matrix (0-1)
TRANSDUCTION_EFFICIENCY = {
    "AAV2": {"muscle": 0.85, "liver": 0.60, "brain": 0.10, "lung": 0.40, "heart": 0.50},
    "AAV5": {"muscle": 0.70, "liver": 0.75, "brain": 0.30, "lung": 0.60, "heart": 0.55},
    "AAV8": {"muscle": 0.65, "liver": 0.90, "brain": 0.20, "lung": 0.50, "heart": 0.70},
    "AAV9": {"muscle": 0.75, "liver": 0.85, "brain": 0.65, "lung": 0.55, "heart": 0.80},
    "Lentivirus": {"muscle": 0.50, "liver": 0.55, "brain": 0.40, "lung": 0.35, "heart": 0.45},
}


def predict_transduction_efficiency(serotype: str, target_tissue: str) -> float:
    """Predict transduction efficiency for a serotype-tissue pair.

    Args:
        serotype: Viral serotype.
        target_tissue: Target tissue (e.g., liver, muscle, brain).

    Returns:
        Transduction efficiency between 0.0 and 1.0.
    """
    tissue_map = TRANSDUCTION_EFFICIENCY.get(serotype)
    if tissue_map is None:
        return 0.1
    return tissue_map.get(target_tissue, 0.15)


# ---------------------------------------------------------------------------
# Delivery optimization
# ---------------------------------------------------------------------------
# Recommended delivery routes by tissue
TISSUE_DELIVERY_ROUTES = {
    "liver": "IV",
    "muscle": "IM",
    "brain": "IT",
    "lung": "intrathecal",
    "heart": "IV",
    "eye": "subcutaneous",
    "spinal_cord": "IT",
}


def optimize_delivery(target_tissue: str, vector_type: str, patient_age: int) -> str:
    """Select the best delivery route for gene therapy.

    Args:
        target_tissue: Target tissue for gene delivery.
        vector_type: Type of viral vector.
        patient_age: Patient age in years.

    Returns:
        Recommended delivery route (e.g., IV, IM, IT, SC).
    """
    route = TISSUE_DELIVERY_ROUTES.get(target_tissue, "IV")

    # For young patients with brain targeting, prefer intrathecal
    if target_tissue == "brain" and patient_age < 5:
        route = "IT"

    return route


class DeliveryOptimizer:
    """Optimizes delivery route for gene therapy."""

    def optimize_delivery(
        self, target_tissue: str, vector_type: str, patient_age: int
    ) -> str:
        """Select the best delivery route.

        Args:
            target_tissue: Target tissue for gene delivery.
            vector_type: Type of viral vector.
            patient_age: Patient age in years.

        Returns:
            Recommended delivery route.
        """
        return optimize_delivery(target_tissue, vector_type, patient_age)


# ---------------------------------------------------------------------------
# Dose calculation
# ---------------------------------------------------------------------------
# Tissue-specific dose multipliers (vg/kg)
TISSUE_DOSE_MULTIPLIERS = {
    "liver": 2e11,
    "muscle": 1e11,
    "brain": 5e11,
    "lung": 3e11,
    "heart": 2.5e11,
    "eye": 5e10,
    "spinal_cord": 4e11,
}

# Vector-specific dose adjustments
VECTOR_DOSE_FACTORS = {
    "AAV": 1.0,
    "Lentivirus": 0.5,
    "Adenovirus": 2.0,
}


def calculate_dose(patient_weight: float, target_tissue: str, vector_type: str) -> float:
    """Calculate gene therapy dose based on patient weight and target.

    Args:
        patient_weight: Patient weight in kilograms.
        target_tissue: Target tissue for gene delivery.
        vector_type: Type of viral vector.

    Returns:
        Calculated dose in viral genomes (vg).

    Raises:
        ValueError: If patient_weight is zero or negative.
    """
    if patient_weight <= 0:
        raise ValueError("Patient weight must be positive")

    tissue_multiplier = TISSUE_DOSE_MULTIPLIERS.get(target_tissue, 1e11)
    vector_factor = VECTOR_DOSE_FACTORS.get(vector_type, 1.0)

    return patient_weight * tissue_multiplier * vector_factor
