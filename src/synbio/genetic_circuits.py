"""Genetic circuits, pathway optimization, and DNA synthesis design."""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# LogicGate
# ---------------------------------------------------------------------------

VALID_GATE_TYPES = {"AND", "OR", "NOT", "NOR"}


class LogicGate:
    """A single logic gate in a genetic circuit."""

    def __init__(self, gate_type: str, inputs: list[str], output: str) -> None:
        if gate_type not in VALID_GATE_TYPES:
            raise ValueError(f"Unsupported gate type: {gate_type}")
        self.gate_type = gate_type
        self.inputs = list(inputs)
        self.output = output

    def evaluate(self, input_values: dict[str, bool]) -> bool:
        """Evaluate the gate given input values."""
        vals = [input_values[name] for name in self.inputs]
        if self.gate_type == "AND":
            return all(vals)
        elif self.gate_type == "OR":
            return any(vals)
        elif self.gate_type == "NOT":
            return not vals[0]
        elif self.gate_type == "NOR":
            return not any(vals)
        raise ValueError(f"Unsupported gate type: {self.gate_type}")


# ---------------------------------------------------------------------------
# GeneticCircuit
# ---------------------------------------------------------------------------


class GeneticCircuit:
    """A genetic circuit composed of logic gates."""

    def __init__(self, name: str, inputs: list[str], outputs: list[str]) -> None:
        self.name = name
        self.inputs = list(inputs)
        self.outputs = list(outputs)
        self.gates: list[LogicGate] = []

    def add_gate(self, gate_type: str, inputs: list[str], output: str) -> None:
        """Add a logic gate to the circuit."""
        if gate_type not in VALID_GATE_TYPES:
            raise ValueError(f"Unsupported gate type: {gate_type}")
        if gate_type == "AND" and len(inputs) != 2:
            raise ValueError("AND gate requires 2 inputs")
        if gate_type == "OR" and len(inputs) != 2:
            raise ValueError("OR gate requires 2 inputs")
        if gate_type == "NOR" and len(inputs) != 2:
            raise ValueError("NOR gate requires 2 inputs")
        if gate_type == "NOT" and len(inputs) != 1:
            raise ValueError("NOT gate requires 1 input")
        self.gates.append(LogicGate(gate_type, inputs, output))

    def evaluate(self, input_values: dict[str, bool]) -> dict[str, bool]:
        """Evaluate the circuit for given input values."""
        # Check all circuit inputs are provided
        for name in self.inputs:
            if name not in input_values:
                raise ValueError(f"Missing input: {name}")

        # Evaluate gates in order, building up signal values
        signals: dict[str, bool] = dict(input_values)
        for gate in self.gates:
            # Check gate inputs are available
            for inp in gate.inputs:
                if inp not in signals:
                    raise ValueError(f"Missing input: {inp}")
            signals[gate.output] = gate.evaluate(signals)

        # Return only declared outputs
        return {out: signals[out] for out in self.outputs}

    def validate(self) -> bool:
        """Check that the circuit is well-formed."""
        if not self.gates:
            return False

        # Track available signals: declared inputs + gate outputs
        available = set(self.inputs)
        produced_outputs = set()

        for gate in self.gates:
            # All gate inputs must be available
            for inp in gate.inputs:
                if inp not in available:
                    return False
            available.add(gate.output)
            produced_outputs.add(gate.output)

        # At least one gate must produce a declared output
        if not produced_outputs.intersection(set(self.outputs)):
            return False

        return True


# ---------------------------------------------------------------------------
# PathwayOptimizer
# ---------------------------------------------------------------------------


