"""Protein Engineering: sequence analysis, structure prediction, and design.

Implements:
- ProteinSequence class with validation
- Molecular weight calculation
- Isoelectric point estimation
- Stability prediction
- Sequence design with target properties
- ProteinStructure class
- Structure prediction (alpha/beta/mixed)
"""

from __future__ import annotations

import random
from dataclasses import dataclass

# Valid amino acids (20 standard)
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# Amino acid molecular weights (Da)
AMINO_ACID_WEIGHTS = {
    "A": 89.1,
    "R": 174.2,
    "N": 132.1,
    "D": 133.1,
    "C": 121.2,
    "E": 147.1,
    "Q": 146.1,
    "G": 75.0,
    "H": 155.2,
    "I": 131.2,
    "L": 131.2,
    "K": 146.2,
    "M": 149.2,
    "F": 165.2,
    "P": 115.1,
    "S": 105.1,
    "T": 119.1,
    "W": 204.2,
    "Y": 181.2,
    "V": 117.1,
}

# Hydrophobic amino acids
HYDROPHOBIC_AA = set("AVILMFWPG")

# Alpha-helix favoring amino acids
ALPHA_FAVORING = set("AELKAMQHR")

# Beta-sheet favoring amino acids
BETA_FAVORING = set("VIFYWTLC")

# Valid structure types
VALID_STRUCTURE_TYPES = {"alpha", "beta", "mixed"}

# Maximum sequence length
MAX_SEQUENCE_LENGTH = 5000


def _validate_sequence(seq: str) -> str:
    """Validate and normalize a protein sequence.

    Args:
        seq: The sequence to validate.

    Returns:
        Uppercase validated sequence.

    Raises:
        TypeError: If input is not a string.
        ValueError: If sequence is empty, too long, or contains invalid characters.
    """
    if not isinstance(seq, str):
        raise TypeError(f"Sequence must be a string, got {type(seq).__name__}")
    if not seq:
        raise ValueError("Sequence cannot be empty")
    if len(seq) > MAX_SEQUENCE_LENGTH:
        raise ValueError(f"Sequence exceeds maximum length of {MAX_SEQUENCE_LENGTH}")
    seq_upper = seq.upper()
    invalid_chars = set(seq_upper) - VALID_AMINO_ACIDS
    if invalid_chars:
        raise ValueError(f"Invalid amino acids: {invalid_chars}")
    return seq_upper


class ProteinSequence:
    """Represents a protein sequence with validation."""

    def __init__(self, sequence: str):
        """Initialize a ProteinSequence.

        Args:
            sequence: Amino acid sequence.

        Raises:
            TypeError: If input is not a string.
            ValueError: If sequence is invalid.
        """
        self._sequence = _validate_sequence(sequence)

    @property
    def sequence(self) -> str:
        """Return the sequence string."""
        return self._sequence

    @property
    def length(self) -> int:
        """Return the sequence length."""
        return len(self._sequence)

    def __str__(self) -> str:
        return self._sequence

    def __repr__(self) -> str:
        return f"ProteinSequence('{self._sequence}')"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProteinSequence):
            return NotImplemented
        return self._sequence == other._sequence

    def __len__(self) -> int:
        return self.length


def calculate_molecular_weight(seq: str) -> float:
    """Calculate molecular weight of a protein sequence.

    Args:
        seq: Amino acid sequence.

    Returns:
        Molecular weight in Daltons.

    Raises:
        TypeError: If input is not a string.
        ValueError: If sequence contains invalid amino acids.
    """
    if not isinstance(seq, str):
        raise TypeError(f"Sequence must be a string, got {type(seq).__name__}")
    if not seq:
        return 0.0
    seq_upper = seq.upper()
    invalid_chars = set(seq_upper) - VALID_AMINO_ACIDS
    if invalid_chars:
        raise ValueError(f"Invalid amino acids: {invalid_chars}")
    return sum(AMINO_ACID_WEIGHTS[aa] for aa in seq_upper)


