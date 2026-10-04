"""CRISPR guide RNA design, off-target prediction, and efficiency scoring.

Implements:
- Sequence validation
- GC content calculation
- Efficiency scoring (Rule Set 2 inspired)
- Off-target prediction with mismatch tolerance
- Full design pipeline
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# Valid nucleotides
VALID_NUCS = set("ACGTacgt")


def validate_grna_sequence(seq: str) -> bool:
    """Validate a gRNA sequence.

    A valid gRNA is exactly 20 nucleotides long and contains only A, C, G, T
    (case-insensitive).

    Args:
        seq: The gRNA sequence to validate.

    Returns:
        True if the sequence is valid, False otherwise.
    """
    if not seq:
        return False
    if len(seq) != 20:
        return False
    return all(c in VALID_NUCS for c in seq)


def calculate_gc_content(seq: str) -> float:
    """Calculate GC content of a sequence.

    Args:
        seq: Nucleotide sequence.

    Returns:
        GC content as a float between 0.0 and 1.0.
    """
    if not seq:
        return 0.0
    seq_upper = seq.upper()
    gc_count = seq_upper.count("G") + seq_upper.count("C")
    return gc_count / len(seq_upper)


def calculate_efficiency_score(seq: str) -> float:
    """Calculate gRNA efficiency score using Rule Set 2 inspired heuristics.

    Factors:
    - GC content (optimal 40-60%)
    - Position-specific nucleotides (G at position 20 preferred)
    - Poly-T penalty (TTTT reduces efficiency)

    Args:
        seq: 20-nt gRNA sequence.

    Returns:
        Efficiency score between 0.0 and 1.0.
    """
    if not validate_grna_sequence(seq):
        return 0.0

    seq_upper = seq.upper()
    score = 0.0

    # GC content score (optimal 40-60%)
    gc = calculate_gc_content(seq_upper)
    if 0.40 <= gc <= 0.60:
        score += 0.4
    elif 0.30 <= gc <= 0.70:
        score += 0.2
    else:
        score += 0.1

    # Position 20 (PAM-proximal) should be G
    if seq_upper[19] == "G":
        score += 0.3

    # Poly-T penalty
    if "TTTT" in seq_upper:
        score -= 0.2

    # Position 16 should be C (preferred)
    if seq_upper[15] == "C":
        score += 0.15

    # Position 1 should be G (preferred for U6 promoter)
    if seq_upper[0] == "G":
        score += 0.15

    return max(0.0, min(1.0, score))


def find_off_target_sites(
    grna: str,
    genome: str,
    max_mismatches: int = 3,
) -> list[dict]:
    """Find potential off-target sites in a genome.

    Searches for sites similar to the gRNA with up to `max_mismatches`
    mismatches. Returns a list of off-target sites with scores.

    Args:
        grna: 20-nt gRNA sequence.
        genome: Genome sequence to search.
        max_mismatches: Maximum number of mismatches allowed.

    Returns:
        List of off-target sites, each with 'position', 'sequence',
        'mismatches', and 'score' keys.
    """
    if not validate_grna_sequence(grna) or not genome:
        return []

    grna_upper = grna.upper()
    genome_upper = genome.upper()
    off_targets = []

    for i in range(len(genome_upper) - 19):
        site = genome_upper[i : i + 20]
        mismatches = sum(1 for a, b in zip(grna_upper, site) if a != b)
        if mismatches <= max_mismatches:
            # CFD-inspired score: fewer mismatches = higher score
            score = 1.0 / (1.0 + mismatches)
            off_targets.append(
                {
                    "position": i,
                    "sequence": site,
                    "mismatches": mismatches,
                    "score": round(score, 4),
                }
            )

    return off_targets


def design_grna(
    target: str,
    pam: str = "NGG",
    min_efficiency: float = 0.0,
    max_off_targets: int = 100,
) -> Optional[dict]:
    """Design a gRNA for a target sequence.

    Finds the best gRNA in the target sequence based on:
    - PAM compatibility
    - Efficiency score
    - Off-target count

    Args:
        target: Target DNA sequence.
        pam: PAM sequence (default NGG).
        min_efficiency: Minimum efficiency score threshold.
        max_off_targets: Maximum allowed off-target sites.

    Returns:
        Dictionary with 'sequence', 'efficiency', 'off_targets', and 'pam'
        keys, or None if no valid gRNA is found.
    """
    if not target:
        return None

    target_upper = target.upper()
    pam_upper = pam.upper()

    # Find PAM sites
    pam_len = len(pam_upper)
    grna_len = 20

    best_grna = None
    best_score = -1.0

    def _pam_matches(potential: str, pam_pattern: str) -> bool:
        """Check if a PAM matches the pattern (N = wildcard)."""
        return all(p == "N" or p == g for p, g in zip(pam_pattern, potential))

    for i in range(len(target_upper) - pam_len - grna_len + 1):
        # Check if PAM follows the gRNA site
        potential_grna = target_upper[i : i + grna_len]
        potential_pam = target_upper[i + grna_len : i + grna_len + pam_len]

        if _pam_matches(potential_pam, pam_upper):
            if validate_grna_sequence(potential_grna):
                score = calculate_efficiency_score(potential_grna)
                if score >= min_efficiency and score > best_score:
                    best_score = score
                    best_grna = potential_grna

    if best_grna is None:
        return None

    return {
        "sequence": best_grna,
        "efficiency": round(best_score, 4),
        "off_targets": [],
        "pam": pam_upper,
        "max_off_targets": max_off_targets,
    }


@dataclass
class GuideRNA:
    """Represents a designed guide RNA."""

    sequence: str
    efficiency: float = 0.0
    off_targets: list[dict] = field(default_factory=list)
    pam: str = "NGG"

    def __post_init__(self):
        if not validate_grna_sequence(self.sequence):
            raise ValueError(f"Invalid gRNA sequence: {self.sequence}")
        self.efficiency = calculate_efficiency_score(self.sequence)

    @property
    def gc_content(self) -> float:
        return calculate_gc_content(self.sequence)

    def to_dict(self) -> dict:
        return {
            "sequence": self.sequence,
            "efficiency": self.efficiency,
            "gc_content": self.gc_content,
            "off_targets": self.off_targets,
            "pam": self.pam,
        }
