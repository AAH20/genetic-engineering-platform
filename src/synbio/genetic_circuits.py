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