class PathwayOptimizer:
    """Flux-based pathway optimization."""

    def optimize_pathway(self, pathway: dict[str, Any]) -> dict[str, Any]:
        """Optimize fluxes in a metabolic pathway."""
        reactions = pathway.get("reactions", [])
        target = pathway.get("target")

        if not reactions:
            raise ValueError("Empty pathway")
        if target is None:
            raise ValueError("Pathway must specify a target")

        # Simple flux optimization: find the bottleneck flux
        # and scale all fluxes to maximize target production
        fluxes = [r["flux"] for r in reactions]
        min_flux = min(fluxes)

        # Optimal fluxes: scale to bottleneck
        optimal_fluxes = {}
        for r in reactions:
            optimal_fluxes[r["id"]] = min_flux

        # Max yield is limited by the bottleneck
        max_yield = min_flux

        return {
            "optimal_fluxes": optimal_fluxes,
            "max_yield": max_yield,
        }

    def calculate_yield(
        self,
        stoichiometry: dict[str, int],
        substrate: str,
        product: str,
        efficiency: float = 1.0,
    ) -> float:
        """Calculate theoretical yield from substrate to product."""
        if substrate not in stoichiometry or stoichiometry[substrate] == 0:
            raise ValueError(f"Invalid stoichiometry for substrate: {substrate}")
        if product not in stoichiometry:
            raise ValueError(f"Invalid stoichiometry for product: {product}")

        # Yield = (product moles / substrate moles) * efficiency
        yield_value = (stoichiometry[product] / stoichiometry[substrate]) * efficiency
        return yield_value


# ---------------------------------------------------------------------------
# DNASynthesis
# ---------------------------------------------------------------------------


