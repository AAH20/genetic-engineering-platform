"""Protein language model, variant effect prediction, and drug-target interaction.

Implements:
- ProteinLanguageModel: k-mer embedding, variant effect prediction, sequence generation
- VariantEffectPredictor: pathogenicity prediction, conservation scoring
- DrugTargetInteraction: binding affinity and selectivity prediction
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter

import numpy as np

# Standard 20 amino acids
VALID_AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"

# Amino acid property groups for conservation analysis
AA_PROPERTIES = {
    "A": "hydrophobic", "V": "hydrophobic", "I": "hydrophobic", "L": "hydrophobic",
    "M": "hydrophobic", "F": "hydrophobic", "W": "hydrophobic", "Y": "hydrophobic",
    "G": "special", "P": "special", "C": "special",
    "S": "polar", "T": "polar", "N": "polar", "Q": "polar",
    "D": "acidic", "E": "acidic",
    "K": "basic", "R": "basic", "H": "basic",
}

# Grantham distance-inspired similarity matrix (simplified)
# Lower = more similar, higher = more different
GRANTHAM_SIMILARITY = {
    ("A", "G"): 0.5, ("A", "S"): 0.8, ("A", "T"): 0.7,
    ("D", "E"): 0.9, ("D", "N"): 0.6, ("D", "Q"): 0.7,
    ("K", "R"): 0.9, ("K", "Q"): 0.7, ("K", "N"): 0.6,
    ("S", "T"): 0.8, ("S", "N"): 0.6, ("S", "Q"): 0.5,
    ("N", "Q"): 0.8, ("N", "D"): 0.6, ("N", "E"): 0.7,
    ("F", "Y"): 0.9, ("F", "W"): 0.7, ("Y", "W"): 0.8,
    ("I", "L"): 0.9, ("I", "V"): 0.7, ("L", "V"): 0.7,
    ("C", "S"): 0.5, ("C", "A"): 0.6, ("C", "T"): 0.5,
}


def _get_similarity(aa1: str, aa2: str) -> float:
    """Get Grantham-inspired similarity between two amino acids (0-1)."""
    if aa1 == aa2:
        return 1.0
    key = (aa1, aa2) if (aa1, aa2) in GRANTHAM_SIMILARITY else (aa2, aa1)
    if key in GRANTHAM_SIMILARITY:
        return GRANTHAM_SIMILARITY[key]
    # Check property groups
    prop1 = AA_PROPERTIES.get(aa1, "unknown")
    prop2 = AA_PROPERTIES.get(aa2, "unknown")
    if prop1 == prop2:
        return 0.4
    return 0.1


def _kmer_hash(kmer: str, dim: int) -> int:
    """Hash a k-mer to an index in [0, dim)."""
    h = hashlib.md5(kmer.encode(), usedforsecurity=False).hexdigest()  # noqa: S324
    return int(h, 16) % dim


class ProteinLanguageModel:
    """Simple protein language model using k-mer embeddings."""

    def __init__(self, name: str = "default-plm", max_length: int = 1024):
        self.name = name
        self.max_length = max_length
        self.k = 3  # k-mer size
        self.embedding_dim = 256

    def embed(self, sequence: str) -> np.ndarray:
        """Generate a k-mer embedding for a protein sequence.

        Args:
            sequence: Amino acid sequence.

        Returns:
            Numpy array of shape (embedding_dim,).

        Raises:
            ValueError: If sequence is empty or contains invalid amino acids.
        """
        if not sequence:
            raise ValueError("Sequence cannot be empty")

        seq = sequence.upper()
        for aa in seq:
            if aa not in VALID_AMINO_ACIDS:
                raise ValueError(f"Invalid amino acid: {aa}")
        embedding = np.zeros(self.embedding_dim, dtype=np.float64)

        for i in range(len(seq) - self.k + 1):
            kmer = seq[i : i + self.k]
            idx = _kmer_hash(kmer, self.embedding_dim)
            embedding[idx] += 1.0

        # L2 normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        return embedding

    def predict_variant_effect(
        self, wild_type: str, mutant: str, position: int
    ) -> float:
        """Predict the effect of a variant mutation.

        Args:
            wild_type: Wild-type protein sequence.
            mutant: Mutant protein sequence.
            position: Position of the mutation (0-indexed).

        Returns:
            Effect score between 0.0 (no effect) and 1.0 (high effect).

        Raises:
            ValueError: If wild_type or mutant is empty, or position is out of bounds.
        """
        if not wild_type:
            raise ValueError("Wild-type sequence cannot be empty")
        if not mutant:
            raise ValueError("Mutant sequence cannot be empty")
        if position < 0 or position >= len(wild_type):
            raise ValueError(
                f"position {position} is out of bounds for sequence of length {len(wild_type)}"
            )

        wt = wild_type.upper()
        mut = mutant.upper()

        # Get amino acids at the mutation position
        ref_aa = wt[position] if position < len(wt) else "X"
        alt_aa = mut[position] if position < len(mut) else "X"

        if ref_aa == alt_aa:
            return 0.0

        # Base effect from amino acid similarity
        similarity = _get_similarity(ref_aa, alt_aa)
        base_effect = 1.0 - similarity

        # Position weight: mutations near the N-terminus often more disruptive
        position_weight = 1.0
        if len(wt) > 0:
            rel_pos = position / len(wt)
            if rel_pos < 0.1:
                position_weight = 1.2
            elif rel_pos > 0.9:
                position_weight = 1.1

        # Cysteine involvement (disulfide bonds)
        cysteine_factor = 1.0
        if ref_aa == "C" or alt_aa == "C":
            cysteine_factor = 1.3

        # Glycine/Proline in secondary structure
        structure_factor = 1.0
        if alt_aa in ("G", "P"):
            structure_factor = 1.2

        score = base_effect * position_weight * cysteine_factor * structure_factor
        return max(0.0, min(1.0, score))

    def embed_batch(self, sequences: list[str]) -> list[np.ndarray]:
        """Generate embeddings for a batch of protein sequences.

        Args:
            sequences: List of amino acid sequences.

        Returns:
            List of numpy arrays, one per input sequence.
        """
        return [self.embed(seq) for seq in sequences]

    def predict_variant_effect_batch(self, variants: list[dict]) -> list[float]:
        """Predict variant effects for a batch of variants.

        Args:
            variants: List of dicts with keys: wild_type, mutant, position.

        Returns:
            List of effect scores, one per variant.
        """
        return [
            self.predict_variant_effect(v["wild_type"], v["mutant"], v["position"])
            for v in variants
        ]

    def generate_sequence(self, length: int) -> str:
        """Generate a random protein sequence.

        Args:
            length: Desired sequence length.

        Returns:
            Random amino acid sequence.
        """
        actual_length = min(length, self.max_length)
        if actual_length <= 0:
            return ""
        return "".join(random.choices(VALID_AMINO_ACIDS, k=actual_length))


class VariantEffectPredictor:
    """Predict variant pathogenicity and conservation."""

    def __init__(self, model_name: str = "default-vep", threshold: float = 0.5):
        self.model_name = model_name
        self.threshold = threshold

    def predict_pathogenicity(
        self, sequence: str, position: int, ref: str, alt: str
    ) -> float:
        """Predict if a variant is pathogenic.

        Args:
            sequence: Protein sequence.
            position: Position of the variant (0-indexed).
            ref: Reference amino acid.
            alt: Alternate amino acid.

        Returns:
            Pathogenicity score between 0.0 (benign) and 1.0 (pathogenic).

        Raises:
            ValueError: If sequence is empty or position is out of bounds.
        """
        if not sequence:
            raise ValueError("Sequence cannot be empty")
        if position < 0 or position >= len(sequence):
            raise ValueError(
                f"position {position} is out of bounds for sequence of length {len(sequence)}"
            )

        seq = sequence.upper()
        ref = ref.upper()
        alt = alt.upper()

        if ref == alt:
            return 0.0

        # Base pathogenicity from amino acid change severity
        similarity = _get_similarity(ref, alt)
        base_score = 1.0 - similarity

        # Position conservation proxy: check if position is in a conserved region
        # (simplified: positions in the middle of the sequence are more conserved)
        position_factor = 1.0
        if len(seq) > 0:
            rel_pos = position / len(seq)
            if 0.2 < rel_pos < 0.8:
                position_factor = 1.2

        # Cysteine loss is often pathogenic
        cysteine_factor = 1.0
        if ref == "C" and alt != "C":
            cysteine_factor = 1.4
        elif alt == "C" and ref != "C":
            cysteine_factor = 1.2

        # Introduction of proline (helix breaker) or glycine (too flexible)
        structure_factor = 1.0
        if alt == "P":
            structure_factor = 1.3
        elif alt == "G":
            structure_factor = 1.1

        # Introduction of stop codon (represented as '*')
        stop_factor = 1.0
        if alt == "*":
            stop_factor = 2.0

        score = base_score * position_factor * cysteine_factor * structure_factor * stop_factor
        return max(0.0, min(1.0, score))

    def predict_pathogenicity_batch(self, variants: list[dict]) -> list[float]:
        """Predict pathogenicity for a batch of variants.

        Args:
            variants: List of dicts with keys: sequence, position, ref, alt.

        Returns:
            List of pathogenicity scores, one per variant.
        """
        return [
            self.predict_pathogenicity(v["sequence"], v["position"], v["ref"], v["alt"])
            for v in variants
        ]

    def calculate_conservation_score(
        self, sequences: list[str], position: int
    ) -> float:
        """Calculate conservation score at a position across sequences.

        Args:
            sequences: List of aligned protein sequences.
            position: Position to check (0-indexed).

        Returns:
            Conservation score between 0.0 (not conserved) and 1.0 (fully conserved).
        """
        if not sequences:
            return 0.0

        # Get amino acids at the position from all sequences
        aas = []
        for seq in sequences:
            if position < len(seq):
                aas.append(seq[position].upper())

        if not aas:
            return 0.0

        if len(aas) == 1:
            return 1.0

        # Count occurrences of each amino acid
        counts = Counter(aas)
        most_common_count = counts.most_common(1)[0][1]

        # Conservation = fraction of sequences with the most common AA
        conservation = most_common_count / len(aas)

        return conservation


class DrugTargetInteraction:
    """Predict drug-target binding affinity and selectivity."""

    def __init__(self, model_name: str = "default-dti", binding_threshold: float = 0.5):
        self.model_name = model_name
        self.binding_threshold = binding_threshold

    def predict_binding_affinity(
        self, protein_sequence: str, ligand_features: list[float]
    ) -> float:
        """Predict binding affinity between a protein and ligand.

        Args:
            protein_sequence: Target protein sequence.
            ligand_features: List of ligand descriptors.

        Returns:
            Binding affinity score between 0.0 (no binding) and 1.0 (strong binding).
        """
        if not protein_sequence:
            return 0.3

        seq = protein_sequence.upper()

        # Protein features: hydrophobicity, charge, size
        hydrophobic = sum(1 for aa in seq if AA_PROPERTIES.get(aa) == "hydrophobic")
        charged = sum(1 for aa in seq if AA_PROPERTIES.get(aa) in ("acidic", "basic"))
        polar = sum(1 for aa in seq if AA_PROPERTIES.get(aa) == "polar")

        prot_hydro = hydrophobic / len(seq) if seq else 0
        prot_charge = charged / len(seq) if seq else 0
        prot_polar = polar / len(seq) if seq else 0

        # Ligand features (use first 3 as hydrophobicity, charge, size)
        lig_hydro = ligand_features[0] if len(ligand_features) > 0 else 0.5
        lig_charge = ligand_features[1] if len(ligand_features) > 1 else 0.5
        lig_size = ligand_features[2] if len(ligand_features) > 2 else 0.5

        # Complementary interactions
        hydro_match = 1.0 - abs(prot_hydro - lig_hydro)
        charge_match = 1.0 - abs(prot_charge - lig_charge)
        polar_match = 1.0 - abs(prot_polar - 0.5)  # polar ligands prefer polar proteins

        # Size factor: larger ligands need larger binding pockets
        size_factor = min(1.0, len(seq) / 100.0) * lig_size

        score = (hydro_match * 0.3 + charge_match * 0.3 + polar_match * 0.2 + size_factor * 0.2)
        return max(0.0, min(1.0, score))

    def predict_selectivity(
        self, protein_sequence: str, target_family: str
    ) -> float:
        """Predict selectivity of a compound for a target family.

        Args:
            protein_sequence: Target protein sequence.
            target_family: Target family name (e.g., "kinase", "protease").

        Returns:
            Selectivity score between 0.0 (non-selective) and 1.0 (highly selective).
        """
        if not protein_sequence:
            return 0.3

        seq = protein_sequence.upper()
        family = target_family.lower()

        # Family-specific sequence signatures
        family_signatures = {
            "kinase": ["GAGK", "HRD", "DFG", "APE"],
            "protease": ["HDS", "GHS", "CGSC", "TAA"],
            "gpcr": ["DRY", "NPxxY", "CWxP", "PxxF"],
            "ion_channel": ["GYG", "TVGYG", "TTVGYG"],
            "nuclear_receptor": ["LxxLL", "AF-2", "DBD"],
        }

        # Count family-specific motifs
        signatures = family_signatures.get(family, [])
        if not signatures:
            return 0.5

        motif_count = 0
        for motif in signatures:
            # Simple substring search (case-insensitive)
            if motif.upper() in seq:
                motif_count += 1

        # Base selectivity from motif presence
        base_selectivity = motif_count / len(signatures)

        # Sequence length factor: longer sequences have more unique features
        length_factor = min(1.0, len(seq) / 200.0)

        # Hydrophobic binding site density
        hydrophobic = sum(1 for aa in seq if AA_PROPERTIES.get(aa) == "hydrophobic")
        hydro_density = hydrophobic / len(seq) if seq else 0

        score = base_selectivity * 0.5 + length_factor * 0.3 + hydro_density * 0.2
        return max(0.0, min(1.0, score))
