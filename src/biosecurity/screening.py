"""Biosecurity screening: sequence screening, dual-use detection, compliance, and gating."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

# Known threat sequence patterns (simplified motifs for screening)
THREAT_PATTERNS: dict[str, str] = {
    "botulinum_neurotoxin_light_chain": "GAGCTGCTGGACTTCGCT",
    "ricin_chain_A": "ATCGAGCTGCTGGACTTCGCT",
    "tetrodotoxin_binding": "TTCGCTGCTGCTGCTGCTGC",
    "anthrax_lethal_factor": "GCTATCGAGCTGCTGGACTTC",
    "cholera_toxin_A": "GCTGCTGGACTTCGCTATCGAG",
    "diphtheria_toxin": "CTGCTGGACTTCGCTATCGAGCTG",
    "shiga_toxin": "GAGCTGCTGGACTTCGCTATCGAGCT",
    "pertussis_toxin": "ATCGAGCTGCTGGACTTCGCTATCGAG",
}


def load_custom_patterns(patterns: dict[str, str]) -> None:
    """Load custom threat patterns into the global THREAT_PATTERNS dict."""
    THREAT_PATTERNS.update(patterns)


def save_patterns_to_file(filepath: str) -> None:
    """Save current threat patterns to a JSON file."""
    with open(filepath, "w") as f:
        json.dump(THREAT_PATTERNS, f, indent=2)


def load_patterns_from_file(filepath: str) -> None:
    """Load threat patterns from a JSON file."""
    with open(filepath) as f:
        patterns = json.load(f)
    THREAT_PATTERNS.update(patterns)


def get_pattern_count() -> int:
    """Return the number of threat patterns currently loaded."""
    return len(THREAT_PATTERNS)


# Dual-use concern patterns
DUAL_USE_PATTERNS: dict[str, str] = {
    "virulence_factor": "GCTATCGAGCTGCTGGACTTC",
    "toxin_related": "TTCGCTGCTGCTGCTGCTGC",
    "antibiotic_resistance_marker": "GAGCTGCTGGACTTCGCT",
    "immune_evasion": "ATCGAGCTGCTGGACTTCGCT",
    "host_cell_entry": "CTGCTGGACTTCGCTATCGAGCTG",
}

# Regulatory frameworks
REGULATORY_FRAMEWORKS: dict[str, dict[str, Any]] = {
    "NIH": {
        "name": "NIH Guidelines for Recombinant/Synthetic Nucleic Acid Research",
        "risk_threshold": 0.6,
        "requires_review_above": 0.3,
    },
    "WHO": {
        "name": "WHO Laboratory Biosafety Manual",
        "risk_threshold": 0.5,
        "requires_review_above": 0.25,
    },
    "CDC": {
        "name": "CDC Biosafety in Microbiological and Biomedical Laboratories",
        "risk_threshold": 0.7,
        "requires_review_above": 0.35,
    },
}


# Synonymous codon groups for watermarking
WATERMARK_CODON_GROUPS: list[list[str]] = [
    ["GCT", "GCC", "GCA", "GCG"],  # Ala
    ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],  # Ser
    ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],  # Arg
    ["GGT", "GGC", "GGA", "GGG"],  # Gly
    ["CCT", "CCC", "CCA", "CCG"],  # Pro
    ["ACT", "ACC", "ACA", "ACG"],  # Thr
    ["GTT", "GTC", "GTA", "GTG"],  # Val
    ["CTT", "CTC", "CTA", "CTG"],  # Leu
]

# Build lookup: codon -> (group, index_in_group)
_WATERMARK_CODON_MAP: dict[str, tuple[list[str], int]] = {}
for _group in WATERMARK_CODON_GROUPS:
    for _i, _codon in enumerate(_group):
        _WATERMARK_CODON_MAP[_codon] = (_group, _i)


def embed_watermark(sequence: str, watermark: str) -> str:
    """Embed a binary watermark into a DNA sequence via synonymous codon substitution.

    For each bit, finds the next codon in a synonymous group and replaces it
    with group[0] (bit '0') or group[1] (bit '1'). Preserves amino acid sequence.
    """
    if not watermark:
        return sequence

    seq_upper = sequence.upper()
    result = list(seq_upper)
    bit_index = 0

    for i in range(0, len(seq_upper) - 2, 3):
        if bit_index >= len(watermark):
            break
        codon = seq_upper[i : i + 3]
        entry = _WATERMARK_CODON_MAP.get(codon)
        if entry is not None:
            group, _ = entry
            target = group[0] if watermark[bit_index] == "0" else group[1]
            result[i : i + 3] = list(target)
            bit_index += 1

    return "".join(result)


def verify_watermark(sequence: str, watermark: str) -> bool:
    """Verify if a DNA sequence contains the given binary watermark.

    Extracts bits from synonymous codon positions and compares with watermark.
    """
    if not watermark:
        return True

    seq_upper = sequence.upper()
    extracted: list[str] = []

    for i in range(0, len(seq_upper) - 2, 3):
        if len(extracted) >= len(watermark):
            break
        codon = seq_upper[i : i + 3]
        entry = _WATERMARK_CODON_MAP.get(codon)
        if entry is not None:
            _, pos = entry
            if pos == 0:
                extracted.append("0")
            elif pos == 1:
                extracted.append("1")
            else:
                extracted.append("?")

    return "".join(extracted)[: len(watermark)] == watermark


class SequenceScreener:
    """Screen DNA sequences against known threat patterns."""

    def __init__(self) -> None:
        self.threat_patterns = THREAT_PATTERNS

    def _reverse_complement(self, seq: str) -> str:
        """Return the reverse complement of a DNA sequence."""
        comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
        return "".join(comp.get(c, c) for c in reversed(seq.upper()))

    def screen_sequence(self, sequence: str) -> dict[str, Any]:
        """Check sequence against known threat patterns.

        Searches both forward and reverse-complement strands.

        Returns dict with:
            is_clean: bool - True if no threat patterns found
            matches: list[str] - names of matched threat patterns
        """
        if not sequence:
            return {"is_clean": True, "matches": []}

        seq_upper = sequence.upper()
        rc = self._reverse_complement(seq_upper)
        matches: list[str] = []

        for name, pattern in self.threat_patterns.items():
            if pattern in seq_upper or pattern in rc:
                matches.append(name)

        return {
            "is_clean": len(matches) == 0,
            "matches": matches,
        }

    def calculate_risk_score(self, sequence: str) -> float:
        """Calculate a 0-1 risk score for a sequence.

        Score is based on:
            - Number of threat pattern matches
            - GC content deviation from normal (50%)
            - Sequence length (very short or very long sequences score higher)
        """
        if not sequence:
            return 0.0

        seq_upper = sequence.upper()
        rc = self._reverse_complement(seq_upper)
        score = 0.0

        # Threat pattern contribution (up to 0.6)
        threat_count = 0
        for pattern in self.threat_patterns.values():
            if pattern in seq_upper or pattern in rc:
                threat_count += 1
        score += min(threat_count * 0.2, 0.6)

        # GC content deviation (up to 0.2)
        gc_count = seq_upper.count("G") + seq_upper.count("C")
        gc_content = gc_count / len(seq_upper) if seq_upper else 0.0
        gc_deviation = abs(gc_content - 0.5)
        score += min(gc_deviation * 0.4, 0.2)

        # Length anomaly (up to 0.2)
        seq_len = len(sequence)
        if seq_len < 20:
            score += 0.1
        elif seq_len > 10000:
            score += 0.1

        return min(score, 1.0)

    def check_homology(self, sequence: str, reference: str) -> dict[str, Any]:
        """Check homology between a sequence and a reference.

        Uses a simple k-mer based approach:
            - Extract k-mers (k=8) from both sequences
            - Calculate Jaccard similarity

        Returns dict with:
            homology: float - 0.0 to 1.0 similarity score
            is_homologous: bool - True if homology >= 0.7
        """
        if not sequence or not reference:
            return {"homology": 0.0, "is_homologous": False}

        k = 8
        seq_upper = sequence.upper()
        ref_upper = reference.upper()

        if len(seq_upper) < k or len(ref_upper) < k:
            return {"homology": 0.0, "is_homologous": False}

        # Extract k-mers
        seq_kmers = {seq_upper[i:i+k] for i in range(len(seq_upper) - k + 1)}
        ref_kmers = {ref_upper[i:i+k] for i in range(len(ref_upper) - k + 1)}

        # Jaccard similarity
        intersection = seq_kmers & ref_kmers
        union = seq_kmers | ref_kmers

        homology = len(intersection) / len(union) if union else 0.0

        return {
            "homology": round(homology, 4),
            "is_homologous": homology >= 0.7,
        }

    def screen_batch(self, sequences: list[str]) -> list[dict[str, Any]]:
        """Screen a batch of sequences against known threat patterns.

        Returns a list of screen_sequence results, one per input sequence.
        """
        return [self.screen_sequence(seq) for seq in sequences]

    def calculate_risk_batch(self, sequences: list[str]) -> list[float]:
        """Calculate risk scores for a batch of sequences.

        Returns a list of risk scores, one per input sequence.
        """
        return [self.calculate_risk_score(seq) for seq in sequences]


class DualUseDetector:
    """Detect potential dual-use DNA sequences."""

    def __init__(self) -> None:
        self.dual_use_patterns = DUAL_USE_PATTERNS

    def detect_dual_use(self, sequence: str) -> dict[str, Any]:
        """Flag potential dual-use sequences.

        Returns dict with:
            is_dual_use: bool - True if any dual-use patterns found
            flags: list[str] - names of matched dual-use patterns
        """
        if not sequence:
            return {"is_dual_use": False, "flags": []}

        seq_upper = sequence.upper()
        flags: list[str] = []

        for name, pattern in self.dual_use_patterns.items():
            if pattern in seq_upper:
                flags.append(name)

        return {
            "is_dual_use": len(flags) > 0,
            "flags": flags,
        }

    def classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level from a 0-1 risk score.

        Levels:
            Low: 0.0 - 0.3
            Medium: 0.3 - 0.6
            High: 0.6 - 0.85
            Extreme: 0.85 - 1.0
        """
        if risk_score < 0.0:
            risk_score = 0.0
        if risk_score > 1.0:
            risk_score = 1.0

        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Medium"
        elif risk_score < 0.85:
            return "High"
        else:
            return "Extreme"