class DNASynthesis:
    """DNA synthesis design and cost estimation."""

    # Standard Golden Gate overhang set (4-nt, unique, balanced GC)
    STANDARD_OVERHANGS = [
        "AACA", "AACC", "AACG", "AACT", "AAGC", "AAGT", "AATC", "AATT",
        "ACAA", "ACAC", "ACAG", "ACAT", "ACCA", "ACCC", "ACCG", "ACCT",
        "ACGA", "ACGC", "ACGG", "ACGT", "ACTA", "ACTC", "ACTG", "ACTT",
        "AGAA", "AGAC", "AGAG", "AGAT", "AGCA", "AGCC", "AGCG", "AGCT",
        "AGGA", "AGGC", "AGGG", "AGGT", "AGTA", "AGTC", "AGTG", "AGTT",
        "ATAA", "ATAC", "ATAG", "ATAT", "ATCA", "ATCC", "ATCG", "ATCT",
        "ATGA", "ATGC", "ATGG", "ATGT", "ATTA", "ATTC", "ATTG", "ATTT",
        "CAAA", "CAAC", "CAAG", "CAAT", "CACA", "CACC", "CACG", "CACT",
        "CAGA", "CAGC", "CAGG", "CAGT", "CATA", "CATC", "CATG", "CATT",
        "CCAA", "CCAC", "CCAG", "CCAT", "CCCA", "CCCC", "CCCG", "CCCT",
        "CCGA", "CCGC", "CCGG", "CCGT", "CCTA", "CCTC", "CCTG", "CCTT",
        "CGAA", "CGAC", "CGAG", "CGAT", "CGCA", "CGCC", "CGCG", "CGCT",
        "CGGA", "CGGC", "CGGG", "CGGT", "CGTA", "CGTC", "CGTG", "CGTT",
        "CTAA", "CTAC", "CTAG", "CTAT", "CTCA", "CTCC", "CTCG", "CTCT",
        "CTGA", "CTGC", "CTGG", "CTGT", "CTTA", "CTTC", "CTTG", "CTTT",
        "GAAA", "GAAC", "GAAG", "GAAT", "GACA", "GACC", "GACG", "GACT",
        "GAGA", "GAGC", "GAGG", "GAGT", "GATA", "GATC", "GATG", "GATT",
        "GCAA", "GCAC", "GCAG", "GCAT", "GCCA", "GCCC", "GCCG", "GCCT",
        "GCGA", "GCGC", "GCGG", "GCGT", "GCTA", "GCTC", "GCTG", "GCTT",
        "GGAA", "GGAC", "GGAG", "GGAT", "GGCA", "GGCC", "GGCG", "GGCT",
        "GGGA", "GGGC", "GGGG", "GGGT", "GGTA", "GGTC", "GGTG", "GGTT",
        "GTAA", "GTAC", "GTAG", "GTAT", "GTCA", "GTCC", "GTCG", "GTCT",
        "GTGA", "GTGC", "GTGG", "GTGT", "GTTA", "GTTC", "GTTG", "GTTT",
        "TAAA", "TAAC", "TAAG", "TAAT", "TACA", "TACC", "TACG", "TACT",
        "TAGA", "TAGC", "TAGG", "TAGT", "TATA", "TATC", "TATG", "TATT",
        "TCAA", "TCAC", "TCAG", "TCAT", "TCCA", "TCCC", "TCCG", "TCCT",
        "TCGA", "TCGC", "TCGG", "TCGT", "TCTA", "TCTC", "TCTG", "TCTT",
        "TGAA", "TGAC", "TGAG", "TGAT", "TGCA", "TGCC", "TGCG", "TGCT",
        "TGGA", "TGGC", "TGGG", "TGGT", "TGTA", "TGTC", "TGTG", "TGTT",
        "TTAA", "TTAC", "TTAG", "TTAT", "TTCA", "TTCC", "TTCG", "TTCT",
        "TTGA", "TTGC", "TTGG", "TTGT", "TTTA", "TTTC", "TTTG", "TTTT",
    ]

    def design_overhangs(self, parts: list[str]) -> list[str]:
        """Design Golden Gate overhangs for a list of parts."""
        if not parts:
            return []

        # Use a deterministic selection from standard overhangs
        # Filter for balanced GC content (25%-75%)
        valid_overhangs = []
        for oh in self.STANDARD_OVERHANGS:
            gc = (oh.count("G") + oh.count("C")) / len(oh)
            if 0.25 <= gc <= 0.75:
                valid_overhangs.append(oh)

        # Select unique overhangs
        selected = []
        used = set()
        idx = 0
        for _ in parts:
            oh = valid_overhangs[idx % len(valid_overhangs)]
            while oh in used:
                idx += 1
                oh = valid_overhangs[idx % len(valid_overhangs)]
            selected.append(oh)
            used.add(oh)
            idx += 1

        return selected

    def calculate_synthesis_cost(self, sequence: str) -> float:
        """Estimate DNA synthesis cost for a sequence."""
        if not sequence:
            return 0.0

        length = len(sequence)
        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        gc_content = gc_count / length if length > 0 else 0.0

        # Base cost: $0.15 per bp
        base_cost = length * 0.15

        # GC content factor: high GC costs more
        gc_factor = 1.0 + (gc_content - 0.5) * 0.4

        return base_cost * gc_factor


# ---------------------------------------------------------------------------
# RBS Calculator & Designer
# ---------------------------------------------------------------------------

# Anti-Shine-Dalgarno sequence on 16S rRNA (3'->5' direction)
ANTI_SD = "AUUCCUCCACUAG"

# Host-specific RBS motifs
HOST_RBS_MOTIFS = {
    "E.coli": "AGGAGG",
    "B.subtilis": "AGGAGGU",
    "S.cerevisiae": "AAAAAA",
}


