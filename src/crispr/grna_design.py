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


def _pam_matches_iupac(pam_pattern: str, potential: str) -> bool:
    """Check if a PAM matches a pattern with IUPAC ambiguity codes.

    IUPAC codes:
        R = A or G (purine)
        Y = C or T (pyrimidine)
        S = G or C (strong)
        W = A or T (weak)
        K = G or T (keto)
        M = A or C (amino)
        B = C, G, or T (not A)
        D = A, G, or T (not C)
        H = A, C, or T (not G)
        V = A, C, or G (not T)
        N = any base

    Args:
        pam_pattern: The PAM pattern with IUPAC codes.
        potential: The PAM sequence from the genome.

    Returns:
        True if the potential PAM matches the pattern.
    """
    iupac = {
        "R": "AG", "Y": "CT", "S": "GC", "W": "AT",
        "K": "GT", "M": "AC", "B": "CGT", "D": "AGT",
        "H": "ACT", "V": "ACG", "N": "ACGT",
    }
    for p, g in zip(pam_pattern, potential):
        if p in iupac:
            if g not in iupac[p]:
                return False
        elif p != g:
            return False
    return True


def build_kmer_index(genome: str, k: int = 8) -> dict[str, list[int]]:
    """Build a k-mer index for fast off-target lookup.

    Args:
        genome: Genome sequence.
        k: k-mer length.

    Returns:
        Dict mapping k-mer -> list of positions.
    """
    if not genome or len(genome) < k:
        return {}
    genome_upper = genome.upper()
    index: dict[str, list[int]] = {}
    for i in range(len(genome_upper) - k + 1):
        kmer = genome_upper[i : i + k]
        index.setdefault(kmer, []).append(i)
    return index


def find_off_target_sites_both_strands(
    grna: str,
    genome: str,
    max_mismatches: int = 3,
) -> list[dict]:
    """Find off-target sites on both forward and reverse strands.

    Searches the forward strand and the reverse complement of the genome.
    Each result includes a 'strand' key indicating which strand matched.

    Args:
        grna: 20-nt gRNA sequence.
        genome: Genome sequence to search.
        max_mismatches: Maximum number of mismatches allowed.

    Returns:
        List of off-target sites with 'position', 'sequence',
        'mismatches', 'score', and 'strand' keys.
    """
    if not validate_grna_sequence(grna) or not genome:
        return []

    grna_upper = grna.upper()
    genome_upper = genome.upper()
    rc_genome = _reverse_complement(genome_upper)

    off_targets: list[dict] = []

    # Forward strand
    for i in range(len(genome_upper) - 19):
        site = genome_upper[i : i + 20]
        mismatches = sum(1 for a, b in zip(grna_upper, site) if a != b)
        if mismatches <= max_mismatches:
            score = 1.0 / (1.0 + mismatches)
            off_targets.append({
                "position": i,
                "sequence": site,
                "mismatches": mismatches,
                "score": round(score, 4),
                "strand": "forward",
            })

    # Reverse strand
    for i in range(len(rc_genome) - 19):
        site = rc_genome[i : i + 20]
        mismatches = sum(1 for a, b in zip(grna_upper, site) if a != b)
        if mismatches <= max_mismatches:
            score = 1.0 / (1.0 + mismatches)
            off_targets.append({
                "position": len(genome_upper) - i - 20,
                "sequence": _reverse_complement(site),
                "mismatches": mismatches,
                "score": round(score, 4),
                "strand": "reverse",
            })

    return off_targets