class ComplianceChecker:
    """Verify sequences against regulatory frameworks."""

    def __init__(self) -> None:
        self.frameworks = REGULATORY_FRAMEWORKS
        self.screener = SequenceScreener()
        self.dual_use_detector = DualUseDetector()

    def check_compliance(self, sequence: str, framework: str = "NIH") -> dict[str, Any]:
        """Verify sequence against a regulatory framework.

        Returns dict with:
            compliant: bool - True if sequence passes compliance
            violations: list[str] - descriptions of violations
            framework: str - the framework checked against
        """
        if not sequence:
            return {"compliant": True, "violations": [], "framework": framework}

        if framework not in self.frameworks:
            return {
                "compliant": False,
                "violations": [f"Unknown regulatory framework: {framework}"],
                "framework": framework,
            }

        violations: list[str] = []
        config = self.frameworks[framework]

        # Check threat patterns
        screening = self.screener.screen_sequence(sequence)
        if not screening["is_clean"]:
            for match in screening["matches"]:
                violations.append(f"Threat pattern detected: {match}")

        # Check dual-use
        dual_use = self.dual_use_detector.detect_dual_use(sequence)
        if dual_use["is_dual_use"]:
            for flag in dual_use["flags"]:
                violations.append(f"Dual-use concern: {flag}")

        # Check risk score against framework threshold
        risk_score = self.screener.calculate_risk_score(sequence)
        if risk_score > config["risk_threshold"]:
            violations.append(
                f"Risk score {risk_score:.2f} exceeds {framework} threshold "
                f"({config['risk_threshold']})"
            )

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "framework": framework,
        }

    def generate_report(self, sequence: str, framework: str = "NIH") -> dict[str, Any]:
        """Generate a compliance report for a sequence.

        Returns dict with:
            sequence_length: int
            framework: str
            compliant: bool
            violations: list[str]
            risk_score: float
            risk_level: str
            screening_result: dict
            dual_use_result: dict
        """
        compliance = self.check_compliance(sequence, framework=framework)
        risk_score = self.screener.calculate_risk_score(sequence)
        risk_level = self.dual_use_detector.classify_risk_level(risk_score)
        screening = self.screener.screen_sequence(sequence)
        dual_use = self.dual_use_detector.detect_dual_use(sequence)

        return {
            "sequence_length": len(sequence),
            "framework": framework,
            "compliant": compliance["compliant"],
            "violations": compliance["violations"],
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "screening_result": screening,
            "dual_use_result": dual_use,
        }