def calculate_rbs_strength(sequence: str, start_position: int = 0) -> float:
    """Calculate ribosome binding site strength (0-1).

    Based on complementarity to 16S rRNA anti-Shine-Dalgarno sequence,
    spacing from start codon, and AU content.
    """
    if not sequence:
        return 0.0

    seq = sequence.upper().replace("U", "T")

    # When start_position is 0, evaluate the entire sequence as the RBS
    if start_position == 0:
        window = seq
        spacing_score = 1.0  # No spacing penalty when no start codon context
    else:
        # Extract window around start_position (15 nt upstream to 5 nt downstream)
        window_start = max(0, start_position - 15)
        window_end = min(len(seq), start_position + 5)
        window = seq[window_start:window_end]

        if not window:
            return 0.0

        # Spacing score: optimal spacing is 5-13 nt upstream of start codon
        # Find position of best SD match
        sd_motif = "AGGAGG"
        best_sd_pos = 0
        best_complementarity_for_spacing = 0.0
        for i in range(len(window) - len(sd_motif) + 1):
            subseq = window[i:i + len(sd_motif)]
            matches = sum(1 for a, b in zip(subseq, sd_motif) if a == b)
            if matches / len(sd_motif) > best_complementarity_for_spacing:
                best_complementarity_for_spacing = matches / len(sd_motif)
                best_sd_pos = i

        # Distance from start codon (start_position is the start codon position)
        sd_end = window_start + best_sd_pos + len(sd_motif)
        spacing = start_position - sd_end
        if 5 <= spacing <= 13:
            spacing_score = 1.0
        elif spacing < 5:
            spacing_score = max(0.0, 1.0 - (5 - spacing) * 0.2)
        else:
            spacing_score = max(0.0, 1.0 - (spacing - 13) * 0.1)

    # Complementarity score: check for SD-like motifs
    sd_motif = "AGGAGG"
    best_complementarity = 0.0
    for i in range(len(window) - len(sd_motif) + 1):
        subseq = window[i:i + len(sd_motif)]
        matches = sum(1 for a, b in zip(subseq, sd_motif) if a == b)
        complementarity = matches / len(sd_motif)
        best_complementarity = max(best_complementarity, complementarity)

    # AU content score: higher AU content generally increases RBS strength
    au_count = window.count("A") + window.count("T")
    au_content = au_count / len(window) if window else 0.0
    au_score = au_content  # 0-1 range

    # Weighted combination
    strength = (
        0.5 * best_complementarity
        + 0.3 * spacing_score
        + 0.2 * au_score
    )

    return max(0.0, min(1.0, strength))


def design_rbs(target_protein_seq: str, host: str = "E.coli") -> str:
    """Design an RBS sequence for the given protein and host.

    Returns 5' UTR sequence with RBS.
    Host-specific: 'E.coli', 'B.subtilis', 'S.cerevisiae'.
    """
    if host not in HOST_RBS_MOTIFS:
        raise ValueError(f"Unsupported host: {host}")

    motif = HOST_RBS_MOTIFS[host]

    # Spacer sequence between RBS and start codon
    if host == "E.coli":
        spacer = "TAATAC"  # Optimal spacing for E.coli
    elif host == "B.subtilis":
        spacer = "AATTCG"  # Different spacing for B.subtilis
    else:
        spacer = "GCTAGC"  # Different spacing for S.cerevisiae

    # Upstream sequence
    if host == "E.coli":
        upstream = "TTAAAG"
    elif host == "B.subtilis":
        upstream = "CGCGAT"
    else:
        upstream = "TATATA"

    # Construct 5' UTR: upstream + RBS motif + spacer
    utr = upstream + motif + spacer

    return utr


# ---------------------------------------------------------------------------
# MoClo Assembly Overhang Design
# ---------------------------------------------------------------------------

def _reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    return seq[::-1].translate(str.maketrans("ATGC", "TACG"))


def _gc_content(seq: str) -> float:
    """Calculate GC content of a DNA sequence."""
    if not seq:
        return 0.0
    return (seq.count("G") + seq.count("C")) / len(seq)


def _is_palindrome(seq: str) -> bool:
    """Check if a DNA sequence is a palindrome (equals its reverse complement)."""
    return seq == _reverse_complement(seq)