def calculate_isoelectric_point(seq: str) -> float:
    """Estimate isoelectric point (pI) of a protein sequence.

    Uses a simple heuristic based on the ratio of acidic to basic residues.

    Args:
        seq: Amino acid sequence.

    Returns:
        Estimated pI value.

    Raises:
        TypeError: If input is not a string.
        ValueError: If sequence contains invalid amino acids.
    """
    if not isinstance(seq, str):
        raise TypeError(f"Sequence must be a string, got {type(seq).__name__}")
    if not seq:
        return 7.0
    seq_upper = seq.upper()
    invalid_chars = set(seq_upper) - VALID_AMINO_ACIDS
    if invalid_chars:
        raise ValueError(f"Invalid amino acids: {invalid_chars}")

    acidic = seq_upper.count("D") + seq_upper.count("E")
    basic = seq_upper.count("K") + seq_upper.count("R") + seq_upper.count("H")

    # Simple heuristic: each acidic residue lowers pI, each basic raises it
    pi = 7.0 + (basic - acidic) * 0.5
    return max(3.0, min(12.0, pi))


def predict_stability(seq: str) -> float:
    """Predict protein stability based on hydrophobic ratio.

    Args:
        seq: Amino acid sequence.

    Returns:
        Stability score between 0.0 and 1.0.

    Raises:
        TypeError: If input is not a string.
        ValueError: If sequence contains invalid amino acids.
    """
    if not isinstance(seq, str):
        raise TypeError(f"Sequence must be a string, got {type(seq).__name__}")
    if not seq:
        return 0.0
    seq_upper = seq.upper()
    invalid_chars = set(seq_upper) - VALID_AMINO_ACIDS
    if invalid_chars:
        raise ValueError(f"Invalid amino acids: {invalid_chars}")

    hydrophobic_count = sum(1 for aa in seq_upper if aa in HYDROPHOBIC_AA)
    return hydrophobic_count / len(seq_upper)


def design_sequence(target_length: int, target_hydrophobic_ratio: float) -> str:
    """Design a protein sequence with target properties.

    Args:
        target_length: Desired sequence length.
        target_hydrophobic_ratio: Target ratio of hydrophobic amino acids (0.0-1.0).

    Returns:
        Designed amino acid sequence.

    Raises:
        ValueError: If parameters are invalid.
    """
    if target_length < 0:
        raise ValueError("Target length must be non-negative")
    if not 0.0 <= target_hydrophobic_ratio <= 1.0:
        raise ValueError("Target hydrophobic ratio must be between 0.0 and 1.0")
    if target_length == 0:
        return ""

    hydrophobic = list(HYDROPHOBIC_AA)
    hydrophilic = list(VALID_AMINO_ACIDS - HYDROPHOBIC_AA)

    seq = []
    for _ in range(target_length):
        if random.random() < target_hydrophobic_ratio:
            seq.append(random.choice(hydrophobic))
        else:
            seq.append(random.choice(hydrophilic))
    return "".join(seq)


@dataclass
class ProteinStructure:
    """Represents a protein structure."""

    sequence: str
    structure_type: str

    def __post_init__(self):
        """Validate sequence and structure type."""
        self.sequence = _validate_sequence(self.sequence)
        if self.structure_type not in VALID_STRUCTURE_TYPES:
            raise ValueError(
                f"Invalid structure type: {self.structure_type}. "
                f"Must be one of {VALID_STRUCTURE_TYPES}"
            )

    def to_dict(self) -> dict:
        """Return structure as dictionary."""
        return {
            "sequence": self.sequence,
            "structure_type": self.structure_type,
        }


def predict_structure(seq: str) -> str:
    """Predict protein structure type (alpha/beta/mixed).

    Uses amino acid propensities to predict secondary structure tendency.

    Args:
        seq: Amino acid sequence.

    Returns:
        Predicted structure type: "alpha", "beta", or "mixed".

    Raises:
        TypeError: If input is not a string.
        ValueError: If sequence contains invalid amino acids.
    """
    if not isinstance(seq, str):
        raise TypeError(f"Sequence must be a string, got {type(seq).__name__}")
    if not seq:
        return "mixed"
    seq_upper = seq.upper()
    invalid_chars = set(seq_upper) - VALID_AMINO_ACIDS
    if invalid_chars:
        raise ValueError(f"Invalid amino acids: {invalid_chars}")

    alpha_count = sum(1 for aa in seq_upper if aa in ALPHA_FAVORING)
    beta_count = sum(1 for aa in seq_upper if aa in BETA_FAVORING)

    if alpha_count > beta_count:
        return "alpha"
    elif beta_count > alpha_count:
        return "beta"
    else:
        return "mixed"