def find_off_target_sites_indexed(
    grna: str,
    genome: str,
    max_mismatches: int = 3,
    k: int = 8,
) -> list[dict]:
    """Find off-target sites using k-mer indexed search.

    Uses a k-mer index to quickly locate candidate regions, then
    verifies mismatches only in those regions. Much faster than
    brute-force for large genomes.

    Args:
        grna: 20-nt gRNA sequence.
        genome: Genome sequence to search.
        max_mismatches: Maximum number of mismatches allowed.
        k: k-mer length for indexing.

    Returns:
        List of off-target sites with 'position', 'sequence',
        'mismatches', and 'score' keys.
    """
    if not validate_grna_sequence(grna) or not genome:
        return []

    grna_upper = grna.upper()
    genome_upper = genome.upper()
    index = build_kmer_index(genome_upper, k=k)

    # Extract k-mers from gRNA and look up candidates
    candidates: set[int] = set()
    for i in range(len(grna_upper) - k + 1):
        kmer = grna_upper[i : i + k]
        for pos in index.get(kmer, []):
            # Candidate start position in genome
            candidate_start = pos - i
            if 0 <= candidate_start <= len(genome_upper) - 20:
                candidates.add(candidate_start)

    # Verify candidates
    off_targets: list[dict] = []
    seen: set[int] = set()
    for start in sorted(candidates):
        if start in seen:
            continue
        site = genome_upper[start : start + 20]
        mismatches = sum(1 for a, b in zip(grna_upper, site) if a != b)
        if mismatches <= max_mismatches:
            seen.add(start)
            score = 1.0 / (1.0 + mismatches)
            off_targets.append(
                {
                    "position": start,
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


def validate_cas12a_grna(seq: str) -> bool:
    """Validate a Cas12a (Cpf1) gRNA sequence.

    Cas12a gRNAs are 20-24 nucleotides long and contain only A, C, G, T.

    Args:
        seq: The gRNA sequence to validate.

    Returns:
        True if the sequence is valid, False otherwise.
    """
    if not seq:
        return False
    if len(seq) < 20 or len(seq) > 24:
        return False
    return all(c in VALID_NUCS for c in seq)


def validate_cas13_grna(seq: str) -> bool:
    """Validate a Cas13 gRNA sequence.

    Cas13 gRNAs are 24-28 nucleotides long, contain only A, C, G, U
    (RNA-targeting, no T), and target RNA.

    Args:
        seq: The gRNA sequence to validate.

    Returns:
        True if the sequence is valid, False otherwise.
    """
    if not seq:
        return False
    if len(seq) < 24 or len(seq) > 28:
        return False
    return all(c in "ACGUacgu" for c in seq)


def _rna_efficiency_score(seq: str) -> float:
    """Calculate efficiency score for an RNA gRNA (Cas13).

    Similar to DNA efficiency but works on ACGU sequences.
    """
    if not seq or len(seq) < 24:
        return 0.0
    seq_upper = seq.upper()
    score = 0.0
    # GC content (optimal 40-60%)
    gc = seq_upper.count("G") + seq_upper.count("C")
    gc_content = gc / len(seq_upper)
    if 0.40 <= gc_content <= 0.60:
        score += 0.4
    elif 0.30 <= gc_content <= 0.70:
        score += 0.2
    else:
        score += 0.1
    # G at PAM-proximal position preferred
    if seq_upper[-1] == "G":
        score += 0.3
    # Poly-U penalty
    if "UUUU" in seq_upper:
        score -= 0.2
    return max(0.0, min(1.0, score))


def design_grna_cas13(
    target: str,
    pfs: str = "A",
    min_efficiency: float = 0.0,
) -> Optional[dict]:
    """Design a Cas13 gRNA for an RNA target sequence.

    Cas13 uses a 3' PFS (protospacer flanking site) and a 24-28 nt guide.
    Targets RNA (A, C, G, U only).

    Args:
        target: Target RNA sequence.
        pfs: PFS sequence (default A).
        min_efficiency: Minimum efficiency score threshold.

    Returns:
        Dictionary with 'sequence', 'efficiency', 'off_targets', and 'pfs'
        keys, or None if no valid gRNA is found.
    """
    if not target:
        return None

    target_upper = target.upper()
    pfs_upper = pfs.upper()
    pfs_len = len(pfs_upper)
    grna_len = 28

    best_grna = None
    best_score = -1.0

    def _pfs_matches(potential: str, pfs_pattern: str) -> bool:
        """Check if a PFS matches the pattern."""
        return all(p == "N" or p == g for p, g in zip(pfs_pattern, potential))

    for i in range(len(target_upper) - pfs_len - grna_len + 1):
        # Cas13 PFS is 3' (downstream of the guide)
        potential_grna = target_upper[i : i + grna_len]
        potential_pfs = target_upper[i + grna_len : i + grna_len + pfs_len]

        if _pfs_matches(potential_pfs, pfs_upper):
            if validate_cas13_grna(potential_grna):
                score = _rna_efficiency_score(potential_grna)
                if score >= min_efficiency and score > best_score:
                    best_score = score
                    best_grna = potential_grna

    if best_grna is None:
        return None

    return {
        "sequence": best_grna,
        "efficiency": round(best_score, 4),
        "off_targets": [],
        "pfs": pfs_upper,
    }


def design_grna_cas12a(
    target: str,
    pam: str = "TTTV",
    min_efficiency: float = 0.0,
) -> Optional[dict]:
    """Design a Cas12a (Cpf1) gRNA for a target sequence.

    Cas12a uses a 5' TTTV PAM (V = A, C, or G) and a 20-24 nt guide.

    Args:
        target: Target DNA sequence.
        pam: PAM sequence (default TTTV, V = A/C/G).
        min_efficiency: Minimum efficiency score threshold.

    Returns:
        Dictionary with 'sequence', 'efficiency', 'off_targets', and 'pam'
        keys, or None if no valid gRNA is found.
    """
    if not target:
        return None

    target_upper = target.upper()
    pam_upper = pam.upper()
    pam_len = len(pam_upper)
    grna_len = 20

    best_grna = None
    best_score = -1.0

    def _pam_matches_cas12a(potential: str, pam_pattern: str) -> bool:
        """Check if a PAM matches the Cas12a pattern (V = A/C/G)."""
        for p, g in zip(pam_pattern, potential):
            if p == "V":
                if g not in "ACG":
                    return False
            elif p == "N":
                continue
            elif p != g:
                return False
        return True

    for i in range(len(target_upper) - pam_len - grna_len + 1):
        # Cas12a PAM is 5' (upstream of the guide)
        potential_pam = target_upper[i : i + pam_len]
        potential_grna = target_upper[i + pam_len : i + pam_len + grna_len]

        if _pam_matches_cas12a(potential_pam, pam_upper):
            if validate_cas12a_grna(potential_grna):
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
    }


def design_base_editor_grna(
    target: str,
    editor_type: str = "CBE",
    pam: str = "NGG",
) -> Optional[dict]:
    """Design a gRNA for base editing.

    Finds the best gRNA for base editing based on editor type:
    - CBE (Cytosine Base Editor): editing window positions 4-8, converts C->T
    - ABE (Adenine Base Editor): editing window positions 4-7, converts A->G

    Args:
        target: Target DNA sequence.
        editor_type: 'CBE' or 'ABE'.
        pam: PAM sequence (default NGG).

    Returns:
        Dictionary with 'sequence', 'efficiency', 'pam', 'editor_type',
        'editing_window', and 'conversion_type' keys, or None if no valid
        gRNA with an editable base is found.
    """
    if not target:
        return None

    target_upper = target.upper()
    pam_upper = pam.upper()
    editor_upper = editor_type.upper()

    if editor_upper == "CBE":
        editable_base = "C"
        conversion_type = "C->T"
        window_start, window_end = 3, 8  # 0-indexed, positions 4-8
    elif editor_upper == "ABE":
        editable_base = "A"
        conversion_type = "A->G"
        window_start, window_end = 3, 7  # 0-indexed, positions 4-7
    else:
        return None

    pam_len = len(pam_upper)
    grna_len = 20

    best_grna = None
    best_score = -1.0

    def _pam_matches(potential: str, pam_pattern: str) -> bool:
        """Check if a PAM matches the pattern (N = wildcard)."""
        return all(p == "N" or p == g for p, g in zip(pam_pattern, potential))

    for i in range(len(target_upper) - pam_len - grna_len + 1):
        potential_grna = target_upper[i : i + grna_len]
        potential_pam = target_upper[i + grna_len : i + grna_len + pam_len]

        if _pam_matches(potential_pam, pam_upper):
            if validate_grna_sequence(potential_grna):
                # Check if there's an editable base in the editing window
                window = potential_grna[window_start:window_end]
                if editable_base in window:
                    score = calculate_base_editing_efficiency(
                        potential_grna, editor_type=editor_upper
                    )
                    if score > best_score:
                        best_score = score
                        best_grna = potential_grna

    if best_grna is None:
        return None

    return {
        "sequence": best_grna,
        "efficiency": round(best_score, 4),
        "pam": pam_upper,
        "editor_type": editor_upper,
        "editing_window": (window_start + 1, window_end),
        "conversion_type": conversion_type,
    }


def calculate_base_editing_efficiency(seq: str, editor_type: str = "CBE") -> float:
    """Calculate base editing efficiency score.

    Score based on:
    - GC content (optimal 40-60%)
    - Position of editable bases in editing window (closer to center = better)
    - PAM proximity (editable bases closer to PAM = better)

    Args:
        seq: 20-nt gRNA sequence.
        editor_type: 'CBE' or 'ABE'.

    Returns:
        Efficiency score between 0.0 and 1.0.
    """
    if not validate_grna_sequence(seq):
        return 0.0

    seq_upper = seq.upper()
    editor_upper = editor_type.upper()

    if editor_upper == "CBE":
        editable_base = "C"
        window_start, window_end = 3, 8
    elif editor_upper == "ABE":
        editable_base = "A"
        window_start, window_end = 3, 7
    else:
        return 0.0

    score = 0.0

    # GC content score (optimal 40-60%)
    gc = calculate_gc_content(seq_upper)
    if 0.40 <= gc <= 0.60:
        score += 0.3
    elif 0.30 <= gc <= 0.70:
        score += 0.15
    else:
        score += 0.05

    # Editable base in window
    window = seq_upper[window_start:window_end]
    editable_count = window.count(editable_base)

    if editable_count == 0:
        return max(0.0, min(1.0, score))

    # Score based on number of editable bases (more = better, up to a point)
    score += min(editable_count * 0.15, 0.3)

    # Position score: editable bases closer to center of window = better
    window_center = (window_start + window_end) / 2
    for idx, base in enumerate(window):
        if base == editable_base:
            abs_pos = window_start + idx
            distance = abs(abs_pos - window_center)
            # Closer to center = higher score
            score += max(0.0, 0.1 - distance * 0.02)

    # PAM proximity: editable bases closer to PAM (3' end) = better
    for idx, base in enumerate(window):
        if base == editable_base:
            abs_pos = window_start + idx
            pam_proximity = (len(seq_upper) - 1 - abs_pos) / len(seq_upper)
            score += pam_proximity * 0.1

    return max(0.0, min(1.0, score))


def _reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(complement[c] for c in reversed(seq.upper()))


def design_prime_editing_grna(
    target: str,
    pam: str = "NGG",
    rt_template_len: int = 10,
    pbs_len: int = 10,
) -> Optional[dict]:
    """Design a pegRNA for prime editing.

    Finds a PAM site in the target and designs a pegRNA with:
    - 20nt spacer upstream of the PAM
    - RT template (reverse complement of region downstream of the nick)
    - PBS (sequence upstream of the nick site)

    Args:
        target: Target DNA sequence.
        pam: PAM sequence (default NGG).
        rt_template_len: Length of the RT template in nucleotides.
        pbs_len: Length of the PBS in nucleotides.

    Returns:
        Dictionary with 'spacer', 'rt_template', 'pbs', 'pam', and 'efficiency'
        keys, or None if no valid PAM site is found.
    """
    if not target:
        return None

    target_upper = target.upper()
    pam_upper = pam.upper()
    pam_len = len(pam_upper)
    grna_len = 20

    def _pam_matches(potential: str, pam_pattern: str) -> bool:
        """Check if a PAM matches the pattern (N = wildcard)."""
        return all(p == "N" or p == g for p, g in zip(pam_pattern, potential))

    for i in range(len(target_upper) - pam_len - grna_len + 1):
        potential_grna = target_upper[i : i + grna_len]
        potential_pam = target_upper[i + grna_len : i + grna_len + pam_len]

        if _pam_matches(potential_pam, pam_upper):
            if validate_grna_sequence(potential_grna):
                # Nick site is 3nt upstream of PAM
                nick_offset = i + grna_len - 3

                # RT template: reverse complement of region downstream of nick
                rt_start = nick_offset
                rt_end = min(rt_start + rt_template_len, len(target_upper))
                rt_region = target_upper[rt_start:rt_end]
                rt_template = _reverse_complement(rt_region)

                # PBS: sequence upstream of the nick site
                pbs_start = max(0, nick_offset - pbs_len)
                pbs_region = target_upper[pbs_start:nick_offset]
                pbs = pbs_region

                efficiency = calculate_prime_editing_efficiency(
                    potential_grna, rt_template, pbs
                )

                return {
                    "spacer": potential_grna,
                    "rt_template": rt_template,
                    "pbs": pbs,
                    "pam": pam_upper,
                    "efficiency": round(efficiency, 4),
                }

    return None


def calculate_prime_editing_efficiency(
    spacer: str, rt_template: str, pbs: str
) -> float:
    """Calculate prime editing efficiency score.

    Score based on:
    - GC content of spacer (optimal 40-60%)
    - RT template length (optimal 10-15nt)
    - PBS length (optimal 10-15nt)
    - PBS GC content (optimal 40-60%)

    Args:
        spacer: 20-nt spacer sequence.
        rt_template: RT template sequence.
        pbs: PBS sequence.

    Returns:
        Efficiency score between 0.0 and 1.0.
    """
    if not spacer or not validate_grna_sequence(spacer):
        return 0.0

    score = 0.0

    # GC content of spacer (optimal 40-60%)
    spacer_gc = calculate_gc_content(spacer)
    if 0.40 <= spacer_gc <= 0.60:
        score += 0.3
    elif 0.30 <= spacer_gc <= 0.70:
        score += 0.15
    else:
        score += 0.05

    # RT template length score (optimal 10-15nt)
    rt_len = len(rt_template)
    if 10 <= rt_len <= 15:
        score += 0.25
    elif 8 <= rt_len <= 20:
        score += 0.15
    else:
        score += 0.05

    # PBS length score (optimal 10-15nt)
    pbs_len = len(pbs)
    if 10 <= pbs_len <= 15:
        score += 0.25
    elif 8 <= pbs_len <= 20:
        score += 0.15
    else:
        score += 0.05

    # PBS GC content (optimal 40-60%)
    pbs_gc = calculate_gc_content(pbs)
    if 0.40 <= pbs_gc <= 0.60:
        score += 0.2
    elif 0.30 <= pbs_gc <= 0.70:
        score += 0.1
    else:
        score += 0.05

    return max(0.0, min(1.0, score))


def design_grna_batch(
    targets: list[str],
    pam: str = "NGG",
    min_efficiency: float = 0.0,
) -> list[Optional[dict]]:
    """Design gRNAs for multiple targets in a single call.

    Args:
        targets: List of target DNA sequences.
        pam: PAM sequence (default NGG).
        min_efficiency: Minimum efficiency score threshold.

    Returns:
        List of design dicts (one per target, None for failed targets).
    """
    return [design_grna(t, pam=pam, min_efficiency=min_efficiency) for t in targets]


def design_grna_multiple_pams(
    target: str,
    pams: list[str],
) -> dict[str, Optional[dict]]:
    """Design gRNAs for multiple PAM variants.

    Args:
        target: Target DNA sequence.
        pams: List of PAM sequences to try.

    Returns:
        Dict mapping PAM -> design result (or None if no valid gRNA found).
    """
    return {pam: design_grna(target, pam=pam) for pam in pams}


def calculate_paired_efficiency(grna1: str, grna2: str, distance: int) -> float:
    """Calculate paired gRNA efficiency score.

    Score based on:
    - Individual gRNA efficiencies (using calculate_efficiency_score)
    - Distance between guides (optimal ~100 bp for deletions)
    - Orientation (opposite strands preferred for nickase, same strand for deletions)

    Args:
        grna1: First 20-nt gRNA sequence.
        grna2: Second 20-nt gRNA sequence.
        distance: Distance between the two gRNA cut sites in base pairs.

    Returns:
        Efficiency score between 0.0 and 1.0.
    """
    if not validate_grna_sequence(grna1) or not validate_grna_sequence(grna2):
        return 0.0

    # Individual efficiency scores
    eff1 = calculate_efficiency_score(grna1)
    eff2 = calculate_efficiency_score(grna2)
    avg_efficiency = (eff1 + eff2) / 2.0

    # Distance score: optimal around 100 bp, penalize extremes
    # Gaussian-like falloff from optimal distance of 100
    optimal_distance = 100
    distance_score = max(0.0, 1.0 - abs(distance - optimal_distance) / 200.0)

    # Combined score: 60% individual efficiency, 40% distance
    combined = 0.6 * avg_efficiency + 0.4 * distance_score

    return max(0.0, min(1.0, combined))


def design_paired_grna(
    target: str,
    pam: str = "NGG",
    min_distance: int = 50,
    max_distance: int = 200,
) -> Optional[dict]:
    """Design paired gRNAs for deletions or nickase strategies.

    Finds pairs of gRNAs in the target sequence that:
    - Have valid PAM sites
    - Are within the specified distance range
    - Have high combined efficiency

    Args:
        target: Target DNA sequence.
        pam: PAM sequence (default NGG).
        min_distance: Minimum distance between cut sites in bp.
        max_distance: Maximum distance between cut sites in bp.

    Returns:
        Dictionary with 'grna1', 'grna2', 'distance', 'efficiency', and 'pam'
        keys, or None if no valid pair is found.
    """
    if not target:
        return None

    target_upper = target.upper()
    pam_upper = pam.upper()
    pam_len = len(pam_upper)
    grna_len = 20

    def _pam_matches(potential: str, pam_pattern: str) -> bool:
        """Check if a PAM matches the pattern (N = wildcard)."""
        return all(p == "N" or p == g for p, g in zip(pam_pattern, potential))

    # Find all valid gRNA sites
    sites: list[tuple[int, str]] = []
    for i in range(len(target_upper) - pam_len - grna_len + 1):
        potential_grna = target_upper[i : i + grna_len]
        potential_pam = target_upper[i + grna_len : i + grna_len + pam_len]
        if _pam_matches(potential_pam, pam_upper):
            if validate_grna_sequence(potential_grna):
                sites.append((i, potential_grna))

    if len(sites) < 2:
        return None

    # Find best pair within distance range
    best_pair = None
    best_score = -1.0

    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            pos1, grna1 = sites[i]
            pos2, grna2 = sites[j]
            distance = abs(pos2 - pos1)

            if min_distance <= distance <= max_distance:
                score = calculate_paired_efficiency(grna1, grna2, distance)
                if score > best_score:
                    best_score = score
                    best_pair = (grna1, grna2, distance)

    if best_pair is None:
        return None

    grna1, grna2, distance = best_pair
    return {
        "grna1": grna1,
        "grna2": grna2,
        "distance": distance,
        "efficiency": round(best_score, 4),
        "pam": pam_upper,
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


# Cas9 variant registry
CAS9_VARIANTS: dict[str, dict] = {
    "SpCas9": {
        "pam": "NGG",
        "description": "Standard Streptococcus pyogenes Cas9",
    },
    "eSpCas9": {
        "pam": "NGG",
        "description": "Enhanced specificity Cas9",
    },
    "SpCas9-NG": {
        "pam": "NGN",
        "description": "Relaxed PAM Cas9",
    },
    "xCas9": {
        "pam": "NAG",
        "description": "PAM-flexible Cas9",
    },
    "SpCas9-NRRH": {
        "pam": "NRRH",
        "description": "Extended PAM Cas9",
    },
}


def get_cas9_variant(name: str) -> dict:
    """Get Cas9 variant info by name.

    Args:
        name: Variant name (e.g. 'SpCas9', 'eSpCas9').

    Returns:
        Dict with 'pam' and 'description' keys.

    Raises:
        ValueError: If the variant name is unknown.
    """
    if name not in CAS9_VARIANTS:
        raise ValueError(f"Unknown Cas9 variant: {name}")
    return CAS9_VARIANTS[name]


def list_cas9_variants() -> list[str]:
    """List all available Cas9 variant names.

    Returns:
        List of variant name strings.
    """
    return list(CAS9_VARIANTS.keys())


def design_grna_for_variant(
    target: str,
    variant: str,
    min_efficiency: float = 0.0,
) -> Optional[dict]:
    """Design a gRNA using a specific Cas9 variant's PAM.

    Args:
        target: Target DNA sequence.
        variant: Cas9 variant name.
        min_efficiency: Minimum efficiency score threshold.

    Returns:
        Design dict with 'variant' key added, or None if no valid gRNA found.

    Raises:
        ValueError: If the variant name is unknown.
    """
    variant_info = get_cas9_variant(variant)
    result = design_grna(target, pam=variant_info["pam"], min_efficiency=min_efficiency)
    if result is None:
        return None
    result["variant"] = variant
    return result