def design_moclo_overhangs(parts: list[str]) -> dict[str, str]:
    """Assign unique 4-bp overhangs to each part for MoClo assembly.

    Overhangs are 4bp, GC content 40-60%, no palindromes, no reverse complement pairs.
    Returns dict mapping part index (as string) to overhang sequence.
    """
    if not parts:
        return {}

    from itertools import product

    # Generate all 4-bp sequences with exactly 2 G/C bases (50% GC content)
    valid_overhangs = []
    for seq_tuple in product("ATGC", repeat=4):
        seq = "".join(seq_tuple)
        gc_count = seq.count("G") + seq.count("C")
        if gc_count != 2:  # Must be exactly 50% GC (2 out of 4)
            continue
        if _is_palindrome(seq):
            continue
        valid_overhangs.append(seq)

    # Greedily select overhangs that don't form reverse complement pairs
    selected = []
    used = set()
    for oh in valid_overhangs:
        if len(selected) >= len(parts):
            break
        rc = _reverse_complement(oh)
        if oh not in used and rc not in used:
            selected.append(oh)
            used.add(oh)
            used.add(rc)

    # Map part indices to overhangs
    return {str(i): selected[i] for i in range(len(parts))}


def validate_moclo_design(overhangs: dict[str, str]) -> dict:
    """Validate MoClo overhang design.

    Checks: all overhangs unique, no palindromes, no reverse complement pairs, GC content valid.
    Returns dict with 'valid': bool, 'errors': list[str].
    """
    errors = []

    if not overhangs:
        return {"valid": True, "errors": []}

    # Check all overhangs are 4bp
    for key, oh in overhangs.items():
        if len(oh) != 4:
            errors.append(f"Overhang {key} ({oh}) is not 4bp")

    # Check GC content 40-60%
    for key, oh in overhangs.items():
        gc = _gc_content(oh)
        if gc < 0.4 or gc > 0.6:
            errors.append(f"Overhang {key} ({oh}) has invalid GC content: {gc:.1%}")

    # Check uniqueness
    seen = {}
    for key, oh in overhangs.items():
        if oh in seen:
            errors.append(f"Duplicate overhang {oh} at positions {seen[oh]} and {key}")
        else:
            seen[oh] = key

    # Check no palindromes
    for key, oh in overhangs.items():
        if _is_palindrome(oh):
            errors.append(f"Overhang {key} ({oh}) is a palindrome")

    # Check no reverse complement pairs
    items = list(overhangs.items())
    for i, (key1, oh1) in enumerate(items):
        for key2, oh2 in items[i + 1:]:
            if oh1 == _reverse_complement(oh2):
                errors.append(
                    f"Overhangs {key1} ({oh1}) and {key2} ({oh2}) are reverse complements"
                )

    return {"valid": len(errors) == 0, "errors": errors}


# ---------------------------------------------------------------------------
# Codon Optimization & CAI
# ---------------------------------------------------------------------------

# Standard genetic code: amino acid -> list of codons
GENETIC_CODE: dict[str, list[str]] = {
    "A": ["GCT", "GCC", "GCA", "GCG"],
    "R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "N": ["AAT", "AAC"],
    "D": ["GAT", "GAC"],
    "C": ["TGT", "TGC"],
    "Q": ["CAA", "CAG"],
    "E": ["GAA", "GAG"],
    "G": ["GGT", "GGC", "GGA", "GGG"],
    "H": ["CAT", "CAC"],
    "I": ["ATT", "ATC", "ATA"],
    "L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
    "K": ["AAA", "AAG"],
    "M": ["ATG"],
    "F": ["TTT", "TTC"],
    "P": ["CCT", "CCC", "CCA", "CCG"],
    "S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
    "T": ["ACT", "ACC", "ACA", "ACG"],
    "W": ["TGG"],
    "Y": ["TAT", "TAC"],
    "V": ["GTT", "GTC", "GTA", "GTG"],
    "*": ["TAA", "TAG", "TGA"],
}

# Reverse mapping: codon -> amino acid
CODON_TO_AA: dict[str, str] = {
    codon: aa for aa, codons in GENETIC_CODE.items() for codon in codons
}