def _reverse_complement(seq: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp.get(c, c) for c in reversed(seq.upper()))


def _kmer_jaccard(sequence: str, reference: str, k: int = 8) -> float:
    """Calculate Jaccard similarity between k-mer sets of two sequences."""
    if not sequence or not reference:
        return 0.0
    seq_upper = sequence.upper()
    ref_upper = reference.upper()
    if len(seq_upper) < k or len(ref_upper) < k:
        return 0.0
    seq_kmers = {seq_upper[i : i + k] for i in range(len(seq_upper) - k + 1)}
    ref_kmers = {ref_upper[i : i + k] for i in range(len(ref_upper) - k + 1)}
    intersection = seq_kmers & ref_kmers
    union = seq_kmers | ref_kmers
    return len(intersection) / len(union) if union else 0.0


def check_homology_both_strands(sequence: str, reference: str) -> dict:
    """Check homology between a sequence and a reference on both strands.

    Checks the forward strand and the reverse complement of the sequence
    against the reference using k-mer Jaccard similarity.

    Returns dict with:
        homology: float - 0.0 to 1.0 similarity score
        is_homologous: bool - True if homology >= 0.7
        strand: str - 'forward', 'reverse', or 'none'
    """
    if not sequence or not reference:
        return {"homology": 0.0, "is_homologous": False, "strand": "none"}

    seq_upper = sequence.upper()
    ref_upper = reference.upper()

    forward_score = _kmer_jaccard(seq_upper, ref_upper)
    rc = _reverse_complement(seq_upper)
    reverse_score = _kmer_jaccard(rc, ref_upper)

    if forward_score >= reverse_score:
        best_score = forward_score
        best_strand = "forward"
    else:
        best_score = reverse_score
        best_strand = "reverse"

    is_homologous = best_score >= 0.7
    if not is_homologous:
        best_strand = "none"

    return {
        "homology": round(best_score, 4),
        "is_homologous": is_homologous,
        "strand": best_strand,
    }


