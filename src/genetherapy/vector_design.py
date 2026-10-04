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

import math
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
    "lung": "inhalation",
    "heart": "IV",
    "eye": "intravitreal",
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


def optimize_titer(transgene_size: float, purity: float) -> dict:
    """Find the best vector type for maximum titer.

    Args:
        transgene_size: Size of the transgene in kb.
        purity: Preparation purity as a fraction (0.0 to 1.0).

    Returns:
        Dict with 'best_vector', 'titer', and 'all_titers' keys.

    Raises:
        ValueError: If transgene_size is negative or purity is outside [0, 1].
    """
    if transgene_size < 0:
        raise ValueError("Transgene size must be non-negative")
    if purity < 0.0 or purity > 1.0:
        raise ValueError("Purity must be between 0.0 and 1.0")

    all_titers = {
        vt: calculate_titer(vt, transgene_size, purity)
        for vt in BASE_TITERS
    }
    best_vector = max(all_titers, key=all_titers.get)
    return {
        "best_vector": best_vector,
        "titer": all_titers[best_vector],
        "all_titers": all_titers,
    }


def compare_vector_types(transgene_size: float, purity: float) -> dict:
    """Compare titers across all vector types.

    Args:
        transgene_size: Size of the transgene in kb.
        purity: Preparation purity as a fraction (0.0 to 1.0).

    Returns:
        Dict mapping vector type to titer.
    """
    return {
        vt: calculate_titer(vt, transgene_size, purity)
        for vt in BASE_TITERS
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


# ---------------------------------------------------------------------------
# Capsid stability prediction
# ---------------------------------------------------------------------------
# Serotype stability scores (0-1, higher = more stable capsid)
CAPSID_STABILITY = {
    "AAV2": 0.7,
    "AAV5": 0.6,
    "AAV8": 0.75,
    "AAV9": 0.8,
    "Lentivirus": 0.5,
}


def predict_capsid_stability(serotype: str) -> float:
    """Predict capsid stability score for a given serotype.

    Args:
        serotype: Viral serotype (e.g., AAV2, AAV5, AAV8, AAV9, Lentivirus).

    Returns:
        Stability score between 0.0 and 1.0.
    """
    return CAPSID_STABILITY.get(serotype, 0.5)


# ---------------------------------------------------------------------------
# Capsid antibody binding prediction
# ---------------------------------------------------------------------------
# Base antibody binding probability by serotype (pre-existing immunity)
ANTIBODY_BINDING_BASE = {
    "AAV2": 0.6,
    "AAV5": 0.4,
    "AAV8": 0.35,
    "AAV9": 0.25,
    "Lentivirus": 0.15,
}


def predict_capsid_antibody_binding(serotype: str, patient_age: int) -> float:
    """Predict probability of pre-existing antibody binding for a serotype.

    Args:
        serotype: Viral serotype.
        patient_age: Patient age in years.

    Returns:
        Probability between 0.0 and 1.0 of pre-existing immunity.
    """
    base = ANTIBODY_BINDING_BASE.get(serotype, 0.4)

    # Age factor: older patients have higher chance of prior exposure
    if patient_age < 18:
        age_factor = 0.5 + (patient_age / 18.0) * 0.5
    else:
        age_factor = 1.0

    prob = base * age_factor
    return min(1.0, max(0.0, prob))


# ---------------------------------------------------------------------------
# Immune evasion strategy suggestions
# ---------------------------------------------------------------------------
def suggest_immune_evasion(serotype: str, patient_age: int) -> list[str]:
    """Suggest immune evasion strategies based on serotype and patient age.

    Args:
        serotype: Viral serotype.
        patient_age: Patient age in years.

    Returns:
        List of recommended immune evasion strategies.
    """
    strategies = []

    # Get immunogenicity for this serotype
    immunogenicity = SEROTYPE_IMMUNOGENICITY.get(serotype, 0.5)

    # High immunogenicity serotypes need more aggressive evasion
    if immunogenicity >= 0.5:
        strategies.append("immunosuppression")
        strategies.append("capsid_switch")
        strategies.append("empty_capsid_decoy")
        strategies.append("plasmapheresis")
    elif immunogenicity >= 0.3:
        strategies.append("capsid_switch")
        strategies.append("empty_capsid_decoy")
    else:
        strategies.append("empty_capsid_decoy")

    return strategies


# ---------------------------------------------------------------------------
# MOI and transduction efficiency
# ---------------------------------------------------------------------------
def calculate_moi(vector_dose: float, cell_count: int) -> float:
    """Calculate multiplicity of infection (MOI).

    Args:
        vector_dose: Total vector genomes administered.
        cell_count: Number of target cells.

    Returns:
        MOI = vector_dose / cell_count.

    Raises:
        ValueError: If cell_count is zero.
    """
    if cell_count == 0:
        raise ValueError("Cell count must be non-zero")
    return vector_dose / cell_count


def calculate_transduction_efficiency(moi: float) -> float:
    """Estimate transduction efficiency based on MOI using Poisson distribution.

    P(transduction) = 1 - exp(-MOI)

    Args:
        moi: Multiplicity of infection.

    Returns:
        Transduction efficiency between 0.0 and 1.0.
    """
    return 1.0 - math.exp(-moi)


def calculate_required_volume(titer: float, target_dose: float, cell_count: int) -> float:
    """Calculate required injection volume in mL.

    Args:
        titer: Vector titer in vg/mL.
        target_dose: Desired dose per cell (MOI).
        cell_count: Number of target cells.

    Returns:
        Required volume in mL.

    Raises:
        ValueError: If titer is zero.
    """
    if titer == 0:
        raise ValueError("Titer must be non-zero")
    return target_dose * cell_count / titer


# ---------------------------------------------------------------------------
# Transgene sequence analysis
# ---------------------------------------------------------------------------
def analyze_transgene_sequence(sequence: str) -> dict:
    """Analyze transgene sequence for problematic features.

    Checks for polyA signals, cryptic splice sites, GC content extremes,
    and ORF length.

    Args:
        sequence: DNA sequence to analyze.

    Returns:
        Dict with keys: gc_content, has_polyA, has_cryptic_splice,
        orf_length, warnings.
    """
    seq = sequence.upper()
    length = len(seq)

    # GC content
    gc_count = seq.count("G") + seq.count("C")
    gc_content = gc_count / length if length > 0 else 0.0

    # PolyA signal (canonical: AATAAA)
    has_polya = "AATAAA" in seq

    # Cryptic splice site: GT...AG with at least 10 bp between
    has_cryptic_splice = False
    donor_pos = seq.find("GT")
    while donor_pos != -1:
        acceptor_pos = seq.find("AG", donor_pos + 12)
        if acceptor_pos != -1:
            has_cryptic_splice = True
            break
        donor_pos = seq.find("GT", donor_pos + 1)

    # ORF length: find longest ORF (ATG to stop codon)
    stop_codons = {"TAA", "TAG", "TGA"}
    orf_length = 0
    for frame in range(3):
        i = frame
        while i + 3 <= length:
            codon = seq[i : i + 3]
            if codon == "ATG":
                # Found start, look for stop
                for j in range(i + 3, length - 2, 3):
                    if seq[j : j + 3] in stop_codons:
                        orf_length = max(orf_length, j + 3 - i)
                        break
            i += 3

    # Warnings
    warnings = []
    if gc_content > 0.7:
        warnings.append("High GC content may cause secondary structure issues")
    elif gc_content < 0.3:
        warnings.append("Low GC content may reduce expression efficiency")
    if has_polya:
        warnings.append("PolyA signal detected - may cause premature termination")
    if has_cryptic_splice:
        warnings.append("Cryptic splice site detected - may cause aberrant splicing")

    return {
        "gc_content": gc_content,
        "has_polyA": has_polya,
        "has_cryptic_splice": has_cryptic_splice,
        "orf_length": orf_length,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Immunogenicity risk calculation
# ---------------------------------------------------------------------------
def calculate_immunogenicity_risk(sequence: str, serotype: str) -> float:
    """Estimate immunogenicity risk based on sequence features and serotype.

    Based on CpG content, ORF length, and serotype immunogenicity.

    Args:
        sequence: DNA sequence of the transgene.
        serotype: Viral serotype (e.g., AAV2, AAV9).

    Returns:
        Risk score between 0.0 and 1.0.
    """
    seq = sequence.upper()
    length = len(seq)

    # CpG content using observed/expected ratio
    c_count = seq.count("C")
    g_count = seq.count("G")
    cpg_count = seq.count("CG")

    if c_count > 0 and g_count > 0 and length > 0:
        expected_cpg = (c_count * g_count) / length
        cpg_ratio = cpg_count / expected_cpg if expected_cpg > 0 else 0.0
    else:
        cpg_ratio = 0.0

    # Normalize: ratio of 2.0+ is considered very high
    cpg_factor = min(1.0, cpg_ratio / 2.0)

    # ORF length factor (longer ORFs = more immunogenic potential)
    analysis = analyze_transgene_sequence(seq)
    orf_length = analysis["orf_length"]
    orf_factor = min(1.0, orf_length / 1000.0) if orf_length > 0 else 0.0

    # Serotype immunogenicity (0-1)
    serotype_immuno = SEROTYPE_IMMUNOGENICITY.get(serotype, 0.5)

    # Weighted combination
    risk = (
        0.5 * cpg_factor
        + 0.2 * orf_factor
        + 0.3 * serotype_immuno
    )

    return min(1.0, max(0.0, risk))