# Host-specific codon usage tables: host -> {codon: relative_adaptiveness (0-1)}
# Relative adaptiveness = frequency of codon / frequency of most frequent synonymous codon
CODON_USAGE_TABLES: dict[str, dict[str, float]] = {
    "E.coli": {
        # Ala
        "GCT": 0.35, "GCC": 0.25, "GCA": 0.20, "GCG": 0.20,
        # Arg
        "CGT": 0.40, "CGC": 0.35, "CGA": 0.05, "CGG": 0.05, "AGA": 0.10, "AGG": 0.05,
        # Asn
        "AAT": 0.30, "AAC": 0.70,
        # Asp
        "GAT": 0.40, "GAC": 0.60,
        # Cys
        "TGT": 0.35, "TGC": 0.65,
        # Gln
        "CAA": 0.30, "CAG": 0.70,
        # Glu
        "GAA": 0.70, "GAG": 0.30,
        # Gly
        "GGT": 0.40, "GGC": 0.40, "GGA": 0.05, "GGG": 0.15,
        # His
        "CAT": 0.30, "CAC": 0.70,
        # Ile
        "ATT": 0.50, "ATC": 0.45, "ATA": 0.05,
        # Leu
        "TTA": 0.05, "TTG": 0.10, "CTT": 0.10, "CTC": 0.10, "CTA": 0.05, "CTG": 0.60,
        # Lys
        "AAA": 0.75, "AAG": 0.25,
        # Met
        "ATG": 1.00,
        # Phe
        "TTT": 0.60, "TTC": 0.40,
        # Pro
        "CCT": 0.15, "CCC": 0.10, "CCA": 0.15, "CCG": 0.60,
        # Ser
        "TCT": 0.15, "TCC": 0.15, "TCA": 0.10, "TCG": 0.10, "AGT": 0.15, "AGC": 0.35,
        # Thr
        "ACT": 0.20, "ACC": 0.50, "ACA": 0.10, "ACG": 0.20,
        # Trp
        "TGG": 1.00,
        # Tyr
        "TAT": 0.40, "TAC": 0.60,
        # Val
        "GTT": 0.30, "GTC": 0.20, "GTA": 0.20, "GTG": 0.30,
        # Stop
        "TAA": 0.60, "TAG": 0.10, "TGA": 0.30,
    },
    "S.cerevisiae": {
        # Ala
        "GCT": 0.40, "GCC": 0.20, "GCA": 0.25, "GCG": 0.15,
        # Arg
        "CGT": 0.15, "CGC": 0.05, "CGA": 0.05, "CGG": 0.05, "AGA": 0.45, "AGG": 0.25,
        # Asn
        "AAT": 0.30, "AAC": 0.70,
        # Asp
        "GAT": 0.60, "GAC": 0.40,
        # Cys
        "TGT": 0.60, "TGC": 0.40,
        # Gln
        "CAA": 0.70, "CAG": 0.30,
        # Glu
        "GAA": 0.75, "GAG": 0.25,
        # Gly
        "GGT": 0.50, "GGC": 0.20, "GGA": 0.10, "GGG": 0.20,
        # His
        "CAT": 0.40, "CAC": 0.60,
        # Ile
        "ATT": 0.50, "ATC": 0.30, "ATA": 0.20,
        # Leu
        "TTA": 0.20, "TTG": 0.20, "CTT": 0.10, "CTC": 0.05, "CTA": 0.10, "CTG": 0.35,
        # Lys
        "AAA": 0.60, "AAG": 0.40,
        # Met
        "ATG": 1.00,
        # Phe
        "TTT": 0.40, "TTC": 0.60,
        # Pro
        "CCT": 0.30, "CCC": 0.15, "CCA": 0.40, "CCG": 0.15,
        # Ser
        "TCT": 0.20, "TCC": 0.15, "TCA": 0.15, "TCG": 0.10, "AGT": 0.10, "AGC": 0.30,
        # Thr
        "ACT": 0.35, "ACC": 0.25, "ACA": 0.20, "ACG": 0.20,
        # Trp
        "TGG": 1.00,
        # Tyr
        "TAT": 0.35, "TAC": 0.65,
        # Val
        "GTT": 0.35, "GTC": 0.25, "GTA": 0.15, "GTG": 0.25,
        # Stop
        "TAA": 0.50, "TAG": 0.20, "TGA": 0.30,
    },
    "B.subtilis": {
        # Ala
        "GCT": 0.30, "GCC": 0.20, "GCA": 0.30, "GCG": 0.20,
        # Arg
        "CGT": 0.35, "CGC": 0.25, "CGA": 0.10, "CGG": 0.10, "AGA": 0.15, "AGG": 0.05,
        # Asn
        "AAT": 0.50, "AAC": 0.50,
        # Asp
        "GAT": 0.55, "GAC": 0.45,
        # Cys
        "TGT": 0.40, "TGC": 0.60,
        # Gln
        "CAA": 0.45, "CAG": 0.55,
        # Glu
        "GAA": 0.65, "GAG": 0.35,
        # Gly
        "GGT": 0.35, "GGC": 0.30, "GGA": 0.20, "GGG": 0.15,
        # His
        "CAT": 0.45, "CAC": 0.55,
        # Ile
        "ATT": 0.55, "ATC": 0.35, "ATA": 0.10,
        # Leu
        "TTA": 0.10, "TTG": 0.15, "CTT": 0.15, "CTC": 0.15, "CTA": 0.10, "CTG": 0.35,
        # Lys
        "AAA": 0.70, "AAG": 0.30,
        # Met
        "ATG": 1.00,
        # Phe
        "TTT": 0.55, "TTC": 0.45,
        # Pro
        "CCT": 0.25, "CCC": 0.15, "CCA": 0.30, "CCG": 0.30,
        # Ser
        "TCT": 0.20, "TCC": 0.20, "TCA": 0.15, "TCG": 0.15, "AGT": 0.10, "AGC": 0.20,
        # Thr
        "ACT": 0.30, "ACC": 0.35, "ACA": 0.15, "ACG": 0.20,
        # Trp
        "TGG": 1.00,
        # Tyr
        "TAT": 0.50, "TAC": 0.50,
        # Val
        "GTT": 0.30, "GTC": 0.25, "GTA": 0.20, "GTG": 0.25,
        # Stop
        "TAA": 0.55, "TAG": 0.15, "TGA": 0.30,
    },
}