def batch_check_homology(sequences: list[str], reference: str) -> list[dict]:
    """Check homology for multiple sequences against a reference.

    Returns a list of homology result dicts, one per input sequence.
    """
    return [check_homology_both_strands(seq, reference) for seq in sequences]


def classify_bsl_level(sequence: str) -> str:
    """Classify a DNA sequence into a Biosafety Level (BSL-1 through BSL-4).

    Classification is based on:
    - BSL-1: No threat patterns, normal GC content
    - BSL-2: No threats but unusual GC content (>80% or <20%), or dual-use patterns
    - BSL-3: Known toxin/virulence threat patterns detected
    - BSL-4: Multiple high-risk threat patterns detected

    Args:
        sequence: DNA sequence to classify.

    Returns:
        BSL level string: "BSL-1", "BSL-2", "BSL-3", or "BSL-4".
    """
    if not sequence:
        return "BSL-1"

    seq_upper = sequence.upper()

    # Count threat pattern matches
    threat_count = 0
    for pattern in THREAT_PATTERNS.values():
        if pattern in seq_upper:
            threat_count += 1

    # Multiple threats → BSL-4
    if threat_count >= 2:
        return "BSL-4"

    # Single threat → BSL-3
    if threat_count == 1:
        return "BSL-3"

    # Check GC content
    gc_count = seq_upper.count("G") + seq_upper.count("C")
    gc_content = gc_count / len(seq_upper) if seq_upper else 0.0

    # Unusual GC content → BSL-2
    if gc_content > 0.8 or gc_content < 0.2:
        return "BSL-2"

    # Check dual-use patterns
    for pattern in DUAL_USE_PATTERNS.values():
        if pattern in seq_upper:
            return "BSL-2"

    return "BSL-1"