def optimize_codon_usage(protein_seq: str, host: str = "E.coli") -> str:
    """Optimize codon usage for expression in a given host.

    Returns DNA sequence encoding the protein using the most frequent
    synonymous codon for each amino acid in the specified host.

    Supported hosts: 'E.coli', 'S.cerevisiae', 'B.subtilis'.
    """
    if host not in CODON_USAGE_TABLES:
        raise ValueError(f"Unsupported host: {host}")

    usage_table = CODON_USAGE_TABLES[host]
    dna = []

    for aa in protein_seq.upper():
        if aa not in GENETIC_CODE:
            raise ValueError(f"Unknown amino acid: {aa}")

        codons = GENETIC_CODE[aa]
        # Pick the codon with highest relative adaptiveness
        best_codon = max(codons, key=lambda c: usage_table.get(c, 0.0))
        dna.append(best_codon)

    return "".join(dna)


def calculate_cai(dna_seq: str, host: str = "E.coli") -> float:
    """Calculate Codon Adaptation Index (CAI) for a DNA sequence.

    CAI ranges from 0 to 1, where higher values indicate better adaptation
    to the host's codon usage preferences.

    Supported hosts: 'E.coli', 'S.cerevisiae', 'B.subtilis'.
    """
    if host not in CODON_USAGE_TABLES:
        raise ValueError(f"Unsupported host: {host}")

    if not dna_seq:
        return 0.0

    usage_table = CODON_USAGE_TABLES[host]
    seq = dna_seq.upper()

    # Extract codons (skip incomplete trailing codon)
    codons = [seq[i:i + 3] for i in range(0, len(seq) - 2, 3)]

    if not codons:
        return 0.0

    # Calculate relative adaptiveness for each codon
    # w_i = observed frequency of codon / max frequency among synonymous codons
    # For our pre-computed tables, the values are already relative adaptiveness
    weights = []
    for codon in codons:
        if codon in CODON_TO_AA:
            aa = CODON_TO_AA[codon]
            # Get all synonymous codons for this amino acid
            synonymous = GENETIC_CODE[aa]
            # Get the max relative adaptiveness among synonymous codons
            max_w = max(usage_table.get(c, 0.0) for c in synonymous)
            if max_w > 0:
                w = usage_table.get(codon, 0.0) / max_w
            else:
                w = 0.0
            weights.append(w)

    if not weights:
        return 0.0

    # CAI = geometric mean of relative adaptiveness values
    import math
    log_sum = sum(math.log(w) for w in weights if w > 0)
    n = len([w for w in weights if w > 0])
    if n == 0:
        return 0.0

    cai = math.exp(log_sum / n)
    return max(0.0, min(1.0, cai))