def check_bsl_clearance(sequence: str, user_bsl_level: str) -> dict:
    """Check if a user with given BSL clearance can handle a sequence.

    Args:
        sequence: DNA sequence to check.
        user_bsl_level: User's BSL clearance level (e.g., "BSL-2").

    Returns:
        Dict with 'allowed', 'required_bsl', and 'reason' keys.
    """
    required_bsl = classify_bsl_level(sequence)

    # Parse BSL levels to integers
    try:
        user_level = int(user_bsl_level.replace("BSL-", ""))
    except (ValueError, AttributeError):
        return {
            "allowed": False,
            "required_bsl": required_bsl,
            "reason": f"Invalid BSL level: {user_bsl_level}",
        }

    try:
        required_level = int(required_bsl.replace("BSL-", ""))
    except (ValueError, AttributeError):
        return {
            "allowed": False,
            "required_bsl": required_bsl,
            "reason": f"Invalid required BSL level: {required_bsl}",
        }

    if user_level >= required_level:
        return {
            "allowed": True,
            "required_bsl": required_bsl,
            "reason": (
                f"User clearance ({user_bsl_level}) is sufficient "
                f"for {required_bsl} sequence"
            ),
        }
    else:
        return {
            "allowed": False,
            "required_bsl": required_bsl,
            "reason": (
                f"Insufficient clearance: user has {user_bsl_level} "
                f"but sequence requires {required_bsl}"
            ),
        }


class BiosecurityGate:
    """Gate that evaluates sequences for biosecurity compliance."""

    def __init__(self) -> None:
        self.screener = SequenceScreener()
        self.dual_use_detector = DualUseDetector()
        self.compliance_checker = ComplianceChecker()
        self._audit_log: list[dict[str, Any]] = []
        self._callbacks: list = []

    def add_callback(self, callback) -> None:
        """Add a callback that fires when a sequence fails screening."""
        self._callbacks.append(callback)

    def clear_callbacks(self) -> None:
        """Clear all registered callbacks."""
        self._callbacks.clear()

    def evaluate(self, sequence: str, framework: str = "NIH") -> dict[str, Any]:
        """Evaluate a sequence through the biosecurity gate.

        Returns dict with:
            passed: bool - True if sequence passes all checks
            risk_level: str - Low/Medium/High/Extreme
            risk_score: float - 0-1 risk score
            screening_result: dict
            dual_use_result: dict
            compliance_result: dict
        """
        if not sequence:
            result = {
                "passed": True,
                "risk_level": "Low",
                "risk_score": 0.0,
                "screening_result": {"is_clean": True, "matches": []},
                "dual_use_result": {"is_dual_use": False, "flags": []},
                "compliance_result": {"compliant": True, "violations": []},
            }
        else:
            screening = self.screener.screen_sequence(sequence)
            dual_use = self.dual_use_detector.detect_dual_use(sequence)
            compliance = self.compliance_checker.check_compliance(sequence, framework=framework)
            risk_score = self.screener.calculate_risk_score(sequence)
            risk_level = self.dual_use_detector.classify_risk_level(risk_score)

            # Gate passes if: no threat matches, no dual-use flags, and compliant
            passed = (
                screening["is_clean"]
                and not dual_use["is_dual_use"]
                and compliance["compliant"]
            )

            result = {
                "passed": passed,
                "risk_level": risk_level,
                "risk_score": round(risk_score, 4),
                "screening_result": screening,
                "dual_use_result": dual_use,
                "compliance_result": compliance,
            }

        if not result["passed"]:
            reasons = []
            if not result["screening_result"]["is_clean"]:
                reasons.append("threat pattern detected")
            if result["dual_use_result"]["is_dual_use"]:
                reasons.append("dual-use concern")
            if not result["compliance_result"]["compliant"]:
                reasons.append("compliance violation")
            reason = "; ".join(reasons) if reasons else "unknown"
            for cb in self._callbacks:
                cb(sequence, reason)

        self._audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "sequence_hash": hashlib.sha256(sequence.encode()).hexdigest(),
            "result": "passed" if result["passed"] else "failed",
            "framework": framework,
        })

        return result

    def get_audit_log(self) -> list[dict[str, Any]]:
        """Return the audit log entries."""
        return self._audit_log

    def clear_audit_log(self) -> None:
        """Clear all audit log entries."""
        self._audit_log.clear()