# ---------------------------------------------------------------------------
# Terminator Efficiency Prediction & Design
# ---------------------------------------------------------------------------

# Host-specific terminator motifs
HOST_TERMINATOR_MOTIFS = {
    "E.coli": {"stem": "GGGCCC", "loop": "AAA", "tail": "TTTTTT"},
    "B.subtilis": {"stem": "GCGCGC", "loop": "AAT", "tail": "TTTTTT"},
    "S.cerevisiae": {"stem": "GCGCGC", "loop": "AAT", "tail": "TTTTTT"},
}


def predict_terminator_efficiency(sequence: str) -> float:
    """Predict terminator efficiency (0-1) based on hairpin structure.

    Based on: GC content of stem, loop size, U-rich tail.
    """
    if not sequence:
        return 0.0

    seq = sequence.upper().replace("U", "T")

    # GC content score: higher GC content in stem region = stronger terminator
    gc_count = seq.count("G") + seq.count("C")
    gc_content = gc_count / len(seq) if seq else 0.0
    gc_score = gc_content  # 0-1 range

    # U-rich tail score: look for T-rich region at the 3' end
    # A strong terminator has a run of T's at the end
    tail_length = min(10, len(seq))
    tail = seq[-tail_length:]
    t_count = tail.count("T")
    tail_score = t_count / tail_length if tail_length > 0 else 0.0

    # Loop size score: optimal loop is 3-8 nt
    # We approximate by checking if there's a non-GC region in the middle
    mid_start = len(seq) // 3
    mid_end = 2 * len(seq) // 3
    if mid_end > mid_start:
        mid_region = seq[mid_start:mid_end]
        mid_gc = (mid_region.count("G") + mid_region.count("C")) / len(mid_region)
        # Lower GC in middle = better loop
        loop_score = 1.0 - mid_gc
    else:
        loop_score = 0.5

    # Weighted combination
    efficiency = (
        0.4 * gc_score
        + 0.4 * tail_score
        + 0.2 * loop_score
    )

    return max(0.0, min(1.0, efficiency))


def design_terminator(host: str = "E.coli") -> str:
    """Design a terminator sequence for the given host.

    Returns DNA sequence with hairpin + U-rich tail.
    """
    if host not in HOST_TERMINATOR_MOTIFS:
        raise ValueError(f"Unsupported host: {host}")

    motif = HOST_TERMINATOR_MOTIFS[host]

    # Construct terminator: stem + loop + reverse complement of stem + U-rich tail
    stem = motif["stem"]
    loop = motif["loop"]
    tail = motif["tail"]

    # Reverse complement of stem for the hairpin
    rc_stem = stem[::-1].translate(str.maketrans("ATGC", "TACG"))

    terminator = stem + loop + rc_stem + tail
    return terminator
